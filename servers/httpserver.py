#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = ""
hostPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(f"<p>You accessed path: {self.path}</p>\n", "utf-8"))
        self.log()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        self.send_response(200)
        self.end_headers()
        self.log(post_data.decode())

    do_PUT = do_POST

    def log(self, data=None):
        for header, value in self.headers.items():
            print(f"{header}: {value}")
        if data:
            print()
            print(data)
        print()


myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
