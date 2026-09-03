# KalaSetu AI — Phone & Desktop App Guide

This package contains everything needed to run, install, and distribute **KalaSetu AI** as a standalone application on **Windows/macOS Desktop** and **Android/iOS Mobile Phones**.

---

## 1. Instant Desktop App (Windows)

You can run KalaSetu AI as a standalone desktop app right now on your PC:

### Option A: Install Desktop Shortcut (Recommended)
1. In this folder, double-click **`Install-KalaSetu-Desktop.bat`**.
2. A shortcut named **`KalaSetu AI`** with the custom KalaSetu icon will appear on your Windows Desktop.
3. Double-clicking it opens KalaSetu in a **dedicated, borderless app window** (no browser URL bar, no tabs, standalone taskbar icon).

### Option B: Quick Launcher
- Double-click **`Start-KalaSetu-App.cmd`** anytime to launch the standalone desktop window directly.

---

## 2. Install on Phone over Local Wi-Fi (No Cloud Setup Needed)

To install KalaSetu directly onto your Android phone or iPhone right now:

1. Double-click **`Run-KalaSetu-Server.bat`**.
2. A browser page will open displaying:
   - A **QR Code**.
   - Your local network link (e.g., `http://192.168.1.xxx:8080/index.html`).
3. Make sure your phone is connected to the **same Wi-Fi network** as your computer.
4. Open your phone's camera and **scan the QR code** (or type the link into your phone's browser).
5. **Install on Phone**:
   - **On Android (Google Chrome):** Tap the three-dot menu (**⋮**) in the top right, then tap **Install app** or **Add to Home screen**.
   - **On iPhone / iPad (Safari):** Tap the **Share** button (the square with an arrow pointing up), then tap **Add to Home Screen**.
6. The KalaSetu AI app icon will now appear on your phone's home screen, functioning like a native mobile app with voice playback and offline caching!

---

## 3. Free 1-Click Cloud Hosting (Accessible Worldwide)

If you want a live HTTPS link to send to clients, team members, or open on your phone without needing Wi-Fi:

### Fastest Option: Netlify Drop (10 Seconds, No Terminal Needed)
1. Go to [https://app.netlify.com/drop](https://app.netlify.com/drop).
2. Drag and drop this entire `outputs` folder onto the page.
3. Netlify will instantly give you a free, permanent HTTPS link (e.g., `https://kalasetu-ai.netlify.app`).
4. Any phone or computer can open that link and click "Install" to download the app!

### Option B: GitHub Pages
1. Push this `outputs` folder to a GitHub repository.
2. In the repository, go to **Settings** → **Pages**.
3. Under **Build and deployment**, select `Deploy from a branch` (main / root).
4. Your app will be live at `https://<username>.github.io/<repo-name>/`.

---

## 4. Generate a Downloadable Android `.apk` File

If you want a raw `.apk` file that Android users can download and install directly:

1. Deploy your app to a free HTTPS link (using Netlify Drop or GitHub Pages above).
2. Visit **[PWABuilder.com](https://www.pwabuilder.com)** (free, open-source tool created by Microsoft & Google).
3. Enter your live HTTPS URL and click **Start**.
4. PWABuilder will verify your manifest and service worker (both are 100% pre-configured in this folder).
5. Click **Package for Stores** → **Android**.
6. Click **Generate Package** / **Download APK**.
7. You now have a signed Android `.apk` ready for direct phone download and distribution!

---

## File Summary in this Directory

| File | Purpose |
|------|---------|
| `Install-KalaSetu-Desktop.bat` | 1-click Windows installer to create Desktop app shortcut |
| `Start-KalaSetu-App.cmd` | Direct desktop standalone app launcher |
| `Run-KalaSetu-Server.bat` | Starts local Wi-Fi server & opens phone QR code connection portal |
| `serve.py` | Python server with automatic IP detection and CORS/MIME handling |
| `connect.html` | Phone pairing page with QR code & install steps |
| `index.html` & `kalasetu-prototype.html` | Core KalaSetu AI application |
| `manifest.webmanifest` | PWA manifest for Android, iOS, and Desktop installability |
| `service-worker.js` | Offline caching and fast background loading |
| `icon-192.png`, `icon-512.png` | Standard high-resolution app icons |
| `icon-maskable-192.png`, `icon-maskable-512.png` | Android adaptive/maskable icons |
| `apple-touch-icon.png` | iOS home screen icon |
| `kalasetu-icon.ico` | Windows multi-resolution icon for shortcuts and taskbar |
| `audio/` | Voice playback files in 8 Indian languages |
