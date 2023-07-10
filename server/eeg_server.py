from enum import Enum


class State(Enum):
    INIT = 0
    SENDING = 1
    RECEIVING = 2


class EEGServerBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        import socket

        self.connection: socket.socket
        self.tcp_socket: socket.socket

        self.state: State = State.INIT

    def initialize(self):
        print("Initializing EEG Server Box")
        import socket

        # Create a TCP/IP socket
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ("localhost", 12345)
        self.tcp_socket.bind(server_address)

    def process(self):
        # Wait for a connection
        if self.state == State.INIT:
            self.tcp_socket.listen(1)
            self.connection, client_address = self.tcp_socket.accept()
            print("Connection from", client_address)

            self.state = State.RECEIVING
        # Receive the data in small chunks and output it
        elif self.state == State.RECEIVING:
            import pickle as pkl

            data = self.connection.recv(4096)
            chunk = pkl.loads(data)
            self.output[0].append(chunk)

    def uninitialize(self):
        print("Uninitialized EEG Server Box")


box = EEGServerBox()
