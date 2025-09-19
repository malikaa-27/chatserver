import socket
import threading

HOST = '127.0.0.1'
PORT = 12345


def receive(client_sock):
    while True:
        try:
            message = client_sock.recv(1024)
            if not message:
                print('Connection closed by server')
                break
            # Server may send control messages like 'NICK' or chat text
            print(message.decode('utf-8'))
        except Exception as e:
            print('Error receiving:', e)
            break


def write(client_sock):
    while True:
        try:
            text = input()
            if not text:
                continue
            client_sock.send(text.encode('utf-8'))
            if text.lower() == '/quit':
                break
        except Exception as e:
            print('Error sending:', e)
            break


def main():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((HOST, PORT))

    # Wait for server's NICK prompt
    initial = client_sock.recv(1024).decode('utf-8')
    if initial == 'NICK':
        nickname = input('Enter your nickname: ')
        client_sock.send(nickname.encode('utf-8'))
    else:
        print('Unexpected server response:', initial)

    # Start receiver thread
    recv_thread = threading.Thread(target=receive, args=(client_sock,), daemon=True)
    recv_thread.start()

    try:
        write(client_sock)
    finally:
        client_sock.close()


if __name__ == '__main__':
    main()
