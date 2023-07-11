from enum import Enum


class State(Enum):
    STAND_BY = 0
    RECORDING = 1


class EEGSubscriberBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        import pandas as pd
        import socket
        import threading

        self.connection: socket.socket
        self.udp_socket: socket.socket

        self.state: State = State.STAND_BY

        self.time_stamp = False
        self.command_thread: threading.Thread
        self.eeg_signal_header: OVSignalHeader
        self.eeg_dataset: pd.DataFrame = pd.DataFrame(
            columns=["timestamp", "time"] + [f"channel_{i}" for i in range(32)]
        )

    def _process_commands(self):
        import pickle as pkl

        while True:
            decoded_command, publisher_address = self.udp_socket.recvfrom(4096)
            command = pkl.loads(decoded_command)

            if self.state == State.STAND_BY and command == "start":
                self.state = State.RECORDING

                print("Started recording")

            elif self.state == State.RECORDING and command == "stop":
                self.state = State.STAND_BY
                print("Stopped recording")

            elif self.state == State.RECORDING and command == "time_stamp":
                self.time_stamp = True
                print("Time stamping")

    def initialize(self):
        print("Initializing EEG subscriber Box")
        import socket
        import threading

        # Create a UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the port
        subscriber_address = ("localhost", 12345)
        self.udp_socket.bind(subscriber_address)

        # Create a thread to process the commands
        self.command_thread = threading.Thread(target=self._process_commands)
        self.command_thread.start()

    def process(self):
        # Take the EEG signal from the input buffer
        eeg_signal_stream = self.input[0]
        while eeg_signal_stream:
            chunk = eeg_signal_stream.pop()
            if self.state == State.RECORDING:
                # TODO: save the data to a .csv file
                pass

    def uninitialize(self):
        print("Uninitialized EEG subscriber Box")
        import pandas as pd

        pd.DataFrame.to_csv(self.eeg_dataset, "eeg_dataset.csv")


box = EEGSubscriberBox()
