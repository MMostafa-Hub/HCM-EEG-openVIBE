from enum import Enum


class State(Enum):
    STAND_BY = 0
    RECORDING = 1


class EEGSubscriberBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        import socket

        self.connection: socket.socket
        self.udp_socket: socket.socket

        self.state: State = State.STAND_BY

    def initialize(self):
        print("Initializing EEG subscriber Box")
        import socket

        # Create a UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the port
        subscriber_address = ("localhost", 12345)
        self.udp_socket.bind(subscriber_address)

    def process(self):
        import pickle as pkl

        decoded_command, publisher_address = self.udp_socket.recvfrom(4096)
        command = pkl.loads(decoded_command)

        if command == "start":
            self.state = State.RECORDING

            print("Started recording")
        elif command == "stop":
            self.state = State.STAND_BY
            print("Stopped recording")

    def uninitialize(self):
        print("Uninitialized EEG subscriber Box")


box = EEGSubscriberBox()
