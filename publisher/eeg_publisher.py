from pynput import keyboard
import socket
import pickle as pkl
from enum import Enum
import pandas as pd


class Command(Enum):
    START = 0
    STOP = 1
    START_EVENT = 2
    STOP_EVENT = 3
    END = 4


SUBSCRIBER_IP = "localhost"
EEG_RECEIVED_COUNT = 0
key_to_command = {"r": Command.START, "s": Command.STOP, "e": Command.END}


# Create a UDP socket
publisher_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
subscriber_address = (SUBSCRIBER_IP, 12345)

old_command: Command = None


def receive_large_data(sock, buffer_size=4096):
    data = bytearray()
    while True:
        part = sock.recv(buffer_size)
        data.extend(part)
        if len(part) < buffer_size:
            break
    return data


def on_press(key):
    global old_command, EEG_RECEIVED_COUNT
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
        print(f"Sending {command}")

        # send the command to the subscriber
        publisher_socket.sendto(pkl.dumps(command), subscriber_address)
        old_command = command

        if command == Command.END:
            # Receive the dataframe from the subscriber
            encoded_df = receive_large_data(publisher_socket)
            eeg_df = pkl.loads(encoded_df)
            print("Received dataframe from subscriber")

            # Save the dataframe to a csv file
            eeg_df.to_csv(f"eeg_data_{EEG_RECEIVED_COUNT}.csv", index=False)
            EEG_RECEIVED_COUNT += 1
            print(f"Saved dataframe_{EEG_RECEIVED_COUNT} to csv file")


import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go


def plot_df(df, title):
    # Ensure 'timestamp' column is in the correct datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig = sp.make_subplots(
        rows=32,
        cols=1,
        subplot_titles=[f"channel_{i}" for i in range(32)],
        shared_xaxes=True,
        vertical_spacing=0.01,
    )

    for i in range(32):  # assuming 'channel_0' to 'channel_31' are the channel columns
        # Prepare color array for the given channel
        colors = df["event"].map({True: "red", False: "blue"})

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df[f"channel_{i}"],
                name=f"Channel {i}",
                showlegend=False,
                mode="lines",
                line=dict(color="DarkSlateGrey"),
            ),
            row=i + 1,  # subplot row index
            col=1,  # subplot column index
        )

        # Add the event markers to the plot
        event_points = df[df["event"] == True]
        fig.add_trace(
            go.Scatter(
                x=event_points["timestamp"],
                y=event_points[f"channel_{i}"],
                name=f"Channel {i}",
                showlegend=False,
                mode="lines",
                line=dict(color="#d62728"),
            ),
            row=i + 1,  # subplot row index
            col=1,  # subplot column index
        )

    fig.update_layout(
        height=2300,
        autosize=True,
        width=None,
        title_text=title,
        showlegend=False,
        yaxis=dict(fixedrange=True),
    )

    fig.show()


def on_release(key):
    if key == keyboard.Key.esc:
        # Close the socket
        publisher_socket.close()

        # Visualize the dataframes
        for i in range(EEG_RECEIVED_COUNT):
            eeg_df = pd.read_csv(f"eeg_data_{i}.csv")
            # Plot timeseries of the eeg data for each channel
            plot_df(eeg_df, f"EEG Data {i}")

        # Stop listener
        return False


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
