import socket
import threading
from _testcapi import get_kwargs
import uuid
import random

from Stomp.Decoder import Decode
from Stomp.Utils import Frames

from Stomp.Encoder import Encode


class Client(object):
    """

    """

    def __init__(self):
        self.encoder = Encode.Encoder()
        self.decoder = Decode.Decoder()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transaction_id = str(uuid.uuid4())

    def connect(self, port, **kwargs):
        connect_frame = self.encoder.encode('CONNECT', **kwargs)
        self.client_socket.connect((kwargs.get('host'), port))
        self.send_frame(str(connect_frame))
        while True:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                self.receive(data)

    def receive(self, msg):
        try:
            frame = self.decoder.decode(msg)
            print 'Client received frame: \n' + str(frame)
            if type(frame) is Frames.CONNECTED:
                pass
        except Exception as ex:
            print ex
            raise

    def send_frame(self,msg):
        print 'Client will send frame: \n' + msg
        totalsent = 0
        while totalsent < len(msg):
            sent = self.client_socket.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def begin(self):
        print 'Client will begin sending frames'
        begin_frame = self.encoder.encode('BEGIN', transaction=self.transaction_id)
        self.send_frame(str(begin_frame))

    def commit(self):
        print 'Client commits sent frames'
        commit_frame = self.encoder.encode('COMMIT', transaction=self.transaction_id)
        self.send_frame(str(commit_frame))

    def abort(self):
        print 'Client aborts'
        abort_frame = self.encoder.encode('ABORT', transaction=self.transaction_id)
        self.send_frame(str(abort_frame))
        self.client_socket.close()

    def send(self, **kwargs):
        send_frame = self.encoder.encode('SEND', **kwargs)
        self.send_frame(str(send_frame))

    def subscribe(self, **kwargs):
        print "Client subscribes"
        subscribe_frame = self.encoder.encode('SUBSCRIBE', **kwargs)
        self.send_frame(str(subscribe_frame))

    def unsubscribe(self, **kwargs):
        print "Client unsubscribes"
        unsubscribe_frame = self.encoder.encode('UNSUBSCRIBE', **kwargs)
        self.send_frame(str(unsubscribe_frame))

if __name__ == '__main__':
    stomp_client = Client()
    t1 = threading.Thread(target=stomp_client.connect,
                          kwargs={'port': 1212, 'accept-version': '1.2,10.1', 'host': 'localhost'})
    t1.start()
    id = 1
    subscribe_id1 = str(id)
    id += 1
    threading._sleep(3)
    stomp_client.begin()
    stomp_client.subscribe(**{'destination': 'foo', 'id': subscribe_id1})
    threading._sleep(3)
    stomp_client.send(**{'destination': 'foo', 'msg': 'First message to foo'})
    stomp_client.commit()
    threading._sleep(3)
    stomp_client.unsubscribe(**{'id': subscribe_id1})

    '''
    msg_frame = stomp_client.encoder.encode('SUBSCRIBE', **{'destination': 'foo', 'id': 0})
    stomp_client.send_frame(str(msg_frame))
    threading._sleep(3)

    msg_frame = stomp_client.encoder.encode('SUBSCRIBE', **{'destination': 'bar', 'id': 0})
    stomp_client.send_frame(str(msg_frame))

    stomp_client_2 = Client()
    t2 = threading.Thread(target=stomp_client_2.connect,
                          kwargs={'port': 1212, 'accept-version': '1.2,10.1', 'host': 'localhost'})
    t2.start()
    threading._sleep(3)
    msg_frame_2 = stomp_client_2.encoder.encode('SUBSCRIBE', **{'destination': 'foo', 'id': 1})
    stomp_client_2.send_frame(str(msg_frame_2))

    threading._sleep(3)
    msg_frame = stomp_client.encoder.encode('SEND', **{'destination': 'foo', 'msg': 'First message to foo'})
    stomp_client.send_frame(str(msg_frame))

    threading._sleep(3)
    msg_frame = stomp_client.encoder.encode('BEGIN', **{'transaction': 'tx1'})
    stomp_client.send_frame(str(msg_frame))

    threading._sleep(3)
    msg_frame = stomp_client.encoder.encode('SEND', **{'destination': 'foo', 'transaction': 'tx1',
                                                       'msg': 'First message to tx1'})
    stomp_client.send_frame(str(msg_frame))

    threading._sleep(3)
    msg_frame = stomp_client.encoder.encode('SEND', **{'destination': 'foo', 'transaction': 'tx1',
                                                       'msg': 'Second message to tx1'})
    stomp_client.send_frame(str(msg_frame))

    threading._sleep(3)
    msg_frame = stomp_client.encoder.encode('COMMIT', **{'transaction': 'tx1'})
    stomp_client.send_frame(str(msg_frame))
    '''
    t1.join()
    #t2.join()