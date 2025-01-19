import socket
import threading

# Global list to store connected clients
clients = []

def broadcast(message, sender_socket=None):
    """Relay messages to all clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except Exception:
                clients.remove(client)

def handle_client(client_socket, client_address):
    """Handle communication with a connected client."""
    print("[NEW CONNECTION] {} connected.".format(client_address))
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == "quit":
                print("[DISCONNECT] {} disconnected.".format(client_address))
                clients.remove(client_socket)
                client_socket.close()
                broadcast("[INFO] {} left the chat.".format(client_address).encode())
                break
                
            else:
                print("[{}] {}".format(client_address, message))
                broadcast(message, sender_socket=client_socket)
        except Exception as e:
            print("[ERROR] Connection with {} lost: {}".format(client_address, e))
            clients.remove(client_socket)
            client_socket.close()
            break


def start_server(server_ip, server_port):
    """Start the server and accept incoming connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print("[SERVER STARTED] Listening on {}:{}".format(server_ip, server_port))

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        broadcast("[INFO] {} joined the chat.".format(client_address).encode())
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print("[ACTIVE CONNECTIONS] {}".format(len(clients)))

if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"  # Use localhost for testing
    SERVER_PORT = 12355
    start_server(SERVER_IP, SERVER_PORT)
