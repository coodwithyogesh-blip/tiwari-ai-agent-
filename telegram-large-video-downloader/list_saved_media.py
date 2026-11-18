#!/usr/bin/env python3
"""List recent media messages in Telegram Saved Messages."""
import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()


async def main() -> None:
    api_id = int(os.environ["TG_API_ID"])
    api_hash = os.environ["TG_API_HASH"]
    async with TelegramClient("telegram_user_session", api_id, api_hash) as client:
        print("Recent media in Saved Messages:")
        found = 0
        async for message in client.iter_messages("me", limit=30):
            if message.media:
                name = message.file.name if message.file and message.file.name else "media (no filename)"
                print(f"ID: {message.id} | {name}")
                found += 1
                if found >= 10:
                    break
        if not found:
            print("No media found. Send a video to your Telegram Saved Messages first.")


if __name__ == "__main__":
    asyncio.run(main())
