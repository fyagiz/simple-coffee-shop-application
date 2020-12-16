import socket, threading
from datetime import date

class ClientThread(threading.Thread):

    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.clientSocket = clientSocket
    
    def run(self):
        print("Connection is from ", self.clientAddress)

        # Send client to connection established message.
        self.clientSocket.send("Connection Established!".encode())

        isLogin = False
        # Read "users.txt" txt file
        usersFile = open("users.txt", "r")
        userDict = dict()
        roleDict = dict()
        for line in usersFile:
            line = line.split(';')
            userDict[line[0]] = line[1]
            roleDict[line[0]] = line[2]

        # Get username and password from client
        while isLogin == False:
            clientUserName = self.clientSocket.recv(1024).decode()
            clientPassword = self.clientSocket.recv(1024).decode()
            # Check if user is exist or not
            if clientUserName in userDict.keys():
                # Check password is correct or not
                if clientPassword == userDict[clientUserName]:
                    self.clientSocket.send(roleDict[clientUserName].encode())
                    clientRole = roleDict[clientUserName]
                    

                    isLogin = True
                    self.clientSocket.send(clientUserName.encode())
                    
                    
                    salesMessage=self.clientSocket.recv(1024).decode()
                    
                    if clientRole=="branchmanager\n":
                        while salesMessage!="closed":
                        
                            sale = salesMessage.split(' ')[1:]
                            print(sale)
                            today = date.today()
                            d1 = today.strftime("%d.%m.%Y")
                            sale.append(d1)
                            print(sale)
                            salesFile = open("sales.txt","a")
                            for s in sale:
                                if s==sale[-1]:
                                    pass
                                else:
                                    s=s+";"
                                salesFile.write(s)
                            salesFile.write("\n")
                        
                            self.clientSocket.send("record is added".encode())
                            self.clientSocket.send(clientUserName.encode())
                            salesMessage=self.clientSocket.recv(1024).decode()

                    else:
                        pass

                    
                    
                     
                else:
                    self.clientSocket.send("INCORRECT PASSWORD!".encode())
            else:
                self.clientSocket.send("USER NOT FOUND!".encode())


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