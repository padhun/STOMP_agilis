import unittest
from Decode import Decoder
import Frames

class TestDecoder(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()