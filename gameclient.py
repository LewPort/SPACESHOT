import socket
import time
import json

host = '127.0.0.1'
port = 6969
s = socket.socket()
s.connect((host, port))

s.setblocking(False)


def upload_to_server(data):
    data = json.dumps(dict(data))
    data = data.encode('utf-8')
    s.send(data)

def download_from_server():
    try:
        data = s.recv(1024)
        data = data.decode('utf-8')
        data = json.loads(data)
        print(data)
        return data
    except BlockingIOError:
        pass

def upload_player_stats(player):
    global last_check
    if time.time() >= last_check + check_interval:
        upload_to_server(player.vital_stats())
        last_check = time.time()

last_check = time.time()
check_interval = 0.05
