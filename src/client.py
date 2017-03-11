
from Encode import Encoder

class Client(object):
    """

    """

    def __init__(self):
        self.encoder = Encoder()

    def connect(self,accept_version,host,**kwargs):
        connect_frame = self.encoder.encode('CONNECT',accept_version,host,**kwargs)
        self.send_frame(connect_frame)

    def send_frame(self,frame):
        tcp.send(frame)