import threading
import json

class SSE:
   def __init__(self, handler = None):
      self.handler = handler
      self.lock = threading.Lock()

   def write(self, payload):
      if not self.handler:
         raise RuntimeError("SSE Handler is undefined")

      try:
         data = f"data: {json.dumps(payload)}\n\n".encode()
         with self.lock:
            self.handler.wfile.write(data)

      except Exception:
         self.close()
         raise RuntimeError("SSE Disconnected")

   def close(self):
      if not self.handler:
         return
      self.handler = None
