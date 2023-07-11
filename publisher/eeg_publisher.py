class EEGPublisherBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        import socket

        self.udp_socket: socket.socket
        self.subscriber_address = ("localhost", 12345)

    def initialize(self):
        print("Initializing EEG publisher Box")
        import socket

        # Create a UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def process(self):
        import pickle as pkl

        command = input("Enter command: ")
        self.udp_socket.sendto(pkl.dumps(command), self.subscriber_address)

    def uninitialize(self):
        print("Uninitialized EEG publisher Box")


box = EEGPublisherBox()
