import socket
import os
import threading
from config import *
from src.Metrics.RAM import *
from src.Metrics.CPU import *
from src.Metrics.DISK import *
from src.Metrics.NETWORK import *
from src.Metrics.CONNECTIONS import *

# Load token from config
TOKEN = SERVER_BIND_TOKEN

def handle_client(client_socket):
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break 

            token, command = request.split(' ', 1)

            if token != TOKEN:
                response = "Invalid token"
            elif command == 'cpu':
                response = get_cpu_metrics()
            elif command == 'ram':
                response = get_ram_metrics()
            elif command == 'network':
                response = get_network_metrics()
            elif command == 'disk':
                response = get_disk_metrics()
            elif command == 'conns':
                response = get_network_connections()
            else:
                response = "Unknown command"

            # Send the response with an end-of-message indicator
            client_socket.sendall((response + "\nEND_OF_MESSAGE\n").encode('utf-8'))
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_BIND_ADDR, int(SERVER_BIND_PORT)))
    server.listen(5)
    print(f"Server started on port {SERVER_BIND_PORT}")

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        server.close()