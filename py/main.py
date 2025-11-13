from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import dispatcher

PORT = 8000

routes = {
    #GET
    "/": lambda: dispatcher.html("index.html"), # Use lambda to read file on-demand so changes update without restarting server
    "/CSS/style.css": lambda: dispatcher.css("style.css"),
    "/JS/properties.js": lambda: dispatcher.js("properties.js"),
    "/JS/acceleration.js": lambda: dispatcher.js("acceleration.js"),
    "/JS/space.js": lambda: dispatcher.js("space.js"),
    "/JS/gravity.js": lambda: dispatcher.js("gravity.js"),
    "/JS/entity.js": lambda: dispatcher.js("entity.js"),
    "/JS/system.js": lambda: dispatcher.js("system.js"),
    "/JS/inputsTable.js": lambda: dispatcher.js("inputsTable.js"),
    "/JS/script.js": lambda: dispatcher.js("script.js"),
    "/simulation/render": lambda: dispatcher.render(),
    "/simulation/clear": lambda: dispatcher.clear(),
    #GET
    #POST
    "/simulation/update": lambda data: dispatcher.update(data),
    "/simulation/add_entity": lambda data: dispatcher.addEntity(data)
    #POST
}

class catcher(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")  # allow browser requests
        self.end_headers()

    def do_GET(self):
        if self.path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
        elif self.path in routes:
            result, content_type = routes[self.path]()
            self._set_headers(content_type)
            if isinstance(result, dict):
                self.wfile.write(json.dumps(result).encode()) #if response contains JSON
            else:
                self.wfile.write(result.encode()) #if response contains html/css/js
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Not found".encode())

    def do_POST(self):
        if self.path in routes:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else None
            result, content_type = routes[self.path](data)
            self._set_headers(content_type)
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Not found.".encode())

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

server = HTTPServer(('127.0.0.1', PORT), catcher)
print(f"Server started on 127.0.0.1:8000 .")
server.serve_forever()

