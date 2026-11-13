#John Platkowski - November 8, 2026
#Handles the connection between the two players of an online session
import socket

#Port the host listens on for the other player
PORT = 5555

#Created by the host, waits for the other player to connect
class Server:
    def __init__(self):
        self.connection = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", PORT))
        self.socket.listen(1)
        self.socket.setblocking(False)

    #Wait for a player trying to connect, return true once connected
    def accept(self):
        if self.connection is None:
            try:
                self.connection, address = self.socket.accept()
                self.connection.setblocking(False)
            except BlockingIOError:
                return False
        return True

#Trey - 11/13/2026
#class representing a client
class Client:
    def __init__(self, address):
        self.address = address
        self.connection = None
    
    #try to connect to the host, returns true if succesful, returns false on failure
    def connect(self):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.settimeout(3)
            self.connection.connect((self.address, PORT))
            self.connection.setblocking(False)
            return True
        except OSError:
            self.connection = None
            return False


#Trey - 11/13/2026
#Return local ip address, it will be used as the session ID
def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        s.close()
        return "127.0.0.1"
