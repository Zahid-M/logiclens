"""
Mesocosm adapter for LogicLens.
Run with: python adapter.py
Health check: http://localhost:8765/health
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import traceback
from env import LogicLensEnv

PORT = 8765
_envs: dict[str, LogicLensEnv] = {}


def _json(data) -> bytes:
    return json.dumps(data).encode()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # silence default access log

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def _send(self, code: int, data: dict):
        body = _json(data)
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "ok", "env": "logiclens"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        try:
            body = self._read_body()
            if self.path == "/reset":
                seed = body.get("seed", 0)
                episode_id = body.get("episode_id", str(seed))
                env = LogicLensEnv(seed=seed)
                _envs[episode_id] = env
                obs = env.reset()
                self._send(200, obs)

            elif self.path == "/step":
                episode_id = body.get("episode_id", "0")
                action = body.get("action", "")
                env = _envs.get(episode_id)
                if env is None:
                    self._send(400, {"error": "unknown episode_id"})
                    return
                result = env.step(action)
                self._send(200, result)

            else:
                self._send(404, {"error": "unknown endpoint"})

        except Exception:
            self._send(500, {"error": traceback.format_exc()})


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"LogicLens adapter running on http://localhost:{PORT}")
    print(f"Health: http://localhost:{PORT}/health")
    server.serve_forever()
