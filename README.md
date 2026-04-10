# CN Project — SSL Secure Remote Shell

A client-server application that establishes an SSL-encrypted connection, authenticates users, and allows remote command execution with performance metrics (latency, response time, throughput).

---

## Requirements

- Python 3.x (standard library only — no extra packages needed)
- `server.crt` and `server.key` must be present in the same directory as `server.py`

---

## Running the Server

```bash
python server.py
```

The server listens on **port 5000** by default.  
Make sure `server.crt` and `server.key` are in the same directory.

### Default credentials

| Username | Password     |
|----------|-------------|
| admin    | password123 |
| user     | test123     |

---

## Running the Client

Before starting the client, update the `HOST` variable in `client.py` to match the server's IP address:

```python
HOST = "192.168.137.1"   # Replace with the server's IP
```

Then run:

```bash
python client.py
```

You will be prompted for your username and password. After successful authentication, you can enter shell commands to execute remotely. Type `exit` to quit.

---

## Project Structure

```
cn proj/
├── server.py      # SSL server with authentication and command execution
├── client.py      # SSL client with login and interactive command prompt
├── server.crt     # SSL certificate (self-signed)
├── server.key     # SSL private key
└── README.md      # This file
```

---

## Notes

- The client skips hostname and certificate verification (`CERT_NONE`) — suitable for local/lab use only.
- Performance metrics (latency, response time, throughput) are printed to the console on both sides.
- To regenerate the SSL certificate and key:

```bash
openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt -days 365 -nodes
```
