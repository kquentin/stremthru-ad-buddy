import json
import urllib.parse
from wsgiref.simple_server import make_server

import cache


def application(request, start_response):
    if request["REQUEST_METHOD"] == "GET":
        # GET /v0/store/magnet-cache/check?hash=...&hash=...
        query = request["QUERY_STRING"]
        parameters = urllib.parse.parse_qs(query)
        hashes = parameters["hash"]
        items = cache.check(hashes)
        payload = {"data": {"items": items}}
    else:
        # POST /v0/store/magnet-cache/track
        # read the body so the connection closes cleanly
        length = int(request["CONTENT_LENGTH"])
        request["wsgi.input"].read(length)
        payload = {"data": {}}
    body = json.dumps(payload).encode()
    start_response("200 OK", [])
    return [body]


server = make_server("0.0.0.0", 8080, application)
server.serve_forever()
