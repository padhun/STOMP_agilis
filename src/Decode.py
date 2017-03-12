
import Frames

class Decoder(object):

    def __init__(self):
        pass

    def get_frame_class(self,command):
        frame_class = Frames.FRAMES.get(command)
        if frame_class is None:
            raise Exception('There is no frame type: ' + command)
        return frame_class

    def decode(self,message):
        command, headers, msg = message.split('\n')[0], \
                                message.split('\n\n')[0].split('\n')[1:], \
                                message.split('\n\n')[1]
        frame_class = self.get_frame_class(command)
        frame_args = dict(item.split(":") for item in headers)
        frame = frame_class(msg=msg,**frame_args)
        return frame