#John Platkowski - November 8, 2026
#Handles the connection between the two players of an online session
import socket
import queue
import threading
import json

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
                sock, address = self.socket.accept()
                self.connection = Connection(sock)
            except BlockingIOError:
                return False
        return True

#Tyler Oswald - November 13th
#This class handles sending and receiving messages
class Connection:
    def __init__(self, sock):
        self.sock = sock
        self.sock.setblocking(True)
        #Queue that will hold messages between get calls
        self.messageQueue = queue.Queue()
        self.connected = True
        #Run listening thread in the background
        threading.Thread(target=self.listen, daemon=True).start()
    #Send a message in the format of a dict
    #Example usage: send({"type": "message_type", "key": "value"})
    def send(self, message):
        try:
            self.sock.sendall((json.dumps(message) + "\n").encode())
        except OSError:
            self.connected = False
    #Background thread to receive messages from the other client
    def listen(self):
        try:
            #Loop over all the messsages received by the socket
            for message in self.sock.makefile("rb"):
                try:
                    #Add each message to the queue
                    self.messageQueue.put(json.loads(message))
                except ValueError:
                    pass
        except OSError:
            pass
        self.connected = False
    #Method for getting all the messages that are currently in the queue
    def getMessages(self):
        received = []
        while not self.messageQueue.empty():
            received.append(self.messageQueue.get())
        return received