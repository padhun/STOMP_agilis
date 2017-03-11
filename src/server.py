
from Frames import *
from Decode import Decoder
from Encode import Encoder

class Server(object):
    """

    """

    def __init__(self):
        self.decoder = Decoder()
        self.encoder = Encoder()
        self.supported_versions = ['1.2']

    def listener(self,msg):
        frame = self.decoder.decode(msg)
        if type(frame) is CONNECT:
            self.connect_request_received(frame)

    def connect_request_received(self,request_frame):
        pass

