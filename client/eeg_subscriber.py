class EEGPublisherBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        import socket

        self.tcp_socket: socket.socket

    def initialize(self):
        print("Initializing EEG publisher Box")
        import socket

        # Create a TCP/IP socket
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        subscriber_address = ("localhost", 12345)
        self.tcp_socket.connect(subscriber_address)

    def process(self):
        import pickle as pkl
        import time
        
        # Take the EEG signal from the input buffer
        eeg_signal_stream = self.input[0]
        while eeg_signal_stream:
            chunk = eeg_signal_stream.pop()
            # Send the data in small chunks
            time.sleep(1 / 64)  # 64 Hz
            self.tcp_socket.send(pkl.dumps(chunk))

    def uninitialize(self):
        print("Uninitialized EEG publisher Box")


box = EEGPublisherBox()
