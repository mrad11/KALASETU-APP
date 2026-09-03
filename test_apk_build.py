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
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
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

    def do_HEAD(self):
        super().do_HEAD()

def run_server(port=8080):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    server = ThreadingHTTPServer(('127.0.0.1', port), KalaSetuHandler)
    server.serve_forever()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    port = 8080

    print("[*] Starting multi-threaded HTTP server...")
    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()
    time.sleep(1)

    print("[*] Starting Cloudflare tunnel...")
    cf_proc = subprocess.Popen(
        ['cloudflared.exe', 'tunnel', '--url', f'http://127.0.0.1:{port}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    public_url = None
    start = time.time()
    while time.time() - start < 25:
        line = cf_proc.stderr.readline()
        if not line:
            time.sleep(0.2)
            continue
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            public_url = match.group(0)
            break

    if not public_url:
        print("[!] Failed to get Cloudflare tunnel URL.")
        cf_proc.terminate()
        return

    print(f"[*] LIVE PUBLIC URL: {public_url}")
    print("[*] Waiting for DNS propagation (6s)...")
    time.sleep(6)

    payload = {
        "packageId": "com.kalasetu.ai",
        "name": "KalaSetu AI",
        "launcherName": "KalaSetu",
        "shortName": "KalaSetu",
        "host": public_url,
        "startUrl": "/index.html",
        "themeColor": "#1f5d4e",
        "navigationColor": "#1f5d4e",
        "backgroundColor": "#f0ede5",
        "display": "standalone",
        "appVersion": "1.0.0.0",
        "appVersionCode": 1,
        "iconUrl": f"{public_url}/icon-512.png",
        "maskableIconUrl": f"{public_url}/icon-maskable-512.png",
        "webManifestUrl": f"{public_url}/manifest.webmanifest",
        "fallbackType": "customtabs",
        "enableNotifications": False,
        "includeSourceCode": False,
        "signingMode": "none",
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

    print("[*] Calling PWABuilder CloudAPK API...")
    try:
        with urllib.request.urlopen(api_req, timeout=180) as resp:
            print(f"[*] Response status: {resp.status}")
            data = resp.read()
            zip_path = os.path.join(script_dir, "KalaSetu-Android-Package.zip")
            apk_path = os.path.join(script_dir, "KalaSetu-AI.apk")
            with open(zip_path, 'wb') as f:
                f.write(data)
            print(f"[SUCCESS] Downloaded package: {zip_path} ({len(data)} bytes)!")

            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for name in z.namelist():
                    print(f"  - Package file: {name}")
                    if name.endswith('.apk'):
                        with open(apk_path, 'wb') as out_apk:
                            out_apk.write(z.read(name))
                        print(f"\n>>> [SUCCESS] APK EXTRACTED TO: {apk_path} ({os.path.getsize(apk_path)} bytes) <<<\n")

    except Exception as e:
        print(f"[!] API call failed: {e}")
        if hasattr(e, 'read'):
            try:
                print("Server detail:", e.read().decode('utf-8', errors='ignore'))
            except Exception:
                pass

    cf_proc.terminate()

if __name__ == '__main__':
    main()
