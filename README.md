# TIWARI AI AGENT

Native Android assistant with a cloud backend.

- Android: Kotlin, package `com.tiwari.aiagent`
- Wake phrase target: Hey Tiwari (background microphone service is a later step)
- Languages: Hindi, Hinglish, English
- Backend: FastAPI on Render Free
- Data: Firebase Realtime Database (credentials configured later)
- Excel exports: OpenPyXL
- SQLite: not used

## Render deployment
In Render choose New + → Blueprint, connect this repository, and deploy `render.yaml`.

## Android build
Open `android/` in Android Studio and build the debug APK. Android SDK is required.
