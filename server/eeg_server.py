class EEGServerBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.signal_header = None

    def initialize(self):
        print("Initializing EEG Server Box")

    def process(self):
        pass

    def uninitialize(self):
        print("Uninitialized EEG Server Box")


box = EEGServerBox()
