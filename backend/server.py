from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import json
import base64
from urllib.parse import parse_qs, urlparse


class RequestHandler(BaseHTTPRequestHandler):
    key = base64.b64encode(
            bytes('%s:%s' % ("admin", "1234"), 'utf-8')).decode('ascii')

    def do_HEAD(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(HTTPStatus.UNAUTHORIZED)
        self.send_header("WWW-Authenticate", 'Basic realm="Demo Realm"')
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        """Present frontpage with user authentication."""
        if self.headers.get("Authorization") is None:
            self.do_AUTHHEAD()

            response = {"success": False, "error": "No auth header received"}

            self.wfile.write(bytes(json.dumps(response), "utf-8"))

        elif self.headers.get("Authorization") == "Basic " + RequestHandler.key:
            print(self.headers.get("Authorization"))

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            getvars = self._parse_GET()

            base_path = urlparse(self.path).path

            response = {"path": self.path, "get_vars": str(getvars)}
            self.wfile.write(bytes(json.dumps(response), "utf-8"))

        else:
            print(self.headers.get("Authorization"))

            self.do_AUTHHEAD()

            response = {"success": False, "error": "Invalid credentials"}

            self.wfile.write(bytes(json.dumps(response), "utf-8"))

    def do_POST(self):
        pass

    def _parse_GET(self):
        getvars = parse_qs(urlparse(self.path).query)

        return getvars


server_address = ("localhost", 8000)
server = HTTPServer(server_address, RequestHandler)

server.serve_forever()
