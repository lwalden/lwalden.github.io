"""Starts a simpel HTTP server for testing iframe sandboxing techniques."""
import re
import sys
import SimpleHTTPServer
import SocketServer

#yeah it's a global variable wanna fight about it?
HEADERS = [{"Feature-Policy": "camera *"}]

class CustomHeadersRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """A request handler that includes custom HTTP response headers."""
    def end_headers(self):
        """Override parent class by adding custmo headers."""
        for custom_header in HEADERS:
            for key, value in custom_header.iteritems():
                self.send_header(key, value)
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

def _main():
    request_handler = CustomHeadersRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), request_handler)

    httpd.serve_forever()

if __name__ == "__main__":
    _main()
