""" Refer back to http://openvibe.inria.fr/tutorial-using-python-with-openvibe/ for how to use openvibe framework """


class EEGClientBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.signal_header = None

    def initialize(self):
        print("Initializing EEG Client Box")

    def process(self):
        eeg_signal_stream = self.input[0]
        while eeg_signal_stream:
            chunk = eeg_signal_stream.pop()

            # signal header is the first chunk of data sent
            # contains startTime, endTime, dimensionSizes, dimensionLabels, samplingRate
            if isinstance(chunk, OVSignalHeader):
                self.signal_header = chunk

            elif isinstance(chunk, OVSignalBuffer):
                # TODO: send chunk over the socket
                pass

            elif isinstance(chunk, OVSignalEnd):
                print("End of signal reached!")

    def uninitialize(self):
        print("Uninitialized EEG Client Box")


box = EEGClientBox()
