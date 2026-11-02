from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def make_server(folder=None, port=0):
    handler = partial(SimpleHTTPRequestHandler, directory=Path(__file__).with_name("public"))
    return ThreadingHTTPServer(("127.0.0.1", port), handler)


if __name__ == "__main__":
    with make_server(port=8000) as app:
        app.serve_forever()
