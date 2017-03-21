import unittest
from Encoder import Encode
from Utils import Frames

class TestEncoder(unittest.TestCase):
    def setUp(self):
        self.encoder = Encode.Encoder();
        pass

    def test_encoder_get_frame_class(self):
        command = 'SEND'
        self.assertEquals(self.encoder.get_frame_class(command),Frames.SEND)

    def test_encoder_invalid_class(self):
        command = 'asd'
        self.assertRaises(Exception,self.encoder.get_frame_class,command)

    def test_encode_connect(self):
        kwargs = {'port':1212,'accept-version':'1.2,10.1','host':'localhost'}
        testFrame = Frames.CONNECT(**kwargs)
        testmsg = 'CONNECT'
        self.assertEquals(self.encoder.encode(testmsg,**kwargs).__dict__,testFrame.__dict__)

    def test_encode_send(self):
        kwargs = {'destination': 'asd'}
        testFrame = Frames.SEND(**kwargs)
        testmsg = 'SEND'
        self.assertEquals(self.encoder.encode(testmsg,**kwargs).__dict__,testFrame.__dict__)

    def test_encode_send_missing_header(self):
        kwargs = {'dst': 'asd'}
        testmsg = 'SEND'
        self.assertRaises(Exception,self.encoder.encode,testmsg,**kwargs)

    def test_encode_subscribe(self):
        kwargs = {'destination':'asd','id':'123'}
        testFrame = Frames.SUBSCRIBE(**kwargs)
        testmsg = 'SUBSCRIBE'
        self.assertEquals(self.encoder.encode(testmsg,**kwargs).__dict__,testFrame.__dict__)

    def test_encode_subscribe_missing_header(self):
        kwargs = {'':'','':''}
        testmsg = 'SUBSCRIBE'
        self.assertRaises(Exception,self.encoder.encode,testmsg, **kwargs)

    def test_encode_unsubscribe(self):
        kwargs = {'id': '123'}
        testFrame = Frames.SUBSCRIBE(**kwargs)
        testmsg = 'UNSUBSCRIBE'
        self.assertEquals(self.encoder.encode(testmsg, **kwargs).__dict__, testFrame.__dict__)

    def test_encode_unsubscribe_missing_header(self):
        kwargs = {'':'','':''}
        testmsg = 'UNSUBSCRIBE'
        self.assertRaises(Exception,self.encoder.encode,testmsg, **kwargs)

if __name__ == '__main__':
    unittest.main()