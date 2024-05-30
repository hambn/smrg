import socket
from config import *

TOKEN = CLIENT_CONNECT_TOKEN

def Client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((CLIENT_CONNECT_ADDR, int(CLIENT_CONNECT_PORT)))
        return client_socket
    except Exception as e:
        print(f"Failed to create or connect socket: {e}")
        return None

def receive_full_response(client_socket):
    response = ""
    while True:
        part = client_socket.recv(1024).decode('utf-8')
        response += part
        if "END_OF_MESSAGE" in part:
            response = response.replace("END_OF_MESSAGE", "").strip()
            break
    return response

def start_client():
    try:
        client_socket = Client()  # Initialize the client socket

        while True:
            command = input("Enter command (GET_CPU to get CPU usage): ")
            message = f"{TOKEN} {command}"
            client_socket.sendall(message.encode('utf-8'))
            response = receive_full_response(client_socket)
            print("Response from server:", response)
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        if client_socket:
            client_socket.close()
        
