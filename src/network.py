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
