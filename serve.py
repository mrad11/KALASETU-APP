import os
import sys
import socket
import webbrowser
import mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Ensure correct mimetypes
mimetypes.add_type('application/manifest+json', '.webmanifest')
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('audio/mpeg', '.mp3')
mimetypes.add_type('image/x-icon', '.ico')

def get_local_ip():
    """Detect the machine's primary local network IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't send any traffic, just identifies outbound interface
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

class KalaSetuHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS and caching headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

def run_server():
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    port = 8080
    max_port = 8090
    server = None

    while port <= max_port:
        try:
            server = HTTPServer(('0.0.0.0', port), KalaSetuHandler)
            break
        except OSError:
            port += 1

    if not server:
        print("[!] Could not bind to any port between 8080 and 8090.")
        sys.exit(1)

    local_ip = get_local_ip()
    desktop_url = f"http://localhost:{port}/index.html"
    phone_url = f"http://{local_ip}:{port}/index.html"
    connect_url = f"http://localhost:{port}/connect.html?ip={local_ip}"

    print("=" * 68)
    print("      KalaSetu AI — Phone & Desktop Local App Server")
    print("=" * 68)
    print()
    print(f"  💻 Desktop App URL:  {desktop_url}")
    print(f"  📱 Phone App URL:    {phone_url}")
    print()
    print(f"  📲 Scan QR Code at:  {connect_url}")
    print()
    print("  * Ensure your phone is connected to the same Wi-Fi network.")
    print("  * On phone: Open the Phone URL -> tap menu -> 'Install' / 'Add to Home Screen'")
    print()
    print("  Press Ctrl+C in this window to stop the server.")
    print("=" * 68)
    print()

    # Open connection QR portal in browser
    try:
        webbrowser.open(connect_url)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped.")
        server.server_close()

if __name__ == '__main__':
    run_server()
