import socket

# IPADDR = "192.168.100.87"

IPADDR = "127.0.0.1"
PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IPADDR, PORT))

def start_game(server, rounds):

    msg = ""

    while str(rounds) not in msg:
        choice = input("Your choice (Lizard, Rock, Paper, Scissors, Spock): ")
        server.send(bytearray(choice.encode("UTF-8")))

        msg = server.recv(2048).decode("UTF-8")
        print(msg)

    msg = server.recv(2048).decode("UTF-8")
    print(msg)


while True:

    msg = s.recv(2048).decode("UTF-8")
    print(msg)

    if "wait" not in msg:

        option = 0
        while option != 1 and option != 2 and option != 3:
            try:
                option = int(input("Enter your option: "))
            except:
                print("Invalid option! Option must be a number!\n")
            else:
                print("Invalid option!")

        # if option == 3:
        #     s.send(bytearray(str(option).encode("UTF-8")))

        s.send(bytearray(str(option).encode("UTF-8")))

        receivedMsg = s.recv(100).decode("UTF-8")
        print("[server] "+receivedMsg)

        if option == 1:
            start_game(s, 2)

        if option == 2:
            start_game(s, 3)

        if option == 3:
            msg = s.recv(2040).decode("UTF-8")
            print(msg)
            break



s.close()
