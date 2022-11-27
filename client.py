import socket

HOST = input("Digite o ip do servidor: ")
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def play():
    data = s.recv(1024)

    print('\nA sua palavra é:')
    print('\n------   ' + data.decode() + '   ------')

    word = input('\nDigite sua tentativa: ')

    s.send(str.encode(word))

    result = int(s.recv(1024).decode())

    if (result == 1):
        print('\nParabéns você acertou!')
        return
    else:
        print('\nVocê errou! Tente novamente')

    while True:
        print('\n1 - Tentar novamente')
        print('\n2 - Sair')

        opt = int(input('\nEscolha uma opção: '))

        if (opt != 1 and opt !=2):
            print('\nOpção inválida digite novamente!')

        if (opt == 2):
            break

        if (opt == 1):
            play()
            break

    return

print('\nBem vindo ao Letroca!')

while True:
    print('\n------   MENU   ------')
    print('\n1 - Jogar')
    print('\n2 - Sair')

    opt = int(input('\nEscolha uma opção: '))

    if (opt != 1 and opt !=2):
        print('\nOpção inválida digite novamente!')

    if (opt == 2):
        break

    if (opt == 1):
        play()