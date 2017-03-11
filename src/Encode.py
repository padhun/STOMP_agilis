
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
        accept_version = kwargs.get('accept_version')
        host = kwargs.get('host')
        if accept_version is None or host is None:
            raise Exception('CONNECT frame REQUIRES host and accept-version headers.')

        login = kwargs.get('login')
        passcode = kwargs.get('passcode ')
        heartbeat = kwargs.get('heartbeat')

        connect_frame = CONNECT(accept_version,host,login=login,passcode=passcode,heartbeat=heartbeat)
        return connect_frame
