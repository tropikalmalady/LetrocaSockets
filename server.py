import socket
import csv
import random

HOST = 'localhost'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print('Aguardando cliente')

conn, ender = s.accept()

print('Conectado em ', ender)
while True:
    l = list('PALAVRA')
    random.shuffle(l)
    word = ''.join(l)
    conn.sendall(str.encode(word))
    data = conn.recv(1024)

    if (not data):
        print('Fechando')
        break
    
    if (data.decode() == 'PALAVRA'):
        conn.send(str(1).encode())
    else:
        conn.send(str(2).encode())