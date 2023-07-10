class EEGClientBox(OVBox):
    def __init__(self):
        import socket

        OVBox.__init__(self)
        self.tcp_socket: socket.socket

    def initialize(self):
        import socket

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("localhost", 12345)
        self.tcp_socket.connect(server_address)
        print("Initializing EEG Client Box")

    def process(self):
        import pickle as pkl

        eeg_signal_stream = self.input[0]
        while eeg_signal_stream:
            chunk = eeg_signal_stream.pop()
            # print(type(chunk))
            print(pkl.dumps(chunk))
            self.tcp_socket.send(pkl.dumps(chunk))

    def uninitialize(self):
        print("Uninitialized EEG Client Box")


box = EEGClientBox()
