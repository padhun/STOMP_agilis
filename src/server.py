
import Frames
from Decode import Decoder
from Encode import Encoder
import socket
import threading
import thread

class Server(object):
    """
    Server class for STOMP server functionality.
    Listen on a given socket and respond to STOMP clients depends on the input message.
    """

    def __init__(self):
        """
        Server class initialization.
        decoder: Decoder class object. Supports making STOMP frames from TCP messages.
        encoder: Encoder class object. Supports making STOMP frames from commands.
        supported_versions: tells which STOMP version supported by the server.
        serversocket: TCP socket for the communication
        """
        self.decoder = Decoder()
        self.encoder = Encoder()
        self.supported_versions = ['1.2']
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_pool = []

    def receive(self,msg,connection):
        """
        This method called when the server get a message from a client.
        First it decodes the msg to a frame. After that call a function depends on the frame's command.
        :param msg: received TCP message
        :param connection: active TCP connection with one of the client
        :return:
        """
        try:
            frame = self.decoder.decode(msg)
            print 'Server received frame: \n' + str(frame) + '\n'
            self.requests.get(type(frame).__name__)(self,frame,connection)
        except Exception:
            raise

    def connect_received(self,request_frame,connection):
        """
        This method called when the server get CONNECT frame.
        If the client and server do not share any common protocol versions, raise an exception
        else the server responds with CONNECTED frame.
        :param request_frame: Decoded frame from client message
        :param connection: active TCP connection with one of the client
        :return:
        """
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
        """
        This method called when the client sends frame, which need some respond.
        :param msg: STOMP frame as a string
        :param connection: active TCP connection with one of the client
        :return:
        """
        print 'Server will send frame: \n' + msg
        totalsent = 0
        while totalsent < len(msg):
            sent = connection.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def start(self,address,port):
        """
        This function starts the listening on the given address and port.
        :param address: Address server listening on
        :param port: Port server listening on
        :return:
        """
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
                t = threading.Thread(target=self.run_client_thread,kwargs={'connection': connection, 'address': address})
                self.connection_pool.append(t)
                t.start()
                #t.join()
        finally:
            self.serversocket.close()

    def run_client_thread(self,connection,address):
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                self.receive(data, connection)
            except Exception as ex:
                print ex
                connection.close()

    def disconnect_received(self,request_frame,connection):
        pass

    def send_received(self,request_frame,connection):
        msg_frame = self.encoder.encode('MESSAGE',**{'destination':'foo','message-id': '0','subscription':'0','msg':request_frame.msg})
        self.respond(str(msg_frame),connection)

    def subscribe_received(self,request_frame,connection):
        pass

    def unsubscribe_received(self,request_frame,connection):
        pass

    requests = {
        'CONNECT': connect_received,
        'DISCONNECT': disconnect_received,
        'SEND': send_received,
        'SUBSCRIBE': subscribe_received,
        'UNSUBSCRIBE': unsubscribe_received
        #'ACK': ack_received,
        #'NACK': nack_received,
        #'ABORT': abort_received,
        #'COMMIT': commit_received,
        #'BEGIN': begin_received,
        #'STOMP': stomp_received,
    }


if __name__ == '__main__':
    stomp_server = Server()
    stomp_server.start('localhost',1212)