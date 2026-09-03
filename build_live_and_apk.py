import os
import sys
import time
import re
import json
import zipfile
import io
import urllib.request
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import mimetypes

mimetypes.add_type('application/manifest+json', '.webmanifest')
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('audio/mpeg', '.mp3')
mimetypes.add_type('image/png', '.png')
mimetypes.add_type('image/x-icon', '.ico')

class KalaSetuHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

def run_local_server(port=8080):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    server = HTTPServer(('127.0.0.1', port), KalaSetuHandler)
    server.serve_forever()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    port = 8080

    print("=" * 60)
    print(" 1. Starting local web server on port 8080...")
    print("=" * 60)
    server_thread = threading.Thread(target=run_local_server, args=(port,), daemon=True)
    server_thread.start()
    time.sleep(1)

    print("=" * 60)
    print(" 2. Establishing secure Cloudflare Public Live URL...")
    print("=" * 60)
    cf_proc = subprocess.Popen(
        ['cloudflared.exe', 'tunnel', '--url', f'http://127.0.0.1:{port}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    public_url = None
    start = time.time()
    while time.time() - start < 20:
        line = cf_proc.stderr.readline()
        if not line:
            time.sleep(0.2)
            continue
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            public_url = match.group(0)
            break

    if not public_url:
        print("[!] Could not obtain Cloudflare public URL.")
        cf_proc.terminate()
        sys.exit(1)

    print(f"[*] LIVE PUBLIC HTTPS URL: {public_url}")
    print(f"[*] Testing connection to {public_url}/index.html ...")

    # Verify connection
    req = urllib.request.Request(f"{public_url}/index.html", headers={'User-Agent': 'PWABuilder-Test'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"[*] Live site status: {r.status} OK!")
    except Exception as e:
        print(f"[!] Warning checking live site: {e}")

    # Step 3: Trigger PWABuilder CloudAPK API
    print("=" * 60)
    print(" 3. Building Android APK via PWABuilder CloudAPK API...")
    print("=" * 60)

    payload = {
        "name": "KalaSetu AI",
        "shortName": "KalaSetu AI",
        "host": public_url,
        "startUrl": "/index.html",
        "themeColor": "#1f5d4e",
        "backgroundColor": "#f0ede5",
        "display": "standalone",
        "packageId": "ai.kalasetu.craft",
        "appVersion": "1.0.0",
        "appVersionCode": 1,
        "iconUrl": f"{public_url}/icon-512.png",
        "maskableIconUrl": f"{public_url}/icon-maskable-512.png",
        "webManifestUrl": f"{public_url}/manifest.webmanifest",
        "enableNotifications": False,
        "features": {
            "locationDelegation": {"enabled": False},
            "playBilling": {"enabled": False}
        }
    }

    req_data = json.dumps(payload).encode('utf-8')
    api_url = "https://pwabuilder-cloudapk.azurewebsites.net/generateAppPackage"
    api_req = urllib.request.Request(
        api_url,
        data=req_data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        },
        method="POST"
    )

    apk_path = os.path.join(script_dir, "KalaSetu-AI.apk")
    zip_path = os.path.join(script_dir, "KalaSetu-Android-Package.zip")

    try:
        print("[*] Sending request to PWABuilder CloudAPK service...")
        with urllib.request.urlopen(api_req, timeout=180) as resp:
            print(f"[*] PWABuilder responded with status: {resp.status}")
            zip_bytes = resp.read()
            print(f"[*] Received package size: {len(zip_bytes)} bytes")

            with open(zip_path, 'wb') as f:
                f.write(zip_bytes)
            print(f"[*] Saved package to: {zip_path}")

            # Extract APK
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
                for filename in z.namelist():
                    print(f"    - Archive contains: {filename}")
                    if filename.endswith('.apk'):
                        with open(apk_path, 'wb') as out_apk:
                            out_apk.write(z.read(filename))
                        print(f"\n[SUCCESS] Extracted Android APK: {apk_path} ({os.path.getsize(apk_path)} bytes)!")
                        break

    except Exception as e:
        print(f"[!] Error building APK via CloudAPK API: {e}")
        if hasattr(e, 'read'):
            try:
                print("Server response:", e.read().decode('utf-8', errors='ignore'))
            except Exception:
                pass

    # Keep tunnel alive if desired
    print("\n" + "=" * 60)
    print(f" LIVE PUBLIC LINK FOR YOUR PWA: {public_url}")
    print("=" * 60)
    return public_url

if __name__ == '__main__':
    main()
