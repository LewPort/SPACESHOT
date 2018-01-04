import socket
import json
import time, datetime


def get_player_name(data):
    return data['name']

def player_is_new(player_addr):
    if player_addr in connected_players:
        return False
    else:
        return True

def update_player(newinfo, storedinfo):
    if newinfo != storedinfo:
        storedinfo = newinfo

def decoded_data(data):
    if data:
        data = data.decode('utf-8')
        data = json.loads(data)
        return data

def encoded_data(data):
    try:
        data = json.dumps(dict(data))
        data = data.encode('utf-8')
        return data
    except TypeError:
        pass

def timestring():
    return datetime.datetime.fromtimestamp(time.time())

def add_new_players():
    try:
        s.listen(1)
        c, addr = s.accept()
        if player_is_new(c):
            connected_players.append(c)
            print('%s\nConnection from: %s' % (timestring(), addr))
            try:
                data = decoded_data(c.recv(1024))
                print('Name: %s' % data['name'])
            except BlockingIOError:
                pass
    except:
        pass

def receive_and_bounce_data_from_connections(list_of_players):
    for c in list_of_players:
        try:
            data = decoded_data(c.recv(1024))
            if data:
                for c in list_of_players:
                    c.send(encoded_data(data))

        except BlockingIOError or TypeError:
            pass

host = '127.0.0.1'
port = 6969
s = socket.socket()
s.setblocking(False)
s.bind((host, port))

print('%s:\nServer is RUNNING!' % timestring())

check_interval = 0.01
last_check_time = time.time()

connected_players = []

while True:
    if last_check_time + check_interval <= time.time():
        add_new_players()
        receive_and_bounce_data_from_connections(connected_players)


        last_check_time = time.time()