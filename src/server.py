import socket, threading
from datetime import date
import time

class ClientThread(threading.Thread):

    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.clientSocket = clientSocket
        self.threadLock = threading.RLock()
    
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
            loginmessage=self.clientSocket.recv(1024).decode()
            loginmessage=loginmessage.split(" ")[1:]

            clientUserName = loginmessage[0]
            clientPassword = loginmessage[1]
            print("username:",clientUserName)
            print("password:",clientPassword)
            # Check if user is exist or not
            if clientUserName in userDict.keys():
                # Check password is correct or not
                if clientPassword == userDict[clientUserName]:
                    loginSuccessMessage="loginsuccess "+clientUserName+" "+roleDict[clientUserName]
                    self.clientSocket.send(loginSuccessMessage.encode())
                    clientRole = roleDict[clientUserName]

                    isLogin = True

                    if clientRole=="branchmanager\n":
                        self.clientSocket.send(clientUserName.encode())
                    
                    
                        salesMessage=self.clientSocket.recv(1024).decode()
                        while salesMessage!="TERMINATE":
                        
                            sale = salesMessage.split(' ')[1:]
                            print(sale)
                            today = date.today()
                            d1 = today.strftime("%d.%m.%Y")
                            sale.append(d1)
                            print(sale)
                            salesFile = open("sales.txt","a")
                            self.threadLock.acquire() # Get Lock the threads 
                            for s in sale:
                                if s==sale[-1]:
                                    pass
                                else:
                                    s=s+";"
                                salesFile.write(s)
                            salesFile.write("\n")
                            salesFile.close() 
                            self.threadLock.release() # Release lock
                            self.clientSocket.send("record is added".encode())
                            self.clientSocket.send(clientUserName.encode())
                            salesMessage=self.clientSocket.recv(1024).decode()

                    else:
                        #Get the report choice from client.
                        report_selection=self.clientSocket.recv(1024).decode()
                        while report_selection!="TERMINATE":
                            if report_selection=="report1":
                                today = date.today()
                                d1 = today.strftime("%d.%m.%Y")
                                self.threadLock.acquire() # Get Lock the threads 
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
                                salesFile.close()
                                self.threadLock.release() # Release lock
                                #print("lattes:",latteCounter, "americanos:",americanoCounter,"cappucinos",cappucinoCounter,"espressos",espressoCounter)
                            elif report_selection=="report2":
                               today = date.today()
                               d1 = today.strftime("%d.%m.%Y")
                               self.threadLock.acquire() # Get Lock the threads 
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
                               equalCoffee = False
                               equalCoffeeValue = coffeedict[mostcoffee]
                               for coffee in coffeedict.keys():
                                   if (equalCoffee == False) and (coffee != mostcoffee) and (coffeedict[coffee] == coffeedict[mostcoffee]):
                                       equallCoffeeValue = coffeedict[mostcoffee]
                                       mostcoffee = mostcoffee + "and" + coffee
                                       equalCoffee = True
                                   elif (equalCoffee == True) and (coffee != mostcoffee.split(" ")[0]) and (coffeedict[coffee] == equalCoffeeValue):
                                        mostcoffee = mostcoffee + "and" + coffee
                               reportmessage="report2:"+mostcoffee.replace("and", ",")
                               print(reportmessage)
                               #Send to client report
                               self.clientSocket.send(reportmessage.encode())
                               report_selection=self.clientSocket.recv(1024).decode()
                               salesFile.close()
                               self.threadLock.release() # Release lock
                            elif report_selection=="report3":
                                today = date.today()
                                d1 = today.strftime("%d.%m.%Y")
                                self.threadLock.acquire() # Get Lock the threads 
                                salesFile=open("sales.txt", "r")
                                report=salesFile.readlines()
                                branchdict={"branchNicosia":0,"branchKyrenia":0}
                                for item in report:
                                    if item.find(d1)!=-1:
                                        if item.find("branchNicosia")!=-1:
                                            branchdict["branchNicosia"]=branchdict["branchNicosia"]+1
                                        elif item.find("branchKyrenia")!=-1:
                                            branchdict["branchKyrenia"]=branchdict["branchKyrenia"]+1
                                        else:
                                            pass
                                print(branchdict)
                                if (branchdict["branchNicosia"] == branchdict ["branchKyrenia"]):
                                    mostPopularBranchToday = "branchNicosia and branchKyrenia"
                                else:
                                    mostPopularBranchToday = max(branchdict, key=branchdict.get)
                                reportmessage="report3:"+mostPopularBranchToday
                                #Send to client report
                                self.clientSocket.send(reportmessage.encode())
                                report_selection=self.clientSocket.recv(1024).decode()
                                salesFile.close()
                                self.threadLock.release() # Release lock
                            elif report_selection=="report4":
                                self.threadLock.acquire()
                                salesFile=open("sales.txt", "r")
                                report=salesFile.readlines()
                                branchdict={"branchNicosia":0,"branchKyrenia":0}
                                for item in report:
                                    if item.find("branchNicosia")!=-1:
                                        branchdict["branchNicosia"]=branchdict["branchNicosia"]+1
                                    elif item.find("branchKyrenia")!=-1:
                                        branchdict["branchKyrenia"]=branchdict["branchKyrenia"]+1
                                    else:
                                        pass
                                print(branchdict)
                                if (branchdict["branchNicosia"] == branchdict ["branchKyrenia"]):
                                    mostPopularBranchGeneral = "branchNicosia and branchKyrenia"
                                else:
                                    mostPopularBranchGeneral = max(branchdict, key=branchdict.get)
                                reportmessage="report4:"+mostPopularBranchGeneral
                                #Send to client report
                                self.clientSocket.send(reportmessage.encode())
                                report_selection=self.clientSocket.recv(1024).decode()
                                salesFile.close()
                                self.threadLock.release() # Release lock
                else:
                    self.clientSocket.send("loginfailure invalid credentials".encode())
            else:
                self.clientSocket.send("loginfailure invalid credentials".encode())


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
