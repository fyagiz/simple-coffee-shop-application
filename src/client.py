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
    
    # Call main gui
    window = ClientGui(clientSocket)
    window.mainloop()
    clientSocket.close()