import sys
from flask import Flask, request, send_file, jsonify
import os
import requests

# Get port from command-line argument
if len(sys.argv) < 2:
    print("Usage: python chunkserver.py <port>")
    sys.exit(1)

port = int(sys.argv[1])
app = Flask(__name__)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

METADATA_URL = "http://127.0.0.1:5000"

@app.route("/upload/<block_id>", methods=["POST"])
def upload(block_id):
    data = request.get_data()
    filepath = os.path.join(DATA_DIR, block_id)

    with open(filepath, "wb") as f:
        f.write(data)

    return jsonify({"status": "stored", "block": block_id})

@app.route("/download/<block_id>", methods=["GET"])
def download(block_id):
    filepath = os.path.join(DATA_DIR, block_id)

    if not os.path.exists(filepath):
        return jsonify({"error": "block not found"}), 404

    return send_file(filepath, as_attachment=True)

@app.route("/list", methods=["GET"])
def list_blocks():
    return jsonify(os.listdir(DATA_DIR))

def register_with_metadata():
    url = f"http://127.0.0.1:{port}"
    try:
        requests.post(f"{METADATA_URL}/register", json={"url": url}, timeout=2)
    except:
        pass

if __name__ == "__main__":
    register_with_metadata()
    app.run(port=port)
