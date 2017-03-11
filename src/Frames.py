

class BaseFrame(object):
    def __init__(self,msg=None):
        self.msg = msg

class CONNECT(BaseFrame):
    """
    headers:
        REQUIRED: accept-version, host
        OPTIONAL: login, passcode, heart-beat
    """
    def __init__(self, accept_version, host, **kwargs):
        BaseFrame.__init__(self)
        self.accept_version = accept_version
        self.host = host
        self.login = kwargs.get('login')
        self.passcode = kwargs.get('passcode')
        self.heartbeat = kwargs.get('heartbeat')

class STOMP(BaseFrame):
    """
    headers:
        REQUIRED: accept-version, host
        OPTIONAL: login, passcode, heart-beat
    """
    def __init__(self, accept_version, host, **kwargs):
        BaseFrame.__init__(self)
        self.accept_version = accept_version
        self.host = host
        self.login = kwargs.get('login')
        self.passcode = kwargs.get('passcode')
        self.heartbeat = kwargs.get('heartbeat')

class CONNECTED(BaseFrame):
    """
    headers:
        REQUIRED: version
        OPTIONAL: session, server, heart-beat
    """
    def __init__(self, version, host, **kwargs):
        BaseFrame.__init__(self)
        self.version = version
        self.login = kwargs.get('session')
        self.passcode = kwargs.get('server')
        self.heartbeat = kwargs.get('heartbeat')

class SEND(BaseFrame):
    """
    headers:
        REQUIRED: destination
        OPTIONAL: transaction
    """
    def __init__(self, destination, **kwargs):
        BaseFrame.__init__(kwargs.get('msg'))
        self.destination = destination
        self.transaction = kwargs.get('transaction')

class SUBSCRIBE(BaseFrame):
    """
    headers:
        REQUIRED: destination, id
        OPTIONAL: ack
    """
    def __init__(self, destination, id, **kwargs):
        BaseFrame.__init__(self)
        self.destination = destination
        self.id = id
        self.ack =  kwargs.get('ack')

class UNSUBSCRIBE(BaseFrame):
    """
    headers:
        REQUIRED: id
        OPTIONAL: none
    """
    def __init__(self, id):
        BaseFrame.__init__(self)
        self.id = id

class ACK(BaseFrame):
    """
    headers:
        REQUIRED: id
        OPTIONAL: transaction
    """
    def __init__(self, id, **kwargs):
        BaseFrame.__init__(self)
        self.id = id
        self.transaction = kwargs.get('transaction')

class NACK(BaseFrame):
    """
    headers:
        REQUIRED: id
        OPTIONAL: transaction
    """
    def __init__(self, id, **kwargs):
        BaseFrame.__init__(self)
        self.id = id
        self.transaction = kwargs.get('transaction')

class BEGIN(BaseFrame):
    """
    headers:
        REQUIRED: transaction
        OPTIONAL: none
    """
    def __init(self, transaction):
        BaseFrame.__init__(self)
        self.transaction = transaction

class COMMIT(BaseFrame):
    """
    headers:
        REQUIRED: transaction
        OPTIONAL: none
    """
    def __init(self, transaction):
        BaseFrame.__init__(self)
        self.transaction = transaction


class ABORT(BaseFrame):
    """
    headers:
        REQUIRED: transaction
        OPTIONAL: none
    """
    def __init(self, transaction):
        BaseFrame.__init__(self)
        self.transaction = transaction


class DISCONNECT(BaseFrame):
    """
    headers:
        REQUIRED: none
        OPTIONAL: receipt
    """
    def __init(self, **kwargs):
        BaseFrame.__init__(self)
        self.receipt = kwargs.get('receipt')


class MESSAGE(BaseFrame):
    """
    headers:
        REQUIRED: destination, message-id, subscription
        OPTIONAL: ack
    """
    def __init__(self, destination, message_id, subscription, **kwargs):
        BaseFrame.__init__(self)
        self.destination = destination
        self.message_id = message_id
        self.subscription = subscription
        self.ack = kwargs.get('ack')

class RECEIPT(BaseFrame):
    """
    headers:
        REQUIRED: receipt-id
        OPTIONAL: none
    """
    def __init__(self, receipt_id):
        BaseFrame.__init__(self)
        self.receipt_id = receipt_id

class ERROR(BaseFrame):
    """
    headers:
        REQUIRED: none
        OPTIONAL: message
    """
    def __init__(self, **kwargs):
        BaseFrame.__init__(self)
        self.message = kwargs.get('message')
