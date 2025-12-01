from flask import Flask, request, jsonify
import os
import json
import uuid

app = Flask(__name__)
DATA_FILE = "metadata_store.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"chunkservers": [], "files": {}, "blocks": {}}, f)

def read_store():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_store(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@app.route("/register", methods=["POST"])
def register():
    req = request.get_json()
    url = req.get("url")
    if not url:
        return jsonify({"error": "no url"}), 400
    store = read_store()
    if url not in store["chunkservers"]:
        store["chunkservers"].append(url)
        write_store(store)
    return jsonify({"status": "ok", "chunkservers": store["chunkservers"]})

@app.route("/allocate", methods=["POST"])
def allocate():
    req = request.get_json()
    path = req.get("path")
    if not path:
        return jsonify({"error": "no path"}), 400
    store = read_store()
    block_id = str(uuid.uuid4())
    servers = store["chunkservers"][:2]
    if not servers:
        return jsonify({"error": "no chunkservers registered"}), 500
    store["blocks"][block_id] = servers
    store["files"][path] = [block_id]
    write_store(store)
    return jsonify({"block_id": block_id, "servers": servers})

@app.route("/locations", methods=["POST"])
def locations():
    req = request.get_json()
    path = req.get("path")
    store = read_store()
    block_ids = store["files"].get(path)
    if not block_ids:
        return jsonify({"error": "file not found"}), 404
    result = {}
    for b in block_ids:
        result[b] = store["blocks"].get(b, [])
    return jsonify(result)

@app.route("/status", methods=["GET"])
def status():
    return jsonify(read_store())

if __name__ == "__main__":
    app.run(port=5000)
