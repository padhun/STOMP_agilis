import unittest
from Encode import Encoder
import Frames
import socket




class TestUM(unittest.TestCase):

    def setUp(self):
        self.encoder = Encoder()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def test_encoder_get_frame_class(self):
        command = 'SEND'
        self.assertEquals(self.encoder.get_frame_class(command),Frames.SEND)

if __name__ == '__main__':
    unittest.main()