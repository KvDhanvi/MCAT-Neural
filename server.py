"""
Run with: python server.py
Then open: http://localhost:3000
"""
import http.server, json, urllib.request, urllib.error, os

PORT = int(os.environ.get('PORT', 3000))
DIR  = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=DIR, **kw)

    def log_message(self, fmt, *args):
        print(fmt % args)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path != '/api/chat':
            self.send_error(404)
            return
        length  = int(self.headers.get('Content-Length', 0))
        body    = self.rfile.read(length)
        auth    = self.headers.get('Authorization', '')
        req = urllib.request.Request(
            'https://integrate.api.nvidia.com/v1/chat/completions',
            data=body,
            headers={'Content-Type': 'application/json', 'Authorization': auth},
            method='POST'
        )
        try:
            with urllib.request.urlopen(req) as r:
                data = r.read()
                self.send_response(r.status)
                self._cors()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            data = e.read()
            self.send_response(e.code)
            self._cors()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(data)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin',  '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

with http.server.HTTPServer(('', PORT), Handler) as srv:
    print(f'MCAT//NEURAL running → http://localhost:{PORT}')
    print('Press Ctrl+C to stop.')
    srv.serve_forever()
