import socket

HEADER = 64
FORMAT = 'utf-8'
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    socket_client.send(send_length)
    socket_client.send(message)

def main():
    send("Hello, World!")
    send("!DISCONNECT")

if __name__ == "__main__":
    main()