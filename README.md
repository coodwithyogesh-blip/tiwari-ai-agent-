# TIWARI AI AGENT

Native Android assistant with a cloud backend.

## Confirmed product settings
- Android + web + GitHub + Render control mode
- Safe read-only tasks may run automatically after their integrations are configured
- Ask the owner before payments, final bookings, purchases, cancellations, sending messages, or account changes
- Hindi, Hinglish, and English
- Android: Kotlin, package `com.tiwari.aiagent`
- Backend: FastAPI on Render Free
- Planned data: Firebase Realtime Database and Excel exports (OpenPyXL)
- SQLite is not used

## Current implementation status
- Android app can connect to a Render URL and send chat requests.
- Backend exposes `/api/health`, `/api/capabilities`, `/api/plan`, and `/api/chat`.
- A conservative command planner classifies rail, Zepto/shopping, GitHub, email, SMS, WhatsApp, ChatGPT, and phone requests.
- The planner does not execute external actions. It explicitly reports `not_configured` until a real, permitted integration is implemented.
- Backend policy tests run in GitHub Actions alongside the Android APK build.

## Important safety and platform notes
- A purchase, payment, final ticket booking, cancellation, outgoing SMS/email/message, or account change must get explicit confirmation.
- Read-only lookups can be automated only after the relevant official API or permitted integration is configured.
- Android SMS, microphone, contacts, and accessibility capabilities require runtime permissions and visible user consent.
- A force-stopped app or powered-off phone cannot continuously listen for the wake phrase.
- Never commit API keys, Firebase service-account JSON, OTPs, passwords, or payment credentials.

## Render deployment
In Render choose New + → Blueprint, connect this repository, and deploy `render.yaml`.

## Android build
Open `android/` in Android Studio and build the debug APK, or use the GitHub Actions workflow artifact. Android SDK is required.
