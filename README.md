# Distributed File System (DFS) with Fault Tolerance

This project implements a simple Distributed File System (DFS) designed to ensure **data availability**, **replication**, and **fault tolerance** across multiple nodes.  
It demonstrates key operating system concepts such as distributed storage, metadata management, and recovery.

---

## 📌 Project Features

- Centralized **Metadata Server** (tracks files, blocks, and chunkserver locations)
- Multiple **Chunkservers** (store replicated blocks)
- **Client** program for uploading and downloading files
- **Replication factor = 2** (each block is stored on 2 chunkservers)
- **Fault Tolerance**: If one server goes down, the other can still serve the file
- Simple **HTTP-based architecture** using Flask

---

# 📁 Project Structure

```
dfs/
│
├── metadata.py        # Metadata manager (file/block mapping)
├── chunkserver.py     # Node that stores blocks
├── client.py          # Tool for upload/download
├── sample.txt         # Sample test file
├── .gitignore         # Ignore cache folders
└── README.md          # Documentation
```

---

# 🚀 How It Works (High-Level)

1. **Client uploads a file**  
   - Metadata server allocates a block and chooses 2 chunkservers  
   - Client uploads the block to both chunkservers

2. **Client downloads a file**  
   - Metadata server returns the block → server list  
   - Client downloads the block from ANY available server  
   - If one server is down, it tries the other (fault tolerance)

3. **Chunkservers register** automatically with the metadata server at startup.

---

# ⚙️ Setup Instructions

## 1️⃣ Install Dependencies
You need Python 3 and Flask/Requests:


pip install flask requests

or (Linux):

pip3 install flask requests

---

# 🧠 Run Instructions

## 2️⃣ Start the Metadata Server
python metadata.py
Runs on port **5000**.

---

## 3️⃣ Start Chunkservers  
Open **two terminals**:

python chunkserver.py 6001
python chunkserver.py 6002

Both will auto-register with the metadata manager.

---

## 4️⃣ Upload a File (PUT)
python client.py put sample.txt /remote/sample.txt http://127.0.0.1:5000

---

## 5️⃣ Download a File (GET)
python client.py get /remote/sample.txt downloaded.txt http://127.0.0.1:5000

If one server fails, download still works from the replica.

---

# 🧪 Example Workflow

1. Start metadata  
2. Start 2 chunkservers  
3. Upload sample.txt  
4. Shutdown server 6001  
5. Try downloading → still succeeds because of replication

---

# ✨ Completed Requirements

- Metadata Manager  
- Chunkservers with block storage  
- Client with PUT/GET  
- Replication factor 2  
- Fault-tolerant download  
- GitHub repo with 7+ commits  
- Branch-based workflow & PRs  
- Appendix A/B/C ready for report  

---

# 👨‍💻 Author
**Swaroop J**  
School of Computer Science & Engineering  
Lovely Professional University

---

Updated on 2 December 2025

