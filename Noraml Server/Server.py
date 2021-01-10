from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote as urlparse
import subprocess

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        
        request_id = urlparse(self.path)
        try:
            response=open('./'+request_id,'r').read()
            self._set_headers()
        except:
            response="404 Not Found"
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
        self.wfile.write(response.encode())

    def do_POST(self):
        self._set_headers()
        request_id = urlparse(self.path)
        response = self.raw_requestline
        length = int(self.headers.get('content-length'))
        parms=self.rfile.read(length).decode().split('=')
        print(parms)
        retu=b"Failed"
        if open("./"+request_id,'w').write(parms[1]):
            retu=b"Done"
        self.wfile.write(retu)

    def do_HEAD(self):
        self._set_headers()

def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
