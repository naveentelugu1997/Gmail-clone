import http.server
import socketserver
from pathlib import Path

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'  # Serve index.html by default
        try:
            # Get the absolute path of the requested file
            file_path = Path(__file__).parent / self.path.lstrip('/')
            if file_path.is_file():  # Check if it's a file
                with open(file_path, 'rb') as file:
                    # Send the response header
                    self.send_response(200)
                    if self.path.endswith(".html"):
                        self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    # Send the file content
                    self.wfile.write(file.read())
            else:
                # Handle case where requested path is not a file
                raise FileNotFoundError

        except FileNotFoundError:
            self.send_error(404, 'File Not Found: %s' % self.path)

PORT = 8000
server = socketserver.TCPServer(("", PORT), MyHTTPRequestHandler)

print(f"Server started on port {PORT}")
server.serve_forever()