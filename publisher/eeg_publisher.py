from pynput import keyboard
import socket
import pickle as pkl
from enum import Enum


class Command(Enum):
    START = 0
    STOP = 1
    START_EVENT = 2
    STOP_EVENT = 3
    END = 4


key_to_command = {"r": Command.START, "s": Command.STOP}


# Create a UDP socket
publisher_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
subscriber_address = ("localhost", 12345)

old_command: Command = None


def on_press(key):
    global old_command
    command: Command = None
    try:
        if key == keyboard.Key.space:
            if old_command == Command.START_EVENT:
                command = Command.STOP_EVENT
            else:
                command = Command.START_EVENT
        else:
            command = key_to_command.get(key.char)
    except AttributeError:
        pass

    if command:
        print(f"Sending command {command}")
        # send the key to the subscriber
        publisher_socket.sendto(pkl.dumps(command), subscriber_address)
        old_command = command


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
