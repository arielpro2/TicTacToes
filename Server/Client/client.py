import json
import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    a = sock.recv(512)
    a = a[:a.index(b'\0')]
    player_id = json.loads(a.decode())['player_id']
    print(player_id)

    request = json.dumps({'player_id': player_id, 'action': 'create_room'}).encode().ljust(512, b'\0')
    sock.send(request)

    a = sock.recv(1024)
    a = a[:a.index(b'\0')]

    print(a)