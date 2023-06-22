""" Refer back to http://openvibe.inria.fr/tutorial-using-python-with-openvibe/ for how to use openvibe framework """

from openvibe import OVBox
import socket


class EEGClientBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)

    # The process method will be called by openvibe on every clock tick
    def process(self) -> None:
        pass


box = EEGClientBox()
