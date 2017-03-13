
from Encode import Encoder
from Decode import Decoder
import Frames
import socket
import threading

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
            print 'Client received frame: \n' + str(frame)
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
    t1 = threading.Thread(target=stomp_client.connect,
                          kwargs={'port':1212,'accept-version':'1.2,10.1','host':'localhost'})
    t1.start()
    threading._sleep(5)
    msg_frame = stomp_client.encoder.encode('SUBSCRIBE', **{'destination': 'foo', 'id': 0})
    stomp_client.send(str(msg_frame))
    threading._sleep(5)

    stomp_client_2 = Client()
    t2 = threading.Thread(target=stomp_client_2.connect,
                          kwargs={'port': 1212, 'accept-version': '1.2,10.1', 'host': 'localhost'})
    t2.start()
    threading._sleep(5)
    msg_frame_2 = stomp_client_2.encoder.encode('SUBSCRIBE', **{'destination': 'foo', 'id': 1})
    stomp_client_2.send(str(msg_frame_2))

    threading._sleep(5)
    msg_frame = stomp_client.encoder.encode('SEND',**{'destination': 'foo','msg': 'First message to foo'})
    stomp_client.send(str(msg_frame))

    t1.join()
    t2.join()