
from Encode import Encoder
from Decode import Decoder
import Frames
import socket

class Client(object):
    """

    """

    def __init__(self):
        self.encoder = Encoder()
        self.decoder = Decoder()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self,port,**kwargs):
        connect_frame = self.encoder.encode('CONNECT',**kwargs)
        self.client_socket.connect((kwargs.get('host'),port))
        self.send(str(connect_frame))
        while True:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                self.receive(data)

    def receive(self,msg):
        try:
            frame = self.decoder.decode(msg)
            print 'Client received frame: ' + str(frame)
            if type(frame) is Frames.CONNECTED:
                pass
        except Exception as ex:
            print ex
            raise

    def send(self,msg):
        print 'Client will send frame: \n' + msg
        totalsent = 0
        while totalsent < len(msg):
            sent = self.client_socket.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent


if __name__ == '__main__':
    stomp_client = Client()
    stomp_client.connect(**{'port':1212,'accept-version':'1.2,10.1','host':'localhost'})