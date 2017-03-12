
import Frames
from Decode import Decoder
from Encode import Encoder
import socket

class Server(object):
    """

    """

    def __init__(self):
        self.decoder = Decoder()
        self.encoder = Encoder()
        self.supported_versions = ['1.2']
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self,msg,connection):
        try:
            frame = self.decoder.decode(msg)
            print 'Server received frame: ' + str(frame)
            if type(frame) is Frames.CONNECT:
                self.connect_request_received(frame,connection)
        except Exception as ex:
            print ex
            raise

    def connect_request_received(self,request_frame,connection):
        common_versions = list(set(request_frame.headers['accept-version'].split(',')).intersection(self.supported_versions))
        if len(common_versions) == 0:
            error_message = 'Supported protocol versions are ' + str(self.supported_versions)
            error_frame = self.encoder.encode('ERROR',**{'msg' : error_message})
            self.respond(str(error_frame),connection)
            raise Exception("The client and server do not share any common protocol versions")
        else:
            connected_frame = self.encoder.encode('CONNECTED',**{'version' : max(common_versions)})
            self.respond(str(connected_frame),connection)

    def respond(self,msg,connection):
        print 'Server will send frame: \n' + msg
        totalsent = 0
        while totalsent < len(msg):
            sent = connection.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def start(self,address,port):
        try:
            # bind the socket to localhost, and STOMP port
            self.serversocket.bind((address, port))
            print 'Server started at: ' + address + ':' + str(port)
            print 'Server supports STOMP version: ' + str(self.supported_versions)
            # become a server socket
            self.serversocket.listen(5)
            while True:
                # accept connections from outside
                (connection, address) = self.serversocket.accept()

                while True:
                    try:
                        data = connection.recv(1024)
                        if not data:
                            break
                        self.receive(data,connection)
                    except Exception:
                        connection.close()
        finally:
            self.serversocket.close()


if __name__ == '__main__':
    stomp_server = Server()
    stomp_server.start('localhost',1212)