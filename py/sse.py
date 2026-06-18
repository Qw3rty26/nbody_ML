import threading
import json

class SSE:
   def __init__(self, handler = None):
      self.handler = handler
      self.handler.wfile.write(b"data: connected\n\n")
      self.handler.wfile.flush()

   def write(self, payload):
      if not self.handler:
         return False
      try:
         self.handler.wfile.write( # write into the stream
            f"data: {json.dumps(payload)}\n\n".encode()
         )
         self.handler.wfile.flush()
         return True

      except (BrokenPipeError, ConnectionResetError, OSError):
         print("SSE client disconnected")
         self.handler = None
         return False
