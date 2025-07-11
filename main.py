import socket       
import sys
from stun import get_ip_info

PORT = 8080

# Get the public IP address of this computer
def get_public_ip():
    nat_type, external_ip, external_port = get_ip_info()
    return external_ip

# Run this on the server computer
def run_server():
    # Show public IP
    public_ip = get_public_ip()
    print(f"[Server] Your public IP is: {public_ip}")
    print(f"[Server] Waiting for connection on port {PORT}...")

    # Create a TCP socket
    server_socket = socket.socket()
    # Bind to all network interfaces on the given port
    server_socket.bind(('', PORT))
    server_socket.listen(1)  # Wait for 1 client

    # Accept a connection
    connection, address = server_socket.accept()
    print(f"[Server] Connected to {address}")

    # Send and receive a message
    connection.send(b"Connection established (from server)")
    message = connection.recv(1024).decode()
    print("[Client]:", message)

    # Close everything
    connection.close()
    server_socket.close()

# Run this on the client computer
def run_client(server_ip):
    print(f"[Client] Connecting to server at {server_ip}:{PORT}...")

    # Create a TCP socket
    client_socket = socket.socket()
    client_socket.connect((server_ip, PORT))

    # Receive and send a message
    message = client_socket.recv(1024).decode()
    print("[Server]:", message)
    client_socket.send(b"Connection established (from client)")

    # Close connection
    client_socket.close()


if __name__ == "__main__":
    # Check how many arguments were passed
    if len(sys.argv) == 2 and sys.argv[1] == "server":
        run_server()
    elif len(sys.argv) == 3 and sys.argv[1] == "client":
        run_client(sys.argv[2])
    else:
        print("How to use:")
        print("  python main.py server           # To run as server")
        print("  python main.py client <IP>      # To run as client")
