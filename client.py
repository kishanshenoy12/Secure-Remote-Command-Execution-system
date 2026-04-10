import socket
import ssl
import getpass
import time

HOST = "192.168.137.1"
PORT = 5000

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket()
secure_sock = context.wrap_socket(sock, server_hostname=HOST)

# Performance metrics
total_bytes = 0
start_time = time.time()

try:
    secure_sock.connect((HOST, PORT))

    while True:
        try:
            recv_start = time.time()
            data = secure_sock.recv(4096)

            if not data:
                print("\n[!] Server disconnected abruptly")
                break

            recv_end = time.time()

            decoded = data.decode()
            print(decoded, end="")

            total_bytes += len(data)

            # Latency
            latency = recv_end - recv_start
            print(f"\n[Latency: {latency:.4f}s]")

            # Hide password input
            if "PASSWORD" in decoded:
                command = getpass.getpass("")
            else:
                command = input()

            send_start = time.time()
            secure_sock.send(command.encode())
            send_end = time.time()

            # Response time
            response_time = send_end - send_start
            print(f"[Response Time: {response_time:.4f}s]")

            if command.lower() == "exit":
                break

        except (ConnectionResetError, BrokenPipeError):
            print("\n[!] Connection lost unexpectedly")
            break

except Exception as e:
    print("Error:", e)

finally:
    end_time = time.time()
    duration = end_time - start_time

    # Throughput
    if duration > 0:
        throughput = total_bytes / duration
        print(f"\n[Throughput: {throughput:.2f} bytes/sec]")

    secure_sock.close()