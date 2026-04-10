import socket
import ssl
import threading
import subprocess
import time

HOST = "0.0.0.0"
PORT = 5000

users = {
    "admin": "password123",
    "user": "test123"
}

def authenticate(conn):
    try:
        conn.send(b"USERNAME: ")
        username = conn.recv(1024).decode().strip()

        conn.send(b"PASSWORD: ")
        password = conn.recv(1024).decode().strip()

        if username in users and users[username] == password:
            conn.send(b"AUTH_SUCCESS\n")
            return True
        else:
            conn.send(b"AUTH_FAILED\n")
            return False
    except:
        return False


def handle_client(conn, addr):
    print(f"[+] Connected {addr}")

    total_bytes = 0
    start_time = time.time()

    try:
        if not authenticate(conn):
            print(f"[-] Authentication failed {addr}")
            conn.close()
            return

        conn.send(b"Enter commands (exit to quit)\n")

        while True:
            conn.send(b"> ")

            try:
                recv_start = time.time()
                data = conn.recv(1024)

                if not data:
                    print(f"[!] Client {addr} disconnected abruptly")
                    break

                recv_end = time.time()

                command = data.decode().strip()
                total_bytes += len(data)

                latency = recv_end - recv_start
                print(f"[Latency {addr}: {latency:.4f}s]")

                if command.lower() == "exit":
                    break

                exec_start = time.time()

                try:
                    output = subprocess.check_output(
                        command,
                        shell=True,
                        stderr=subprocess.STDOUT
                    )
                except subprocess.CalledProcessError as e:
                    output = e.output
                except Exception as e:
                    output = str(e).encode()

                exec_end = time.time()

                response_time = exec_end - exec_start
                print(f"[Response Time {addr}: {response_time:.4f}s]")

                conn.send(output)
                total_bytes += len(output)

            except (ConnectionResetError, BrokenPipeError):
                print(f"[!] Connection lost with {addr}")
                break

    finally:
        end_time = time.time()
        duration = end_time - start_time

        if duration > 0:
            throughput = total_bytes / duration
            print(f"[Throughput {addr}: {throughput:.2f} bytes/sec]")

        conn.close()
        print(f"[-] Disconnected {addr}")


context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("server.crt", "server.key")

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(5)

print("Server running on port", PORT)

secure_sock = context.wrap_socket(sock, server_side=True)

while True:
    try:
        client, addr = secure_sock.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()
    except Exception as e:
        print("[!] Accept error:", e)