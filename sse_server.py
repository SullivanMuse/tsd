import http.server
import socketserver
import json
import random
import time
from urllib.parse import urlparse, parse_qs

# Global variables to store the latest data point for each category
categories = ["Category A", "Category B", "Category C"]
latest_data = {category: {"id": 0, "x": 0, "y": 0} for category in categories}

class SSEHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            while True:
                for category in categories:
                    data = self.generate_data(category)
                    self.wfile.write(f"data: {json.dumps(data)}\n\n".encode())
                    self.wfile.flush()
                time.sleep(1)  # Send data every second
        else:
            return super().do_GET()

    def generate_data(self, category):
        latest = latest_data[category]
        new_id = latest["id"] + 1
        new_x = latest["x"] + 1
        new_y = latest["y"] + random.uniform(-1, 1)

        new_point = {"id": new_id, "x": new_x, "y": new_y}
        latest_data[category] = new_point

        return {
            "category": category,
            "points": [new_point]
        }

if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(("", PORT), SSEHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()