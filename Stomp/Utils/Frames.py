"""
client-command      = "SEND"
                      | "SUBSCRIBE"
                      | "UNSUBSCRIBE"
                      | "BEGIN"
                      | "COMMIT"
                      | "ABORT"
                      | "ACK"
                      | "NACK"
                      | "DISCONNECT"
                      | "CONNECT"
                      | "STOMP"

server-command      = "CONNECTED"
                      | "MESSAGE"
                      | "RECEIPT"
                      | "ERROR"
"""
from util import replace_all

NULL = '\x00'
ESCAPE = {'\n':r"\n",'\r':r"\r",':':r"\c", '\\':"\\\\"}
UNESCAPE = {r"\n":'\n',r"\r":'\r',r"\c":':', "\\\\":'\\'}

class BaseFrame(object):
    # TODO: Handle optional headers
    headers={}
    required_headers=()

    def __init__(self,**kwargs):
        self.msg = None
        self.headers = {}
        if kwargs.has_key('msg'):
            self.msg = kwargs.pop('msg')
        self.headers.update(**kwargs)

    def has_required(self):
        if set(self.required_headers) <= self.headers.viewkeys():
            return True
        else:
            return False

    def __str__(self):
        """
        """
        ascii_command = FRAMES.keys()[FRAMES.values().index(type(self))] + '\n'
        ascii_headers = ''
        ascii_msg = ''
        for k, v in self.headers.iteritems():
            ascii_headers += replace_all(ESCAPE, str(k)) + ':' + replace_all(ESCAPE, str(v)) + '\n'
        ascii_headers += '\n'
        if self.msg is not None:
            ascii_msg = self.msg
        ascii_frame = ascii_command + ascii_headers + ascii_msg + (NULL if NULL not in ascii_msg else '')
        return ascii_frame

class CONNECT(BaseFrame):
    """
    A STOMP client initiates the stream or TCP connection to the server by sending the CONNECT or STOMP frame
    headers:
        REQUIRED: accept-version, host
        OPTIONAL: login, passcode, heart-beat
    """
    required_headers=("accept-version","host",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class STOMP(CONNECT):
    """
    A STOMP client initiates the stream or TCP connection to the server by sending the CONNECT or STOMP frame
    headers:
        REQUIRED: accept-version, host
        OPTIONAL: login, passcode, heart-beat
    """


class CONNECTED(BaseFrame):
    """
    Stomp server sends CONNECTED frame, if it accepts the connection request.
    headers:
        REQUIRED: version
        OPTIONAL: session, server, heart-beat
    """
    required_headers=("version",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class SEND(BaseFrame):
    """
    The SEND frame sends a message to a destination in the messaging system.
    It has one REQUIRED header, destination, which indicates where to send the message.
    The body of the SEND frame is the message to be sent.
    headers:
        REQUIRED: destination
        OPTIONAL: transaction
    """
    required_headers=("destination",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class SUBSCRIBE(BaseFrame):
    """
    The SUBSCRIBE frame is used to register to listen to a given destination.
    Like the SEND frame, the SUBSCRIBE frame requires a destination header
    indicating the destination to which the client wants to subscribe.
    Any messages received on the subscribed destination will henceforth be delivered as MESSAGE frames from the server
    to the client. The ack header controls the message acknowledgment mode.
    headers:
        REQUIRED: destination, id
        OPTIONAL: ack
    """
    required_headers=("destination", "id",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class UNSUBSCRIBE(BaseFrame):
    """
    The UNSUBSCRIBE frame is used to remove an existing subscription.
    Once the subscription is removed the STOMP connections will no longer receive messages from that subscription.
    Since a single connection can have multiple open subscriptions with a server,
    an id header MUST be included in the frame to uniquely identify the subscription to remove.
    This header MUST match the subscription identifier of an existing subscription.
    headers:
        REQUIRED: id
        OPTIONAL: none
    """
    required_headers=("id",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class ACK(BaseFrame):
    """
    ACK is used to acknowledge consumption of a message
    from a subscription using client or client-individual acknowledgment.
    Any messages received from such a subscription
    will not be considered to have been consumed until the message has been acknowledged via an ACK.
    headers:
        REQUIRED: id
        OPTIONAL: transaction
    """
    required_headers=("id",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class NACK(BaseFrame):
    """
    NACK is the opposite of ACK. It is used to tell the server that the client did not consume the message.
    The server can then either send the message to a different client, discard it, or put it in a dead letter queue.
    The exact behavior is server specific.
    headers:
        REQUIRED: id
        OPTIONAL: transaction
    """
    required_headers=("id",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class BEGIN(BaseFrame):
    """
    BEGIN is used to start a transaction. Transactions in this case apply to sending and acknowledging -
    any messages sent or acknowledged during a transaction will be processed atomically based on the transaction.
    headers:
        REQUIRED: transaction
        OPTIONAL: none
    """
    required_headers=("transaction",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class COMMIT(BaseFrame):
    """
    COMMIT is used to commit a transaction in progress.
    headers:
        REQUIRED: transaction
        OPTIONAL: none
    """
    required_headers=("transaction",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class ABORT(BaseFrame):
    """
    ABORT is used to roll back a transaction in progress.
    headers:
        REQUIRED: transaction
        OPTIONAL: none
    """
    required_headers=("transaction",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class DISCONNECT(BaseFrame):
    """
    A client can disconnect from the server at anytime by closing the socket but
    there is no guarantee that the previously sent frames have been received by the server.
    To do a graceful shutdown the client send DISCONNECT frame.
    headers:
        REQUIRED: none
        OPTIONAL: receipt
    """

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class MESSAGE(BaseFrame):
    """
    MESSAGE frames are used to convey messages from subscriptions to the client.
    The MESSAGE frame MUST include a destination header indicating the destination the message was sent to.
    If the message has been sent using STOMP,
    this destination header SHOULD be identical to the one used in the corresponding SEND frame.
    The MESSAGE frame MUST also contain a message-id header with a unique identifier for that message
    and a subscription header matching the identifier of the subscription that is receiving the message.
    headers:
        REQUIRED: destination, message-id, subscription
        OPTIONAL: ack
    """
    required_headers=("destination", "message-id", "subscription",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class RECEIPT(BaseFrame):
    """
    A RECEIPT frame is sent from the server to the client once
    a server has successfully processed a client frame that requests a receipt.
    A RECEIPT frame MUST include the header receipt-id,
    where the value is the value of the receipt header in the frame which this is a receipt for.
    headers:
        REQUIRED: receipt-id
        OPTIONAL: none
    """
    required_headers=("receipt-id",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class ERROR(BaseFrame):
    """
    The server MAY send ERROR frames if something goes wrong. In this case,
    it MUST then close the connection just after sending the ERROR frame.
    The ERROR frame SHOULD contain a message header with a short description of the error,
    and the body MAY contain more detailed information (or MAY be empty).
    headers:
        REQUIRED: none
        OPTIONAL: message
    """

    def __init__(self, **kwargs):
        BaseFrame.__init__(self,**kwargs)

FRAMES={
    "CONNECT":CONNECT,
    "STOMP":STOMP,
    "CONNECTED":CONNECTED,
    "SEND":SEND,
    "SUBSCRIBE":SUBSCRIBE,
    "UNSUBSCRIBE":UNSUBSCRIBE,
    "ACK":ACK,
    "NACK":NACK,
    "BEGIN":BEGIN,
    "COMMIT":COMMIT,
    "ABORT":ABORT,
    "DISCONNECT":DISCONNECT,
    "MESSAGE":MESSAGE,
    "RECEIPT":RECEIPT,
    "ERROR":ERROR
}

