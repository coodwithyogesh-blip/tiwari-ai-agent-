#!/usr/bin/env python3
"""Download Telegram media with MTProto; optionally upload to a configured receiver."""
import asyncio
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()


def required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing {name}. Check your .env file.")
    return value


async def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python bridge.py <chat-or-channel> <message-id>")

    api_id = int(required("TG_API_ID"))
    api_hash = required("TG_API_HASH")
    upload_url = os.getenv("RENDER_UPLOAD_URL", "").strip()
    upload_token = os.getenv("RENDER_UPLOAD_TOKEN", "").strip()
    download_dir = Path(os.getenv("DOWNLOAD_DIR", "./downloads")).expanduser()
    download_dir.mkdir(parents=True, exist_ok=True)

    chat = sys.argv[1]
    message_id = int(sys.argv[2])
    session_path = str(Path("./telegram_user_session").resolve())

    async with TelegramClient(session_path, api_id, api_hash) as client:
        message = await client.get_messages(chat, ids=message_id)
        if not message or not message.media:
            raise SystemExit("Message not found or it has no downloadable media.")

        name = (message.file.name if message.file and message.file.name else f"telegram-{message_id}.bin")
        safe_name = Path(name).name.replace("\\", "_") or f"telegram-{message_id}.bin"
        destination = download_dir / safe_name
        print(f"Downloading {safe_name} ...")
        downloaded = await client.download_media(message, file=str(destination))
        if not downloaded:
            raise SystemExit("Telegram download failed.")

    size_mb = destination.stat().st_size / (1024 * 1024)
    print(f"Downloaded {size_mb:.1f} MB.")
    if not upload_url or not upload_token:
        print("Render upload is not configured yet.")
        print(f"Video safely saved on this phone: {destination.resolve()}")
        return

    print("Sending to Render ...")
    try:
        with destination.open("rb") as stream:
            response = requests.post(
                upload_url,
                headers={"Authorization": f"Bearer {upload_token}"},
                files={"file": (destination.name, stream, "application/octet-stream")},
                data={"source": "termux-mtproto"},
                timeout=(30, 60 * 60),
            )
        response.raise_for_status()
        print("Upload accepted by Render:")
        print(response.text[:2000])
    except Exception:
        print("Upload failed. The downloaded video has been kept on this phone.")
        print(f"Saved at: {destination.resolve()}")
        raise
    else:
        destination.unlink(missing_ok=True)
        print("Render accepted the upload; local temporary video deleted.")


if __name__ == "__main__":
    asyncio.run(main())
