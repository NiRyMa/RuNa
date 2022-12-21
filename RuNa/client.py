import socket, threading, time, hashlib, rsa
from datetime import datetime

#тута шаманить с шифрованием
eng="qwertyuiop[]asdfghjkl;'zxcvbnm,."
rus="йцукенгшщзхъфывапролджэячсмитьбю"
shutdown = 0
join = 0

keys={}
clients = {}
private_key = ''
def load_keys():
    file = open('keys','r')
    keys = {}
    file = file.read().split("\n")[:-1]
    for i in range(len(file)):
        name, passwd = file[i].split()
        keys[name] = passwd
    return keys
def register():
    print("ЗАГРУЗКА...")
    pubkey,privkey = rsa.newkeys(2048)
    global private_key
    private_key = privkey
    pub = pubkey.save_pkcs1()
    name = input("Username: ")
    passwd = input("Password: ")
    for i in range(len(passwd)):
        for j in range(len(rus)):
            if passwd[i]==rus[j]:
                passwd=passwd.replace(passwd[i],eng[j])
    passwd = hashlib.sha256(passwd.encode()).hexdigest()#Разберись с шифрованием sha256
    return name+' '+passwd+' '+(pub.decode().replace(' ','_').replace('\n','|'))
    
def receving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                otpravitel, kras, data = data.split(' '.encode(), 2)
                print('['+otpravitel.decode()+']'+' -=- '+":"+str(datetime.now().time())+":" + ' -=- ' + (rsa.decrypt(data, private_key)).decode())
                time.sleep(0.2)
        except:
            pass

host = 'localhost'
port = 0

server = ("0.0.0.0", 2571)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))
sock.setblocking(1)#нада

while True:
    if not join:
        name = register()
        username, passwd, pub = name.split()
        if type(name) == str:
            sock.sendto((name).encode("utf-8"), server)
            time.sleep(1)
            data, add = sock.recvfrom(1024)
            if data.decode() == '1':
                join = 1
                sock.setblocking(0)
                rt = threading.Thread(target = receving, args = ("RecvThread", sock))# разберись что за многопотчность
                rt.start()
                print("Что бы отправить другому пользователю сообщение введите его в формате \nusername message")
        else:
            continue
    else:
        message = input().split(' ', 1)
        keys = load_keys()
        if message != ['']:
            sock.sendto(username.encode()+' '.encode()+message[0].encode()+" ".encode()+rsa.encrypt(message[1].encode(),rsa.PublicKey.load_pkcs1(keys[message[0]].replace('|','\n').replace('_', ' '), "PEM")), server)
        time.sleep(0.2)
rt.join()
sock.close()


