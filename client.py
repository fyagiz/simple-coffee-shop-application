from tkinter import *
import socket
from tkinter import messagebox
class EntryDemo(Frame):
    def __init__(self, client):
        Frame.__init__(self)
        self.client=client

        self.pack(expand=YES, fill=BOTH)
        self.master.title("Login")

        serverMsg=self.client.recv(1024).decode()
        if serverMsg=="SERVER >>> CONNECTION ESTABLISHED":
            messagebox.showinfo("Message","Connection established")
            self.Label1=Label(self, text="Username:",width=10, height=2)
            self.Label1.pack(side=LEFT,padx=5, pady=5)

            self.text1=Text(self,name="text1",width=10, height=2)
            self.text1.pack(side=LEFT, padx=5, pady=6)
            self.text1.focus_force()
            
            self.Label2= Label(self, text="Password:",width=10, height=2)
            self.Label2.pack(side=LEFT, padx=10, pady=5)

            self.text2=Text(self,name="text2",width=10, height=2)
            self.text2.pack(side=LEFT, padx=10, pady=10)
            self.text2.focus_force()

            self.button= Button(self, text="Login", command=self.submitMessage)
            self.button.pack(side=BOTTOM)
        else:
            messagebox.showinfo("Error","Connection cannot established")
            exit(1)

        
    
    def submitMessage(self):
        username=self.text1.get("1.0", END)[0:-1]
        self.client.send((username).encode())
        password=self.text2.get("1.0",END)[0:-1]
        self.client.send((password).encode())
        serverMsg=self.client.recv(1024).decode()
        
        
if __name__=="__main__":
    HOST="127.0.0.1"
    PORT=5000

    mySocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        mySocket.connect((HOST,PORT))
        print("yes")
    except:
        print("Call to connect failed")
        exit(1)
    window=EntryDemo(mySocket)
    window.mainloop()
    mySocket.close()

