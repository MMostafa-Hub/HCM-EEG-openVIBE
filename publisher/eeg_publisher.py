import keyboard
import threading
import socket
import pickle as pkl
from enum import Enum
import time


class Command(Enum):
    START = 0
    STOP = 1
    EVENT = 2


key_to_command = {"r": Command.START, "s": Command.STOP, "space": Command.EVENT}


# Create a UDP socket
publisher_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
publisher_address = ("localhost", 12345)


class KeyListener(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(KeyListener, self).__init__(*args, **kwargs)
        self.daemon = True  # Set the Thread as Daemon so it automatically closes when the main program ends
        self.key = None

    def run(self):
        while True:
            self.key = keyboard.read_key()
            if str(self.key) in key_to_command.keys():
                print(f"Pressed {self.key}")
                # send the key to the subscriber
                publisher_socket.sendto(
                    pkl.dumps(key_to_command[str(self.key)]), publisher_address
                )
            self.key = None


def main():
    key_thread = KeyListener()
    key_thread.start()

    while True:  # Keep the main thread alive
        time.sleep(0.2)


if __name__ == "__main__":
    main()
