class EEGClientBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        import socket

        self.tcp_socket: socket.socket

    def initialize(self):
        import socket

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("192.168.220.97", 12345)
        self.tcp_socket.connect(server_address)
        print("Initializing EEG Client Box")

    def process(self):
        import pickle as pkl
        import time

        eeg_signal_stream = self.input[0]
        while eeg_signal_stream:
            chunk = eeg_signal_stream.pop()
            time.sleep(1 / 64)  # 64 Hz
            self.tcp_socket.send(pkl.dumps(chunk))

    def uninitialize(self):
        print("Uninitialized EEG Client Box")


box = EEGClientBox()
