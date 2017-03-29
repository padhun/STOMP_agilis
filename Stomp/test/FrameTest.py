import unittest

from Stomp.Utils import Frames

from Stomp.Encoder import Encode


class TestUM(unittest.TestCase):

    def setUp(self):
        self.encoder = Encode.Encoder()
#        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def test_encoder_get_frame_class_send(self):
        command = 'SEND'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.SEND)

    def test_encoder_get_frame_class_subscribe(self):
        command = 'SUBSCRIBE'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.SUBSCRIBE)
    def test_encoder_get_frame_class_unsubscribe(self):
        command = 'UNSUBSCRIBE'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.UNSUBSCRIBE)

    def test_encoder_get_frame_class_begin(self):
        command = 'BEGIN'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.BEGIN)

    def test_encoder_get_frame_class_commit(self):
        command = 'COMMIT'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.COMMIT)

    def test_encoder_get_frame_class_abort(self):
        command = 'ABORT'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.ABORT)

    def test_encoder_get_frame_class_ack(self):
        command = 'ACK'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.ACK)


    def test_encoder_get_frame_class_nack(self):
        command = 'NACK'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.NACK)

    def test_encoder_get_frame_class_disconnect(self):
        command = 'DISCONNECT'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.DISCONNECT)

    def test_encoder_get_frame_class_connect(self):
        command = 'CONNECT'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.CONNECT)

    def test_encoder_get_frame_class_stomp(self):
        command = 'STOMP'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.STOMP)

    def test_encoder_get_frame_class_connected(self):
        command = 'CONNECTED'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.CONNECTED)

    def test_encoder_get_frame_class_message(self):
        command = 'MESSAGE'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.MESSAGE)

    def test_encoder_get_frame_class_receipt(self):
        command = 'RECEIPT'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.RECEIPT)


    def test_encoder_get_frame_class_error(self):
        command = 'ERROR'
        self.assertEquals(self.encoder.get_frame_class(command), Frames.ERROR)

    def test_encoder_invalid_frame_class(self):
        command = '---'
        self.assertRaises(RuntimeError, self.encoder.get_frame_class, command)

if __name__ == '__main__':
    unittest.main()
