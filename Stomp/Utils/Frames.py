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
    headers = {}
    required_headers = ()

    def __init__(self, **kwargs):
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
    headers:
        REQUIRED: accept-version, host
        OPTIONAL: login, passcode, heart-beat
    """
    required_headers = ("accept-version","host",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class STOMP(BaseFrame):
    """
    headers:
        REQUIRED: accept-version, host
        OPTIONAL: login, passcode, heart-beat
    """
    required_headers = ("accept-version", "host",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class CONNECTED(BaseFrame):
    """
    headers:
        REQUIRED: version
        OPTIONAL: session, server, heart-beat
    """
    required_headers = ("version",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class SEND(BaseFrame):
    """
    headers:
        REQUIRED: destination
        OPTIONAL: transaction
    """
    required_headers = ("destination",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class SUBSCRIBE(BaseFrame):
    """
    headers:
        REQUIRED: destination, id
        OPTIONAL: ack
    """
    required_headers = ("destination", "id",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class UNSUBSCRIBE(BaseFrame):
    """
    headers:
        REQUIRED: id
        OPTIONAL: none
    """
    required_headers = ("id",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class ACK(BaseFrame):
    """
    headers:
        REQUIRED: id
        OPTIONAL: transaction
    """
    required_headers = ("id",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class NACK(BaseFrame):
    """
    headers:
        REQUIRED: id
        OPTIONAL: transaction
    """
    required_headers = ("id",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class BEGIN(BaseFrame):
    """
    headers:
        REQUIRED: transaction
        OPTIONAL: none
    """
    required_headers = ("transaction",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class COMMIT(BaseFrame):
    """
    headers:
        REQUIRED: transaction
        OPTIONAL: none
    """
    required_headers = ("transaction",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class ABORT(BaseFrame):
    """
    headers:
        REQUIRED: transaction
        OPTIONAL: none
    """
    required_headers = ("transaction",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class DISCONNECT(BaseFrame):
    """
    headers:
        REQUIRED: none
        OPTIONAL: receipt
    """

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class MESSAGE(BaseFrame):
    """
    headers:
        REQUIRED: destination, message-id, subscription
        OPTIONAL: ack
    """
    required_headers = ("destination", "message-id", "subscription",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class RECEIPT(BaseFrame):
    """
    headers:
        REQUIRED: receipt-id
        OPTIONAL: none
    """
    required_headers = ("receipt-id",)

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)


class ERROR(BaseFrame):
    """
    headers:
        REQUIRED: none
        OPTIONAL: message
    """

    def __init__(self, **kwargs):
        BaseFrame.__init__(self, **kwargs)

FRAMES = {
    "CONNECT": CONNECT,
    "STOMP": STOMP,
    "CONNECTED": CONNECTED,
    "SEND": SEND,
    "SUBSCRIBE": SUBSCRIBE,
    "UNSUBSCRIBE": UNSUBSCRIBE,
    "ACK": ACK,
    "NACK": NACK,
    "BEGIN": BEGIN,
    "COMMIT": COMMIT,
    "ABORT": ABORT,
    "DISCONNECT": DISCONNECT,
    "MESSAGE": MESSAGE,
    "RECEIPT": RECEIPT,
    "ERROR": ERROR
}
