import Frames


class Encoder(object):
    """
    This class is for encoding STOMP frames.
    """
    def __init__(self):
        pass

    def encode(self,command,**kwargs):
        """
        Use variable keyword argument syntax if calling with keywords containing hyphen as keywords can't contain hyphen
        http://stackoverflow.com/a/24121330
        e.g:
        Instead of encode("RECEIPT",receipt-id=10) <- contains hyphen
        Use: encode("RECEIPT", **{"receipt-id":10})
        """
        frame_class=self.get_frame_class(command)
        frame = frame_class(**kwargs)
        if not frame.has_required():
            raise Exception(command + 'frame REQUIRES headers: '+",".join(frame.required_headers()))

        return frame

    def get_frame_class(self,command):
        frame_class = Frames.FRAMES.get(command)
        if frame_class is None:
            raise Exception('There is no frame type: ' + command)
        return frame_class

    def convert_frame_to_ascii(self, frame):
        """
        """
        ascii_command = Frames.FRAMES.keys()[Frames.FRAMES.values().index(type(frame))]
        ascii_headers = ''
        for k, v in frame.headers:
            ascii_headers += str(k) + ':' + str(v) + '\n'
        ascii_headers += '\n'
        ascii_msg = frame.msg
        ascii_frame = ascii_command + ascii_headers + ascii_msg + Frames.NULL
        return ascii_frame