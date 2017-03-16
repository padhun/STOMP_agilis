import unittest
from Decode import Decoder
import Frames

class TestDecoder(unittest.TestCase):
    """
    """
    def setUp(self):
        self.decoder = Decoder()

    def test_decoder_get_frame_class(self):
        command = 'SEND'
        self.assertEquals(self.decoder.get_frame_class(command), Frames.SEND)

    def test_decoder_invalid_frame_class(self):
        command = '---'
        self.assertRaises(Exception, self.decoder.get_frame_class, command)

    def test_decoder_decode_connect(self):
        testFrame = Frames.CONNECT(**{"accept-version":"1.2", "host":"localhost"})
        msg = "CONNECT\naccept-version:1.2\nhost:localhost\n\n\x00"
        self.assertEquals(self.decoder.decode(msg).__dict__, testFrame.__dict__)

    def test_decoder_decode_connect_missing_req_header(self):
        msg = "CONNECT\nhost:localhost\n\n\x00"
        self.assertRaises(Exception, self.decoder.decode(msg))

    def test_decoder_decode_send(self):
        testFrame = Frames.SEND(**{"destination":"/queue/a", "msg":"hello queue a"})
        msg = "SEND\ndestination:/queue/a\n\nhello queue a\x00"
        self.assertEquals(self.decoder.decode(msg).__dict__, testFrame.__dict__)

    def test_decoder_decode_send_missing_req_header(self):
        msg = "SEND\n\nhello queue a\x00"
        self.assertRaises(Exception, self.decoder.decode(msg))

if __name__ == '__main__':
    unittest.main()