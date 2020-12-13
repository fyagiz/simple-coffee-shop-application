import socket, threading


class ClientThread(threading.Thread):

    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.clientSocket = clientSocket
    
    def run(self):
        print("Connection is from ", self.clientAddress)
        clientUserName = self.clientSocket.recv(1024).decode()
        clientPassword = self.clientSocket.recv(1024).decode()
        print(clientUserName + " " + clientPassword)


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5000

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        serverSocket.bind((HOST, PORT))
    except:
        print("Call to find failed!")
        exit(1)
    
    while True:
        serverSocket.listen()
        connection, address = serverSocket.accept()
        newThread = ClientThread(address, connection)
        newThread.start()
    
    serverSocket.close()