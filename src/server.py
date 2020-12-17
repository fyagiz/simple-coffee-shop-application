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
                    


                    if clientRole=="branchmanager\n":
                        self.clientSocket.send(clientUserName.encode())
                    
                    
                        salesMessage=self.clientSocket.recv(1024).decode()
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
                        #Get the report choice from client.
                        report_selection=self.clientSocket.recv(1024).decode()
                        while report_selection!="closed":
                            if report_selection=="report1":
                                today = date.today()
                                d1 = today.strftime("%d.%m.%Y")
                            
                                salesFile=open("sales.txt", "r")
                                report=salesFile.readlines()
                            
                                latteCounter=0
                                americanoCounter=0
                                cappucinoCounter=0
                                espressoCounter=0
                                for item in report:
                                    if item.find(d1)!=-1:
                                        if item.find("Latte")!=-1:
                                            latteCounter=latteCounter+1
                                        elif item.find("Americano")!=-1:
                                            americanoCounter=americanoCounter+1
                                        elif item.find("Espresso")!=-1:
                                            espressoCounter=espressoCounter+1
                                        elif item.find("Cappucino")!=-1:
                                            cappucinoCounter=cappucinoCounter+1
                                        else:
                                            pass
                                report1message="report1:"+str(americanoCounter)+";"+str(espressoCounter)+";"+str(latteCounter)+";"+str(cappucinoCounter)
                                print("report1message",report1message)
                                #Send to client report
                                self.clientSocket.send(report1message.encode())
                                report_selection=self.clientSocket.recv(1024).decode()
                                #print("lattes:",latteCounter, "americanos:",americanoCounter,"cappucinos",cappucinoCounter,"espressos",espressoCounter)
                            elif report_selection=="report2":
                               today = date.today()
                               d1 = today.strftime("%d.%m.%Y")
                               
                               salesFile=open("sales.txt", "r")
                               report=salesFile.readlines()

                               coffeedict={"Americano":0,"Espresso":0,"Latte":0,"Cappucino":0}
                               for item in report:
                                   if item.find(d1)!=-1:
                                       if item.find("Americano")!=-1:
                                           coffeedict["Americano"]=coffeedict["Americano"]+1
                                       elif item.find("Espresso")!=-1:
                                            coffeedict["Espresso"]=coffeedict["Espresso"]+1
                                       elif item.find("Latte")!=-1:
                                            coffeedict["Latte"]=coffeedict["Latte"]+1
                                       elif item.find("Cappucino")!=-1:
                                            coffeedict["Cappucino"]=coffeedict["Cappucino"]+1
                                       else:
                                            pass
                               mostcoffee = max(coffeedict, key=coffeedict.get)
                               reportmessage="report2:"+mostcoffee
                               #Send to client report
                               self.clientSocket.send(reportmessage.encode())
                               report_selection=self.clientSocket.recv(1024).decode()
                    
                    
                     
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
