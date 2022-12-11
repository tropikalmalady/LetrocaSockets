import socket
import threading
import psycopg2
import random

connections = []
addresses = []

dbname = input('Digite o nome da base: ')
dbuser = input('\nDigite o nome do usuário: ')
dbpass = input('\nDigite a senha: ')

dbconn = psycopg2.connect("host={0} user={1} dbname={2} password={3}".format('localhost', dbuser, dbname, dbpass))

print('\nConexão com a base de dados estabelecida!')

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(('0.0.0.0', 50000))
        s.listen()
    except:
        return print('\nServidor não pode ser iniciado!')

    while True:
        conn, ender = s.accept()
        s.setblocking(1)

        connections.append(conn)
        addresses.append(ender)
        print('\nConectado em ', ender)
        t = threading.Thread(target=runGame, args=[conn, ender])
        t.start()

def runGame(conn, ender):
    try:
        dbconn = psycopg2.connect("host={0} user={1} dbname={2} password={3}".format('localhost', dbuser, dbname, dbpass))
        cur = dbconn.cursor()

        cur.execute("SELECT * FROM users WHERE ip = %s;", (str(ender[0]),))
        connectedUser = cur.fetchall()

        if (len(connectedUser) == 0):
            conn.send(str(0).encode())
            userName = conn.recv(1024).decode()
            cur.execute("INSERT INTO users (ip, nmuser) VALUES (%s, %s);", (str(ender[0]), userName))
            dbconn.commit()
        else:
            conn.send(str(1).encode())

        while True:
            action = conn.recv(1024).decode()

            if action == 'listrank':
                cur.execute("SELECT * FROM users;")
                users = cur.fetchall()
                retorno = ''
                for user in users:
                    rank = str(user[2])

                    if rank is None:
                        rank = '0'
                    
                    retorno += user[1] + ' -> ' + rank + '\n'
                conn.send(retorno.encode())
            elif action == 'resetrank':
                cur.execute("DELETE FROM users WHERE ip = %s;", (str(ender[0]),))
                dbconn.commit()
                conn.send(str.encode('deleted'))
            else:
                conn.send(str.encode('starting'))
            
            while action == 'startgame' or action == 'replay':
                if action != 'replay':
                    cur.execute("SELECT * FROM words;")
                    words = cur.fetchall()

                    word = random.choice(words)

                splitedWords = []
                for w in word[1].split():
                    l = list(w)
                    random.shuffle(l)
                    splitedWords.append(''.join(l))
                
                shuffledWord = ' '.join(str(item) for item in splitedWords)
                while shuffledWord == word[1]:
                    splitedWords = []
                    for w in word[1].split():
                        l = list(w)
                        random.shuffle(l)
                        splitedWords.append(''.join(l))
                    
                    shuffledWord = ' '.join(str(item) for item in splitedWords)

                conn.sendall(str.encode(shuffledWord))
                data = conn.recv(1024)
                if (not data):
                    break
                
                if (data.decode().upper() == word[1]):
                    cur.execute("UPDATE users SET vlrank = COALESCE((SELECT vlrank FROM users WHERE ip = %s), 0) + 100 WHERE ip = %s;", (str(ender[0]),str(ender[0])))
                    dbconn.commit()

                    conn.send(str(1).encode())
                    conn.send(word[2].encode())
                else:
                    cur.execute("UPDATE users SET vlrank = COALESCE((SELECT vlrank FROM users WHERE ip = %s), 0) - 10 WHERE ip = %s;", (str(ender[0]),str(ender[0])))
                    dbconn.commit()

                    retorno = 'A palavra era ' + word[1]

                    conn.send(str(2).encode())
                    conn.send(retorno.encode())
                
                action = conn.recv(1024).decode()
                
    except Exception as e:
        print(e)
        cur.close()
        dbconn.close()
        connections.remove(conn)

main()