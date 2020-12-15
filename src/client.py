import socket
from tkinter import *
from tkinter import messagebox

class ClientGui(Frame):
    def __init__(self, clientSocket):
        Frame.__init__(self)
        self.serverSocket = clientSocket
        self.pack()

        # Set Title
        self.master.title("Simple Coffee Shop Application")

        # Create username frame, label and entry field
        self.userNameFrame = Frame(self)
        self.userNameFrame.pack(padx = 5, pady = 5)

        self.userNameLabel = Label(self.userNameFrame, text="Username: ")
        self.userNameLabel.pack(side = LEFT, padx = 5, pady = 5)

        self.userNameEntry = Entry(self.userNameFrame, name="username")
        self.userNameEntry.pack(side = LEFT, padx = 5, pady = 5)

        # Create password frame, label and entry field
        self.passwordFrame = Frame(self)
        self.passwordFrame.pack(padx = 5, pady = 5)

        self.passwordLabel = Label(self.passwordFrame, text="Password: ")
        self.passwordLabel.pack(side = LEFT, padx = 5, pady = 5)

        self.passwordEntry = Entry(self.passwordFrame, name="password", show = "*")
        self.passwordEntry.pack(side = LEFT, padx = 5, pady = 5)

        # Login Button
        self.passwordEntry.pack(side = LEFT, padx = 5, pady = 5)
        self.loginButton = Button(self, text="Login", command=self.LoginButtonPressed)
        self.loginButton.pack(padx = 5, pady = 5)

        # Show connection successfull message
        messagebox.showinfo("Success!", "Connection is established!")

        # Set focus to username enrry field
        self.userNameEntry.focus_force()

    def LoginButtonPressed(self):
        # Get userName and password from users via Gui
        userName = self.userNameEntry.get()
        password = self.passwordEntry.get()

        # Send server the informations
        self.serverSocket.send(userName.encode())
        self.serverSocket.send(password.encode())

        # Get server response
        serverResponse = self.serverSocket.recv(1024).decode()
        serverResponse = serverResponse.replace("\n","")
        print(serverResponse)
        if serverResponse == "INCORRECT PASSWORD!":
            messagebox.showerror("Error!", "Invalid credentials")
        elif serverResponse == "USER NOT FOUND!":
            messagebox.showerror("Error!", "User not found!")
        elif serverResponse == "branchmanager":
            self.destroy()
            self.showBranchManagerPanel()
        elif serverResponse=="coffeeshopmanager":
            self.destroy()
            self.showCoffeeShopManagerPanel()
    
    def showBranchManagerPanel(self):
        self.master.title("Coffee Shop Branch")
        self.CoffeeSelectionFrame = Frame()
        self.CoffeeSelectionFrame.pack(padx=5, pady=5)
        
        self.CoffeeLabel = Label(self.CoffeeSelectionFrame, text = "Coffee: ")
        self.CoffeeLabel.pack(side=LEFT, padx=5, pady=5)
        
        self.CoffeeSelections = ["Americano", "Espresso", "Latte","Cappucino"]
        
        self.coffee = StringVar()
        self.coffee.set(self.CoffeeSelections[0])
		#If you want have none of them is selected, then you can use self.size.set(None)
        for CoffeeSelection in self.CoffeeSelections:
            self.CoffeeTypeSelection = Radiobutton(self.CoffeeSelectionFrame, text= CoffeeSelection, value= CoffeeSelection, variable = self.coffee)
            self.CoffeeTypeSelection.pack(side=LEFT, padx=5, pady=5)
            
        self.frame2 = Frame()
        self.frame2.pack(padx=5, pady=5)
        
        self.CoffeeSizeLabel = Label(self.frame2, text="Size:")
        self.CoffeeSizeLabel.pack(side = LEFT, padx=5, pady=5)
        
        self.CoffeeSizes = ["Small","Medium","Large"]
        self.size = StringVar()
        self.size.set(self.CoffeeSizes[0])
        
        for CoffeeSize in self.CoffeeSizes:
            self.CoffeeSizeSelection = Radiobutton(self.frame2, text=CoffeeSize, value=CoffeeSize, variable=self.size)
            self.CoffeeSizeSelection.pack(side = LEFT, padx=5, pady=5)
        
        self.frame3=Frame()
        self.frame3.pack(padx=5, pady=5)
        self.InformButton=Button(self.frame3, text = "Inform", command=self.InformButtonPressed)
        self.InformButton.pack(side=LEFT,padx=5,pady=5)
        
        self.CloseButton=Button(self.frame3, text = "Close", command=self.CloseButtonPressed)
        self.CloseButton.pack(side=LEFT,padx=5,pady=5)
        
    def InformButtonPressed(self):
        coffee_size = self.size.get()
        CoffeeSelection = ""
        coffee_type=self.coffee.get()
       
        clientBranch = self.serverSocket.recv(1024).decode()
        print("clientBranch:", clientBranch)
        # Send server the informations
        salesMessage="sale "+coffee_type+" "+coffee_size+ " "+clientBranch
        self.serverSocket.send(salesMessage.encode())

        # Get server response
        serverResponse = self.serverSocket.recv(1024).decode()
        if serverResponse=="record is added":
            messagebox.showinfo("Show Success", "Sales record has been added successfully")
        else:
           messagebox.showerror("Error", "Sales record has not been added successfully")
        
        print("salesmessage:", salesMessage)
    def CloseButtonPressed(self):
        self.serverSocket.send("closed".encode())
        self.master.destroy()
    def showCoffeeShopManagerPanel(self):
        self.master.title("Coffee Shop Manager")
        self.ReportSelectionFrame = Frame()
        self.ReportSelectionFrame.pack(padx=5, pady=5)
        
        self.ReportLabel = Label(self.ReportSelectionFrame, text = "Select your report: ")
        self.ReportLabel.pack(side=LEFT, padx=5, pady=5)

        self.ReportTypes = ["(1)How many Americano, Espresso, Latte and Cappuccino have been sold today?","(2)What is the most popular coffee today?","(3)What is the most popular branch today?","(4)What is the most popular branch in general?"]
        self.type = StringVar()
        self.type.set(self.ReportTypes[0])
        
        for ReportType in self.ReportTypes:
            self.ReportTypeSelection = Radiobutton(self.ReportSelectionFrame, text=ReportType, value=ReportType, variable=self.type)
            self.ReportTypeSelection.pack(side = LEFT, padx=5, pady=5)


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5000

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        clientSocket.connect((HOST, PORT))
    except:
        error = Tk()
        error.withdraw()
        messagebox.showerror("Error!", "Connection is not established!")
        exit(1)
    
    # Wait for the "Connection Established" message from Server
    serverResponse = clientSocket.recv(1024).decode()
    if serverResponse == "Connection Established!":
        # Call main gui
        window = ClientGui(clientSocket)
        window.mainloop()
        clientSocket.close()