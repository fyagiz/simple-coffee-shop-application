import socket, threading

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.clientAddress=clientAddress
        self.clientSocket=clientSocket
    
    def run(self):
        print("Connection is from", self.clientAddress)
        msg=("SERVER >>> "+"CONNECTION ESTABLISHED").encode()
        self.clientSocket.send(msg)
        username=self.clientSocket.recv(1024).decode()
        password=self.clientSocket.recv(1024).decode()
        print(username)
        print(password)
        f = open("users.txt", "r")
        userlist=dict()
        rolelist=dict()
        for x in f:
            line=x.split(";")
            userlist[line[0]]=line[1]
            rolelist[line[0]]=line[2]
        print(userlist)
        print(rolelist)

            
        self.clientSocket.close()
if __name__=="__main__":
    HOST = "127.0.0.1"
    PORT=5000
    
    mySocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) #work with multiple clients
    try:
        mySocket.bind((HOST,PORT))
    except:
        print("Call to bind failed")
        exit(1)
    while True:
        mySocket.listen()
        connection, address= mySocket.accept()
        newthread= ClientThread(address, connection)
        newthread.start()
