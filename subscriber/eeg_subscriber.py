from enum import Enum
import pandas as pd
import socket
import threading
import pickle as pkl
import time
import numpy as np


class State(Enum):
    STAND_BY = 0
    RECORDING = 1


class Command(Enum):
    START = 0
    STOP = 1
    START_EVENT = 2
    STOP_EVENT = 3
    END = 4


CHANNEL_COUNT = 32


class EEGSubscriberBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)

        self.udp_socket: socket.socket
        self.state: State = State.STAND_BY
        self.event = False
        self.command_thread: threading.Thread
        self.eeg_signal_header: OVSignalHeader
        self.eeg_df = pd.DataFrame(
            columns=["event", "timestamp"]
            + [f"channel_{i}" for i in range(CHANNEL_COUNT)]
        )

    def _process_commands(self):
        print("Thread to process commands started")

        try:
            while True:
                print("Waiting for command")
                encoded_command, publisher_address = self.udp_socket.recvfrom(4096)
                command = pkl.loads(encoded_command)
                print(f"Received command {command}")

                if self.state == State.STAND_BY and command == Command.START:
                    self.state = State.RECORDING
                    print("Started recording")

                elif self.state == State.RECORDING and command == Command.STOP:
                    self.state = State.STAND_BY
                    print("Stopped recording")

                elif self.state == State.RECORDING and command == Command.START_EVENT:
                    self.event = True
                    print("Started Event recorded")

                elif self.state == State.RECORDING and command == Command.STOP_EVENT:
                    self.event = False
                    print("Stopped Event recorded")

                elif command == Command.END:
                    print("Received End command")

                    # Send the dataframe to the publisher
                    self.send_large_data(
                        self.udp_socket, pkl.dumps(self.eeg_df), self.publisher_address
                    )

                    print("Sent dataframe to publisher")
                    # Clears the dataframe but keeps the columns
                    self.eeg_df = self.eeg_df[0:0]

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
        subscriber_address = ("localhost", 12345)
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
        import os
        import inspect

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(inspect.stack()[0].filename))

        # Create the file path for the CSV file
        csv_file_path = os.path.join(script_dir, "eeg_dataset.csv")

        # Save the dataset to a csv file
        self.eeg_df.to_csv(csv_file_path, index=False)


box = EEGSubscriberBox()
