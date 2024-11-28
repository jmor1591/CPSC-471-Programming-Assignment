Author: Jordan Morris

Language: Python

# Simple FTP Client-Server Application

A Python-based FTP (File Transfer Protocol) application that facilitates file transfers between a client and a server using sockets. The project demonstrates the fundamental concepts of client-server architecture, multithreading, and network communication.

---

## Features

- **File Transfer Operations**: 
  - Upload (`put`) files from client to server.
  - Download (`get`) files from server to client.
  - List (`ls`) available files on the server.
  - Disconnect (`quit`) the client from the server.

- **Control and Data Channels**:
  - Utilizes separate control and data connections for efficient communication.
  - Dynamically assigns ephemeral ports for data transfer.

- **Multithreading**:
  - The server can handle multiple clients concurrently using threads.

---

## Requirements

- **Python Version**: Python 3.8 or higher
- **Libraries Used**:
  - `socket`
  - `os`
  - `threading`

---

## Setup and Configuration

### Server
1. Open `serv.py`.
2. Ensure the desired server IP (`0.0.0.0` by default) and port (`2121` by default) are set.
3. Run the server:
   ```bash
   cd server_side
   python serv.py


### Client
1. Open cli.py.
2. Configure the server IP (default: 127.0.0.1 for localhost) and port (2121).
3. Run the server:
   ```bash
   python serv.py

## Usage
Commands
ls: List files in the server's working directory.
get <filename>: Download a file from the server to the client.
put <filename>: Upload a file from the client to the server.
quit: Disconnect from the server and exit the client.

ftp> ls
Files on server:
file1.txt
file2.txt
ftp> get file1.txt
File file1.txt downloaded successfully.
ftp> put file3.txt
File file3.txt uploaded successfully.
ftp> quit

## Project Structure
serv.py: Server-side script to handle client connections, commands, and file transfers.
cli.py: Client-side script to send commands, interact with the server, and perform file transfers.