import sys
import requests
import os

def put(local_path, remote_path, metadata_url):
    if not os.path.exists(local_path):
        print("Local file not found")
        return

    with open(local_path, "rb") as f:
        data = f.read()

    # Ask metadata for block allocation
    resp = requests.post(
        f"{metadata_url}/allocate",
        json={"path": remote_path}
    )

    if resp.status_code != 200:
        print("Metadata allocation error:", resp.text)
        return

    info = resp.json()
    block_id = info["block_id"]
    servers = info["servers"]

    print("Uploading block:", block_id, "to servers:", servers)

    # Upload block to all assigned chunkservers
    for s in servers:
        try:
            upload_url = f"{s}/upload/{block_id}"
            up = requests.post(upload_url, data=data)
            print("Uploaded to:", s, "| Status:", up.status_code)
        except Exception as e:
            print("Failed to upload to:", s, "| Error:", e)

def get(remote_path, output_path, metadata_url):
    resp = requests.post(
        f"{metadata_url}/locations",
        json={"path": remote_path}
    )

    if resp.status_code != 200:
        print("File not found:", resp.text)
        return

    locations = resp.json()
    for block_id, servers in locations.items():
        print("Trying to download block:", block_id)

        for s in servers:
            try:
                download_url = f"{s}/download/{block_id}"
                r = requests.get(download_url)

                if r.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(r.content)

                    print("Downloaded from:", s)
                    return

            except Exception:
                continue

        print("Failed to download block:", block_id)

def usage():
    print("Usage:")
    print("python client.py put <local_path> <remote_path> <metadata_url>")
    print("python client.py get <remote_path> <output_path> <metadata_url>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "put" and len(sys.argv) == 5:
        put(sys.argv[2], sys.argv[3], sys.argv[4])

    elif cmd == "get" and len(sys.argv) == 5:
        get(sys.argv[2], sys.argv[3], sys.argv[4])

    else:
        usage()
