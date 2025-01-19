import socket
import threading

def receive_messages(client_socket):
    """Receive and display messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                print("[INFO] Server closed the connection.")
                break
        except Exception as e:
            print("[ERROR] Connection to server lost: {}".format(e))
            client_socket.close()
            break

def send_messages(client_socket):
    """Send user messages to the server."""
    while True:
        message = input()
        if message.lower() == "quit":
            client_socket.send(message.encode('utf-8'))
            client_socket.close()
            break
        else:
            client_socket.send(message.encode('utf-8'))

def start_client(server_ip, server_port):
    """Connect to the server and handle communication."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        print("[CONNECTED] Connected to server {}:{}".format(server_ip, server_port))
        
        # Start threads for sending and receiving messages
        thread_receive = threading.Thread(target=receive_messages, args=(client_socket,))
        thread_receive.start()

        send_messages(client_socket)
    except Exception as e:
        print("[ERROR] Unable to connect to server: {}".format(e))

if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"  # Use localhost for testing
    SERVER_PORT = 12355
    start_client(SERVER_IP, SERVER_PORT)
