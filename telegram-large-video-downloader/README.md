# Telegram Large Video Downloader (Termux)

This folder contains a separate Android/Termux MTProto downloader. It does not modify the TIWARI AI AGENT Android app or backend.

## What it does

1. Uses your Telegram user session (Telethon) to download media by chat/channel and message ID, including files larger than the Bot API's 20 MB download limit when Telegram permits that account to access the media.
2. Streams the downloaded file to an authenticated HTTPS upload endpoint that you control.
3. Deletes the local temporary file after the transfer attempt.

## Important: Render connection is not complete yet

The Termux client expects a Render receiver endpoint at `RENDER_UPLOAD_URL` that accepts `multipart/form-data` field `file` and checks `Authorization: Bearer <token>`. That receiver must be added to the actual Render application and connected to its existing video-analysis/upload workflow before this tool can work end-to-end. Do not point this client at the current bot URL until that endpoint exists. This repository folder alone does not create or deploy a Render endpoint.

## Termux setup

```bash
pkg update -y
pkg install python -y
cd ~/tiwari-ai-agent-/telegram-large-video-downloader
pip install -r requirements.txt
cp .env.example .env
nano .env
```

Create Telegram API credentials at https://my.telegram.org and put the API ID/hash in `.env`. Set the Render URL/token only after the receiver endpoint is implemented. Never commit `.env` or `telegram_user_session.session`.

First run asks for your phone number, OTP, and (if enabled) Telegram 2-step verification password. The session file is sensitive: keep it private and never upload it to GitHub or share it.

## Run

```bash
python bridge.py <chat-or-channel> <message-id>
```

Example:

```bash
python bridge.py me 123
```

The example means message ID 123 in Saved Messages. The script downloads media, posts it to the configured receiver, then removes the local temporary video. Keep enough free phone storage for the full file plus working space, and keep Termux awake with a stable internet connection.

## Limits and safety

- 1–2 GB is a target, not a guarantee. Telegram account access, media size, network stability, phone storage, and the Render receiver's request/body limits all matter.
- A Render free instance may sleep or have insufficient disk/request limits for large uploads. Confirm the actual service plan and storage before using large files.
- This tool does not bypass Telegram restrictions, OTP, or access controls.
- The current script sends a file to a receiver; it does not itself invoke Gemini or YouTube upload. That connection belongs in the Render receiver integration.
