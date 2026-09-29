import json
import os
import urllib.parse
import urllib.request

KEY = os.environ["ALLDEBRID_KEY"]


def call(path, parameters):
    address = "https://api.alldebrid.com/" + path
    body = urllib.parse.urlencode(parameters, doseq=True).encode()
    headers = {"Authorization": "Bearer " + KEY}
    request = urllib.request.Request(address, data=body, headers=headers)
    # urlopen honors the standard HTTPS_PROXY variable, for hosts whose IP is blocked
    connection = urllib.request.urlopen(request, timeout=30)
    response = json.load(connection)
    if response["status"] != "success":
        raise RuntimeError(response["error"])
    return response["data"]


def library_hashes():
    data = call("v4.1/magnet/status", {})
    hashes = set()
    for magnet in data["magnets"]:
        hashes.add(magnet["hash"])
    return hashes


def upload(hashes):
    data = call("v4/magnet/upload", {"magnets[]": hashes})
    return data["magnets"]


def files(magnet_ids):
    # answers MAGNET_INVALID_ID when called without any id
    if len(magnet_ids) == 0:
        return []
    data = call("v4/magnet/files", {"id[]": magnet_ids})
    return data["magnets"]


def delete(magnet_ids):
    # answers MAGNET_INVALID_ID when called without any id
    if len(magnet_ids) == 0:
        return
    call("v4/magnet/delete", {"ids[]": magnet_ids})
