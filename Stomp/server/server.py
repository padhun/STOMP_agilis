import socket
import threading

from Stomp.Decoder import Decode
from Stomp.Encoder import Encode


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
        server-command      = "CONNECTED"
                            | "MESSAGE"
                            | "RECEIPT"
                            | "ERROR"
        """
        self.decoder = Decode.Decoder()
        self.encoder = Encode.Encoder()
        self.supported_versions = ['1.2']
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_pool = []
        self.subscriptions = []
        self.transactions = []
        self.messages = []

    def receive(self, msg, connection):
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
            self.requests.get(type(frame).__name__)(self, frame, connection)
        except Exception:
            raise

    def connect_frame_received(self, request_frame, connection):
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
            self.error(error_message, connection)
        else:
            connected_frame = self.encoder.encode('CONNECTED', **{'version': max(common_versions)})
            self.respond(str(connected_frame), connection)

    def respond(self, msg, connection):
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

    def start(self, address, port):
        """
        This function starts the listening on the given address and port.
        Creates a new thread after every TCP connection
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
                (connection, client_address) = self.serversocket.accept()
                t = threading.Thread(target=self.run_client_thread,kwargs={'connection': connection, 'address': client_address})
                self.connection_pool.append(t)
                t.start()
                #t.join()
        finally:
            self.serversocket.close()

    def run_client_thread(self, connection, address):
        """
        This method is waiting for messages from client.
        :param connection: TCP connection variable
        :param address: Client address variable
        :return:
        """
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                self.receive(data, connection)
            except Exception as ex:
                connection.close()
                raise

    def disconnect_frame_received(self, request_frame, connection):
        """
        A graceful shutdown, where if the client is assured that all previous frames have been received by the server,
        then DISCONNECT frame contains receipt header. In that case server has to reply with RECEIPT frame,
        with the given id.
        If client has active subscription, remove it.
        :param request_frame: received DISCONNECT frame
        :param connection: TCP connection variable with the client
        :return:
        """
        if 'receipt' in request_frame.headers:
            self.receipt(request_frame.headers['receipt'], connection)
        else:
            connection.close()
        for sub in self.subscriptions:
            if sub['connection'] == connection:
                self.subscriptions.remove(sub)

    def receipt(self, receipt_id, connection):
        """
        A RECEIPT frame is sent from the server to the client once a server has successfully processed a client frame
        that requests a receipt. A RECEIPT frame MUST include the header receipt-id.
        :param receipt_id:  the value is the value of the receipt header in the frame which this is a receipt for
        :param connection: TCP connection variable
        :return:
        """
        receipt_frame = self.encoder.encode('RECEIPT', **{'receipt-id': str(receipt_id)})
        self.respond(str(receipt_frame), connection)

    def send_frame_received(self, request_frame, connection):
        """
        When STOMP server receive SEND frame, this method forwards the frame to the right clients.
        Check who is subscribed on the destination. Not allowed, to resend the message to the owner client.
        :param request_frame: received SEND frame
        :param connection: TCP connection variable, where the message came from
        :return:
        """
        message_id = 0  # TODO generate random unique message ID
        for sub in self.subscriptions:
            if sub['destination'] == request_frame.headers['destination'] and sub['connection'] != connection:
                msg_frame = self.encoder.encode('MESSAGE', **{'destination': request_frame.headers['destination'],
                                                              'message-id': message_id, 'subscription': sub['id'],
                                                              'msg': request_frame.msg})
                if 'transaction' in request_frame.headers:
                    msg_frame.headers['transaction'] = request_frame.headers['transaction']

                if any(connection == m['client'] for m in self.messages):
                    for m in self.messages:
                        if m['client'] == connection:
                            m['messages'].append(message_id)
                else:
                    self.messages.append({'ids': [message_id], 'client': connection})

                self.respond(str(msg_frame), sub['connection'])
        self.receipt('message-'+str(message_id), connection)

    def subscribe_frame_received(self, request_frame, connection):
        """
        Check if there is a subscription with the same id. If yes send an error message.
        Else make the subscription, and append to the subscription list.
        :param request_frame: received SUBSCRIBE frame from client
        :param connection: TCP connection variable
        :return:
        """
        if any(int(request_frame.headers['id']) == s['id'] and
                request_frame.headers['destination'] == s['destination'] for s in self.subscriptions):
            error_message = 'Given SUBSCRIBE id: ' + request_frame.headers['id'] + ' already registered'
            self.error(error_message, connection)
        else:
            subscription = {'id': int(request_frame.headers['id']), 'destination': request_frame.headers['destination'],
                            'connection': connection, 'ack': 'auto'}
            if 'ack' in request_frame.headers:
                subscription['ack'] = request_frame.headers['ack']
            self.subscriptions.append(subscription)

    def unsubscribe_frame_received(self, request_frame, connection):
        """
        If no subscription with the received id, send error message.
        If the subscription is in the list, but its not belongs to this client, send error message.
        If everything is ok, remove subscription from the list.
        :param request_frame: Received UNSUBSCRIBE frame
        :param connection: TCP connection variable
        :return:
        """
        if not any(int(request_frame.headers['id']) == s['id'] for s in self.subscriptions):
            error_message = 'Given SUBSCRIBE id: ' + request_frame.headers['id'] + ' is NOT registered'
            self.error(error_message, connection)
        else:
            for sub in self.subscriptions:
                if sub['id'] == request_frame.headers['id']:
                    if sub['connection'] != connection:
                        error_message = 'Given SUBSCRIBE id: ' + request_frame.headers['id'] + ' is NOT blongs to you'
                        self.error(error_message, connection)
                    else:
                        self.subscriptions.remove(sub)

    def error(self, error_msg, connection):
        """
        Crete ERROR Frame if something went wrong. Raise exception with error message.
        :param error_msg: Error message. What went wrong.
        :param connection: TCP connection variable
        :return:
        """
        error_frame = self.encoder.encode('ERROR', **{'msg': error_msg})
        self.respond(str(error_frame), connection)
        # raise RuntimeError(error_msg)

    def begin_received(self, request_frame, connection):
        """
        BEGIN frame received. Store the transaction informations if there is no other transaction
        with the same id from the same client.
        :param request_frame: Received BEGIN frame
        :param connection: TCP connection variable
        :return:
        """
        if any(int(request_frame.headers['transaction']) == t['transaction'] and
               connection == t['beginner'] for t in self.transactions):
            error_message = 'Given Transaction id: ' + request_frame.headers['transaction'] + ' is already registered'
            self.error(error_message, connection)
        else:
            self.transactions.append({'id': request_frame.headers['transaction'], 'beginner': connection})

    def ack_nack_received(self, request_frame):
        """
        If ACK or NACK frame contains transaction header, forward the frame to the client who started the transaction
        Else ACK or NACK the message, sender client comes from messages list
        :param request_frame: Received ACK or NACK frame
        :return:
        """
        if 'transaction' in request_frame.headers:
            for transaction in self.transactions:
                if transaction['id'] == request_frame.headers['transaction']:
                    self.respond(str(request_frame), transaction['beginner'])
        else:
            for m in self.messages:
                if any(request_frame.headers['id'] == i for i in m['ids']):
                    self.respond(str(request_frame),m['client'])

    def commit_abort_received(self, request_frame, connection):
        """

        :param request_frame:
        :param connection:
        :return:
        """
        pass


    requests = {
        'CONNECT': connect_frame_received,
        'STOMP': connect_frame_received,
        'DISCONNECT': disconnect_frame_received,
        'SEND': send_frame_received,
        'SUBSCRIBE': subscribe_frame_received,
        'UNSUBSCRIBE': unsubscribe_frame_received,
        'ACK': ack_nack_received,
        'NACK': ack_nack_received,
        'ABORT': commit_abort_received,
        'COMMIT': commit_abort_received,
        'BEGIN': begin_received,
    }


if __name__ == '__main__':
    stomp_server = Server()
    stomp_server.start('localhost', 1212)