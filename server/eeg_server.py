class EEGServerBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        import socket

        self.connection: socket.socket

    def initialize(self):
        import socket 

        print("Initializing EEG Server Box")
        # Create a TCP/IP socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("localhost", 12345)
        tcp_socket.bind(server_address)
        tcp_socket.listen(1)

        self.connection, client_address = tcp_socket.accept()
        print("Connection from: ", client_address)

    def process(self):
        import pickle as pkl

        data = self.connection.recv(4096)
        chunk = pkl.loads(data)
        print(chunk)

    def uninitialize(self):
        print("Uninitialized EEG Server Box")


box = EEGServerBox()
