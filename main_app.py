from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote_plus
import mimetypes
from pathlib import Path
import json


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # print(f"{self.headers.get('Content-Length') = }")
        data = self.rfile.read(int(self.headers.get('Content-Length')))
        self.save_to_json(data)
        print(f"{unquote_plus(data.decode()) = }")
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        
    def do_GET(self):
        url = urlparse(self.path)
        match url.path:
            case '/':
                self.send_html("index.html")
            case '/contacts':
                self.send_html("contacts.html")
            case '/message':
                self.send_html("send_message.html")
            case _:
                file_path = Path(url.path[1:])
                if file_path.exists():
                    self.send_static(str(file_path))
                else:
                    self.send_html("error.html", 404)
                
    def send_static(self, static_filename):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        # print(f"{mt = }")
        if mt:
            self.send_header('Content-type', mt[0])
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(static_filename, 'rb') as f:
            self.wfile.write(f.read())

    def send_html(self, html_filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(html_filename, 'rb') as f:
            self.wfile.write(f.read())

    def save_to_json(self, raw_data):
        data = unquote_plus(raw_data.decode())
        dict_data = {key: value for key, value in [el.split("=") for el in data.split("&")]}
        print(dict_data)
        with open("data/data.json", "w", encoding="utf-8") as f:
            json.dump(dict_data, f)
        
def run(server_class=HTTPServer, handler_class=HttpGetHandler):
    server_address = ('', 8000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
