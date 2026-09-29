import alldebrid


# tells which magnets are cached. AllDebrid has no endpoint for that anymore.
# magnets are uploaded to read their `ready` flag, then the ones we added are deleted.
def check(hashes):
    library = alldebrid.library_hashes()
    uploaded = alldebrid.upload(hashes)

    ready_hash_by_id = {}
    added_ids = []
    for magnet in uploaded:
        if "error" in magnet:
            continue
        magnet_id = magnet["id"]
        magnet_hash = magnet["hash"]
        if magnet["ready"]:
            ready_hash_by_id[magnet_id] = magnet_hash
        # a magnet that was already in the library is never deleted
        if magnet_hash not in library:
            added_ids.append(magnet_id)

    files_by_hash = {}
    ready_ids = list(ready_hash_by_id)
    for magnet in alldebrid.files(ready_ids):
        # magnet/files returns the id as a string
        magnet_id = int(magnet["id"])
        magnet_hash = ready_hash_by_id[magnet_id]
        tree = magnet["files"]
        files_by_hash[magnet_hash] = flatten(tree)

    alldebrid.delete(added_ids)

    items = []
    for magnet_hash in hashes:
        if magnet_hash in files_by_hash:
            files = files_by_hash[magnet_hash]
            item = {"hash": magnet_hash, "status": "cached", "files": files}
        else:
            item = {"hash": magnet_hash, "status": "unknown"}
        items.append(item)
    return items


# AllDebrid gives the files as a tree of folders, StremThru wants a flat list of files:
#   [{"n": "Season 1", "e": [{"n": "E01.mkv", "s": 700}]}]  ->  [{"i": -1, "n": "E01.mkv", "s": 700}]
# Index -1 means unknown. Comet then chooses the file to play by its name.
def flatten(nodes):
    files = []
    for node in nodes:
        name = node["n"]
        if "e" in node:
            folder_content = node["e"]
            folder_files = flatten(folder_content)
            files = files + folder_files
        else:
            size = node["s"]
            file = {"i": -1, "n": name, "s": size}
            files.append(file)
    return files
