"""Local static preview with production-style extensionless HTML routes."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import os
ROOT = Path(__file__).resolve().parent.parent
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        candidate = Path(self.translate_path(path))
        if not candidate.exists() and not candidate.suffix and candidate.with_suffix('.html').is_file():
            self.path = path + '.html'
        super().do_GET()
os.chdir(ROOT)
print('Preview: http://localhost:4173', flush=True)
ThreadingHTTPServer(('127.0.0.1', 4173), Handler).serve_forever()
