import socket
import _thread
import time
import random

# IPADDR = "192.168.100.87"

IPADDR = "127.0.0.1"
PORT = 1234
playersConnected = dict()
Choices = ["Rock", "Scissors", "Spock", "Lizard", "Paper"]

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.bind((IPADDR, PORT))
ServerSocket.listen(3)
print("Server is listening...")


def start_game(client, rounds):
    PlayerScore = 0
    ServerScore = 0

    while PlayerScore < rounds and ServerScore < rounds:
        InvalidChoice = False
        playerWin = False
        playerChoice = client.recv(2048).decode("UTF-8")
        serverChoice = random.choice(Choices)

        if playerChoice == "Paper":
            if serverChoice == "Rock" or serverChoice == "Spock":
                playerWin = True
        elif playerChoice == "Rock":
            if serverChoice == "Lizard" or serverChoice == "Scissors":
                playerWin = True
        elif playerChoice == "Scissors":
            if serverChoice == "Paper" or serverChoice == "Lizard":
                playerWin = True
        elif playerChoice == "Spock":
            if serverChoice == "Scissors" or serverChoice == "Rock":
                playerWin = True
        elif playerChoice == "Lizard":
            if serverChoice == "Spock" or serverChoice == "Paper":
                playerWin = True
        else:
            InvalidChoice = True
            msg = "Wrong choice! try again!"
            client.send(bytearray(msg.encode("UTF=8")))

        if InvalidChoice == False:
            if playerWin:
                PlayerScore += 1
                msg = "Server choice: "+serverChoice+" You win! Score: "+str(PlayerScore)+":"+str(ServerScore)
                client.send(bytearray(msg.encode("UTF-8")))
            else:
                ServerScore += 1
                msg = "Server choice: "+serverChoice+" I win! Score: " + str(PlayerScore) + ":" + str(ServerScore)
                client.send(bytearray(msg.encode("UTF-8")))

    msg = "Game over! Score: (Player)"+str(PlayerScore)+"-"+str(ServerScore)+"(Server)\n"
    client.send(bytearray(msg.encode("UTF-8")))
    time.sleep(1)


def handle_client(client):
    global playersConnected
    try:
        while True:

            if len(playersConnected) > 3 and not playersConnected[client]:
                msg = "Game is full. Please wait ...\n"
                client.send(bytearray(msg.encode("UTF-8")))
                time.sleep(5)
            else:
                playersConnected[client] = True
                meniu = "Choose the number of games:\n 1. 2/3\n 2. 3/5\n 3. Quit\n"

                client.send(bytearray(meniu.encode("UTF-8")))

                option = int(client.recv(2048).decode("UTF-8"))

                response = "Am primit optiunea: "+str(option)
                client.send(bytearray(response.encode("UTF-8")))

                if option == 1:
                    start_game(client, 2)

                if option == 2:
                    start_game(client, 3)

                if option == 3:
                    del playersConnected[client]
                    print(len(playersConnected))
                    msg = "Ati fost deconectat!"
                    client.send(bytearray(msg.encode("UTF-8")))
                    break

        client.close()
    except ConnectionResetError:
        del playersConnected[client]
        print("Un client s-a deconectat!\n")


while True:
    Client, address = ServerSocket.accept()
    print("Connected: "+address[0]+':'+str(address[1]))
    _thread.start_new_thread(handle_client, (Client, ))
    playersConnected[Client] = False
ServerSocket.close()

