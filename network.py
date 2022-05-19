import socket
import pickle


class Network:
    def __init__(self, server, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.id = self.connect()

    def getId(self):
        return self.id

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
