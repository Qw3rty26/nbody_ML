from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import dispatcher
import threading

PORT = 8000

GET_ROUTES = {
   "/":                                lambda: dispatcher.html("index.html"),          # Use lambda to read file on-demand so changes update

   "/CSS/style.css":                   lambda: dispatcher.css("style.css"),            # without restarting server

   "/JS/properties.js":                lambda: dispatcher.js("properties.js"),
   "/JS/acceleration.js":              lambda: dispatcher.js("acceleration.js"),
   "/JS/space.js":                     lambda: dispatcher.js("space.js"),
   "/JS/gravity.js":                   lambda: dispatcher.js("gravity.js"),
   "/JS/entity.js":                    lambda: dispatcher.js("entity.js"),
   "/JS/system.js":                    lambda: dispatcher.js("system.js"),
   "/JS/inputsTable.js":               lambda: dispatcher.js("inputsTable.js"),
   "/JS/script.js":                    lambda: dispatcher.js("script.js"),
   "/JS/mouseActions.js":              lambda: dispatcher.js("mouseActions.js"),

   "/networking/disconnectSSE":        lambda: dispatcher.disconnect_sse(),

   "/simulation/createPhysicsLoop":    lambda: dispatcher.create_physics_loop(),
   "/simulation/destroyPhysicsLoop":   lambda: dispatcher.destroy_physics_loop(),
   "/simulation/startPhysicsLoop":     lambda: dispatcher.start_physics_loop(),
   "/simulation/pausePhysicsLoop":     lambda: dispatcher.pause_physics_loop(),
   "/simulation/clearSystem":          lambda: dispatcher.clear_system(),
}

POST_ROUTES = {
   "/simulation/addEntity":            lambda data: dispatcher.add_entity(data),
   "/simulation/removeEntity":         lambda data: dispatcher.remove_entity(data)
}


class catcher(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")  # allow browser requests
        self.end_headers()

    def _set_headers_SSE(self):
        self.send_response(200)
        self.send_header("Content-type", "text/event-stream")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()

    def do_GET(self):
        if self.path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
                return
        elif self.path == "/networking/connectSSE":  #establish an SSE connection to constantly stream entity data to client-side
                self._set_headers_SSE()
                dispatcher.connect_sse(self)
                return
        elif self.path in GET_ROUTES:
            result, content_type = GET_ROUTES[self.path]()
            self._set_headers(content_type)
            if isinstance(result, dict):
                try:
                   self.wfile.write(json.dumps(result).encode()) #if response contains JSON
                except (BrokenPipeError, ConnectionResetError):
                   return
            else:
                self.wfile.write(result.encode()) #if response contains html/css/js
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"Not found")

    def do_POST(self):
        if self.path in POST_ROUTES:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else None
            result, content_type = POST_ROUTES[self.path](data)
            self._set_headers(content_type)
            try:
               self.wfile.write(json.dumps(result).encode()) #if response contains JSON
            except (BrokenPipeError, ConnectionResetError):
               return
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

server = ThreadingHTTPServer(('127.0.0.1', PORT), catcher)
print(f"Server started on 127.0.0.1:8000 .")

try:
   server.serve_forever()
except KeyboardInterrupt:
   print("Shutting down...")
   dispatcher.system.destroy_physics_loop()
   dispatcher.system.disconnect_sse()
   server.shutdown()
   server.server_close()
