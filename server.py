"""Starts a simpel HTTP server for testing iframe sandboxing techniques."""
import re
import sys
import SimpleHTTPServer
import SocketServer

PARENT_DOMAIN = 'all.i.do.is.win'
VULNERABLE_DOMAIN = 'you.cannot.win'

PORT = 9337

#yeah it's a global variable wanna fight about it?
HEADERS = [{"Feature-Policy": "midi *; microphone *; fullscreen *; encrypted-media *; document-domain *; display-capture *; camera *"}]

class CustomHeadersRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """A request handler that includes custom HTTP response headers."""
    def end_headers(self):
        """Override parent class by adding custmo headers."""
        for custom_header in HEADERS:
            for key, value in custom_header.iteritems():
                self.send_header(key, value)
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

def _main():
    if not hosts_file_ok():
        sys.exit("Hosts file is missing required definitions.")

    request_handler = CustomHeadersRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), request_handler)

    print "Started HTTP server on port %d using custom headers:" % PORT
    for header in HEADERS:
        for key, value in header.iteritems():
            print "\t%s: %s" % (key, value)
    httpd.serve_forever()

def hosts_file_ok():
    """Deterimnes whether desired domains are defined in /etc/hosts"""
    with open('/etc/hosts', 'r') as hosts:
        contents = hosts.read()
        return (_domain_in_str(PARENT_DOMAIN, contents) and
                _domain_in_str(VULNERABLE_DOMAIN, contents))

def _domain_in_str(domain, string):
    regex = r"^\s*127\.0\.0\.1\s+%s\s*$" % re.escape(domain)
    matches = re.search(regex,
                        string,
                        re.MULTILINE)
    return matches is not None

if __name__ == "__main__":
    _main()
