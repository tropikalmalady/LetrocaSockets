import socket

HOST = input("Digite o ip do servidor: ")
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

if int(s.recv(1024).decode()) == 0:
    userName = input('\nDigite seu nome de usuário: ')
    s.send(str.encode(userName))


def play():
    data = s.recv(1024)

    print('\nA sua palavra é:')
    print('\n------   ' + data.decode() + '   ------')

    word = input('\nDigite sua tentativa: ')

    while not word:
        word = input('\nDigite sua tentativa: ')

    s.send(str.encode(word))

    result1 = int(s.recv(1024).decode())
    result2 = s.recv(4096).decode()

    if (result1 == 1):
        print('\nParabéns você acertou!')
        print('\n-> ' + result2)
        s.send(str.encode('gameover'))
        return
    else:
        print('\nVocê errou! Tente novamente')

    while True:
        print('\n1 - Tentar novamente')
        print('\n2 - Sair')

        opt = input('\nEscolha uma opção: ')

        if (opt != '1' and opt !='2'):
            print('\nOpção inválida digite novamente!')

        if (opt == '2'):
            print('\n-> ' + result2)
            s.send(str.encode('gameover'))
            break

        if (opt == '1'):
            s.send(str.encode('replay'))
            play()
            break

    return

def listRank(rank):
    print('\n------   Ranking geral   ------')
    print('\nUsuário  ->  Rank')
    print(rank)

print('\nBem vindo ao Letroca!')

while True:
    print('\n------   MENU   ------')
    print('\n1 - Jogar')
    print('\n2 - Mostrar ranking')
    print('\n3 - Resetar seu ranking')
    print('\n4 - Sair')

    opt = input('\nEscolha uma opção: ')

    if (opt == '1'):
        s.send(str.encode('startgame'))
        s.recv(1024).decode()
        play()
    elif (opt == '2'):
        s.send(str.encode('listrank'))
        listRank(s.recv(4096).decode())
    elif (opt == '3'):
        s.send(str.encode('resetrank'))
        s.recv(1024).decode()
        print('\n Seu ranking foi resetado!')
        s.close()
        break
    elif (opt == '4'):
        s.close()
        break
    else:
        print('\nOpção inválida digite novamente!')