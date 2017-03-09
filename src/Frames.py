

class BaseFrame(object):
    def __init__(self,msg=None):
        self.msg = msg

class CONNECT(BaseFrame):
    """
    headers:
        REQUIRED: accept-version, host
        OPTIONAL: login, passcode, heart-beat
    """

class STOMP(BaseFrame):
    """
    headers:
        REQUIRED: accept-version, host
        OPTIONAL: login, passcode, heart-beat
    """

class CONNECTED(BaseFrame):
    """
    headers:
        REQUIRED: version
        OPTIONAL: session, server, heart-beat
    """

class SEND(BaseFrame):
    """
    headers:
        REQUIRED: destination
        OPTIONAL: transaction
    """

class SUBSCRIBE(BaseFrame):
    """
    headers:
        REQUIRED: destination, id
        OPTIONAL: ack
    """

class UNSUBSCRIBE(BaseFrame):
    """
    headers:
        REQUIRED: id
        OPTIONAL: none
    """

class ACK(BaseFrame):
    """
    headers:
        REQUIRED: id
        OPTIONAL: transaction
    """

class NACK(BaseFrame):
    """
    headers:
        REQUIRED: id
        OPTIONAL: transaction
    """

class BEGIN(BaseFrame):
    """
    headers:
        REQUIRED: transaction
        OPTIONAL: none
    """

class COMMIT(BaseFrame):
    """
    headers:
        REQUIRED: transaction
        OPTIONAL: none
    """

class ABORT(BaseFrame):
    """
    headers:
        REQUIRED: transaction
        OPTIONAL: none
    """

class DISCONNECT(BaseFrame):
    """
    headers:
        REQUIRED: none
        OPTIONAL: receipt
    """

class MESSAGE(BaseFrame):
    """
    headers:
        REQUIRED: destination, message-id, subscription
        OPTIONAL: ack
    """

class RECEIPT(BaseFrame):
    """
    headers:
        REQUIRED: receipt-id
        OPTIONAL: none
    """

class ERROR(BaseFrame):
    """
    headers:
        REQUIRED: none
        OPTIONAL: message
    """
