import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Map client socket -> nickname
clients_map = {}

def broadcast(message):
    """Send message (bytes) to all connected clients. Remove clients that error."""
    for client in list(clients_map.keys()):
        try:
            client.sendall(message)
        except Exception:
            # remove dead client
            try:
                clients_map.pop(client, None)
            except Exception:
                pass
            try:
                client.close()
            except Exception:
                pass


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                # client closed connection
                nickname = clients_map.get(client, 'Unknown')
                clients_map.pop(client, None)
                try:
                    client.close()
                except Exception:
                    pass
                broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                break

            nickname = clients_map.get(client, 'Unknown')
            try:
                text = message.decode('utf-8')
            except Exception:
                text = str(message)

            broadcast(f'{nickname}: {text}'.encode('utf-8'))
        except Exception:
            nickname = clients_map.get(client, 'Unknown')
            clients_map.pop(client, None)
            try:
                client.close()
            except Exception:
                pass
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        clients_map[client] = nickname

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('Server is listening...')
receive()