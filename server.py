#!/usr/bin/env python3

"""
Simple web server


Usage:
    ./server.py [<port>]
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import argv
from urllib.parse import parse_qs


class SimpleWebServer(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        # endpoints that clients can request
        self.endpoints = {"/": self.index, "/formsubmit": self.greet}

        super().__init__(request, client_address, server)

    def _set_headers(self, response_code, content_type="text/html"):
        self.send_response(response_code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        try:
            self.endpoints[self.path]()
        except KeyError:
            self.not_found()

    def do_HEAD(self):
        self._set_headers(200)

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        # Parse the POST data into a dictionary
        data_dict = parse_qs(post_data)

        try:
            self.endpoints[self.path](data_dict)
        # Catching 'TypeError' if a POST request is sent to a function intended
        # for GET requests only
        except (KeyError, TypeError):
            self.not_found()

    def not_found(self):
        """404 page for when a client requests an endpoint that doesn't exist"""
        self._set_headers(404)

        self.wfile.write(
            bytes("<html><head><title>Simple Web Server - 404</title></head>", "utf-8")
        )
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<h1>404</h1>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<p>This endpoint was not configured</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def greet(self, data_dict=False):
        if not data_dict:
            return self.not_found()

        name = data_dict[b"name"][0].decode("utf-8")

        self._set_headers(200)
        self.wfile.write(
            bytes(
                "<html><head><title>Simple Web Server - Hello</title></head>", "utf-8"
            )
        )
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Hello %s</p>" % name, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def index(self):
        self._set_headers(200)
        self.wfile.write(
            bytes(
                "<html><head><title>Simple Web Server - Index</title></head>", "utf-8"
            )
        )
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Please enter your name:</p>", "utf-8"))
        self.wfile.write(
            bytes(
                """<form action='/formsubmit' method='post'>
                    <input name='name'>
                    <input type='submit' value='Send'>
                    </form>""",
                "utf-8",
            )
        )
        self.wfile.write(bytes("</body></html>", "utf-8"))


def run(port=8080):
    httpd = HTTPServer(("", port), SimpleWebServer)
    print("httpd started on port %s" % (port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("httpd stopped\n")


if __name__ == "__main__":
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
