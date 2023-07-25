from enum import Enum
import pandas as pd
import socket
import threading
import pickle as pkl
import numpy as np


class State(Enum):
    STAND_BY = 0
    RECORDING = 1


class Command(Enum):
    START = 0
    STOP = 1
    START_EVENT = 2
    END = 3


# FOR eego sports headset
# CHANNEL_COUNT = 66
# SUBSCRIBER_IP = "192.168.248.36"

# FOR Generic Oscillator
CHANNEL_COUNT = 32
SUBSCRIBER_IP = "localhost"


class EEGSubscriberBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)

        self.udp_socket: socket.socket
        self.publisher_address: tuple = None
        self.state: State = State.STAND_BY
        self.event = 0
        self.command_thread: threading.Thread
        self.eeg_signal_header: OVSignalHeader
        self.eeg_df = pd.DataFrame(
            columns=["event", "timestamp"]
            + [f"channel_{i}" for i in range(CHANNEL_COUNT)]
        )

    # To send large data over UDP we need to split it into chunks
    def send_large_data(self, sock: socket.socket, data: bytes, addr: tuple):
        CHUNK_SIZE = 4096  # Choose a size
        chunks = [data[i : i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]
        for chunk in chunks:
            sock.sendto(chunk, addr)

    def _process_commands(self):
        print("Thread to process commands started")

        try:
            while True:
                print("Waiting for command")
                encoded_command, self.publisher_address = self.udp_socket.recvfrom(4096)
                command = pkl.loads(encoded_command)
                print(f"Received command {command} from {self.publisher_address}")

                if self.state == State.STAND_BY and command == Command.START:
                    self.state = State.RECORDING
                    print("Started recording")

                elif self.state == State.RECORDING and command == Command.STOP:
                    self.state = State.STAND_BY
                    print("Stopped recording")

                elif self.state == State.RECORDING and command == Command.START_EVENT:
                    self.event = self.event + 1
                    print(f"Started Event {self.event}")

                elif command == Command.END:
                    print("Received End command")

                    # Send the dataframe to the publisher
                    self.send_large_data(
                        self.udp_socket, pkl.dumps(self.eeg_df), self.publisher_address
                    )

                    print("Sent dataframe to publisher")
                    # Clears the dataframe but keeps the columns
                    self.eeg_df = self.eeg_df[0:0]

                    # Reset the event count
                    self.event = 0

        except OSError as e:
            # Throws an error when the socket is closed
            # and still waiting for a command from the publisher
            print("Socket closed")

    def initialize(self):
        print("Initializing EEG subscriber Box")

        # Create a UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        print("Socket created")

        # Bind the socket to the port
        subscriber_address = (SUBSCRIBER_IP, 12345)
        self.udp_socket.bind(subscriber_address)

        print("Socket created and bound to port 12345")

        # Create a thread to process the commands
        # Daemon threads are abruptly stopped at shutdown
        self.command_thread = threading.Thread(
            target=self._process_commands, daemon=True
        )
        self.command_thread.start()

    def process(self):
        # Take the EEG signal from the input buffer
        eeg_signal_stream = self.input[0]
        while eeg_signal_stream:
            chunk = eeg_signal_stream.pop()

            if isinstance(chunk, OVSignalHeader):
                self.eeg_signal_header = chunk
            elif isinstance(chunk, OVSignalBuffer):
                if self.state == State.RECORDING:
                    eeg_matrix = np.array(chunk).reshape(
                        tuple(self.eeg_signal_header.dimensionSizes)
                    )

                    for i in range(self.eeg_signal_header.dimensionSizes[0]):
                        self.eeg_df = self.eeg_df.append(
                            {
                                "timestamp": pd.Timestamp.now(),
                                "event": self.event,
                                **{
                                    f"channel_{j}": eeg_matrix[i, j]
                                    for j in range(CHANNEL_COUNT)
                                },
                            },
                            ignore_index=True,
                        )
                    print(self.eeg_df.shape)

    def uninitialize(self):
        print("Uninitialized EEG subscriber Box")
        self.udp_socket.close()
        self.command_thread.kill = True


box = EEGSubscriberBox()
