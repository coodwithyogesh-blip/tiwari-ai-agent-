#!/usr/bin/env python3
"""Termux MTProto downloader -> authenticated HTTP upload bridge.

Downloads a Telegram media message with a logged-in user session, then streams
it to a configured HTTPS receiver. No Telegram session or secrets belong in Git.
"""
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
        raise SystemExit(f"Missing {name}. Copy .env.example to .env and fill it in.")
    return value


async def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python bridge.py <chat-or-channel> <message-id>")

    api_id = int(required("TG_API_ID"))
    api_hash = required("TG_API_HASH")
    upload_url = required("RENDER_UPLOAD_URL")
    upload_token = required("RENDER_UPLOAD_TOKEN")
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
        # Avoid path traversal from a Telegram-supplied filename.
        safe_name = Path(name).name.replace("\\", "_") or f"telegram-{message_id}.bin"
        destination = download_dir / safe_name
        print(f"Downloading {safe_name} ...")
        downloaded = await client.download_media(message, file=str(destination))
        if not downloaded:
            raise SystemExit("Telegram download failed.")

    try:
        size_mb = destination.stat().st_size / (1024 * 1024)
        print(f"Downloaded {size_mb:.1f} MB. Sending to Render ...")
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
    finally:
        try:
            destination.unlink(missing_ok=True)
            print("Temporary video deleted from phone.")
        except OSError as exc:
            print(f"Could not delete temporary file: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
