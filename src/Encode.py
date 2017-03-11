from Frames import *


class Encoder(object):
    """
    This class is for encoding STOMP frames.
    """
    def __init__(self):
        pass

    def encode(self,command,**kwargs):
        if command == 'CONNECT':
            frame = self.create_connect_frame(**kwargs)

        return frame

    def create_connect_frame(self,**kwargs):
        connect_frame = CONNECT(**kwargs)
        if not connect_frame.has_required():
            raise Exception('CONNECT frame REQUIRES host and accept-version headers.')
        return connect_frame
