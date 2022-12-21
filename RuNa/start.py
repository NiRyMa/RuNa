import socket, rsa
from datetime import datetime
def upload_keys(keys):
    file = open('keys', 'w')
    for key, value in keys.items():
        file.write(f'{key} {value}\n')
    file.close()
def file_open():
    try:
        file = open("clients", 'r')
        users = {}
        file = file.read().split("\n")[:-1]
        for i in range(len(file)):
            name, passwd = file[i].split()
            users[name] = passwd
        return users
    except:
        file = open("clients", 'w')
        file.write(' ')
        file.close()
        users = {}
        return users
def file_close(clients):
    file = open("clients", 'w')
    for key, value in users.items():
        file.write(f'{key} {value}\n')
    file.close()

host = ''
port = 2571

keys = {}
players = []
clients = {}
users = file_open()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

print("Start")
while True:
    data, addr = sock.recvfrom(1024)
    if addr not in players:
        while True:
            name, passwd, pub = data.decode().split()
            try:
                if users[name] == passwd:
                    print("Succes login!")
                    sock.sendto('1'.encode(), addr)
                    clients[name] = addr
                    keys[name] = pub#.replace('|','\n').replace('_', ' ')
                    players.append(addr)
                    break
                elif users[name] != passwd:
                   print("Error password!")
                   break
            except KeyError:
                users[name] = passwd
                sock.sendto('1'.encode(), addr)
                clients[name] = addr
                keys[name] = pub#.replace('|','\n').replace('_', ' ')
                players.append(addr)
                break
    else:
        otpravitel, poluchatel, data = data.split(' '.encode(), 2)
        print("FROM ["+otpravitel.decode()+"] FOR ["+poluchatel.decode()+"] IN ["+str(datetime.now())+"]: ")
        print(data)
        if poluchatel.decode() in clients and poluchatel.decode() != otpravitel.decode():
                sock.sendto((otpravitel+" :: ".encode()+data),clients[poluchatel.decode()])
    upload_keys(keys)
file = open("clients", 'w')
file.write(' ')
file.close()
file_close(users)
sock.close()


