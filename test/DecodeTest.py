import unittest
from Decoder import Decode
from Utils import Frames

class TestDecoder(unittest.TestCase):
    def setUp(self):
        self.decoder = Decode.Decoder()

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
        self.assertRaises(Exception, self.decoder.decode, msg)

    def test_decoder_decode_send(self):
        testFrame = Frames.SEND(**{"destination":"/queue/a", "msg":"hello queue a"})
        msg = "SEND\ndestination:/queue/a\n\nhello queue a\x00"
        self.assertEquals(self.decoder.decode(msg).__dict__, testFrame.__dict__)

    def test_decoder_decode_send_missing_req_header(self):
        msg = "SEND\n\nhello queue a\x00"
        self.assertRaises(Exception, self.decoder.decode, msg)

    def test_decoder_decode_subscribe(self):
        testFrame = Frames.SUBSCRIBE(**{"id":"0", "destination": "/queue/foo"})
        msg = "SUBSCRIBE\nid:0\ndestination:/queue/foo\n\n\x00"
        self.assertEquals(self.decoder.decode(msg).__dict__, testFrame.__dict__)

    def test_decoder_decode_subscribe_missing_req_header(self):
        msg = "SUBSCRIBE\ndestination:/queue/foo\n\n\x00"
        self.assertRaises(Exception, self.decoder.decode, msg)

    def test_decoder_decode_unsubscribe(self):
        testFrame = Frames.UNSUBSCRIBE(**{"id":"0"})
        msg = "UNSUBSCRIBE\nid:0\n\n\x00"
        self.assertEquals(self.decoder.decode(msg).__dict__, testFrame.__dict__)

    def test_decoder_decode_unsubscribe_missing_req_header(self):
        msg = "UNSUBSCRIBE\n\n\x00"
        self.assertRaises(Exception, self.decoder.decode, msg)

if __name__ == '__main__':
    unittest.main()