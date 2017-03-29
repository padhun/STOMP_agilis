from Stomp.Utils import Frames


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
            raise RuntimeError(command + 'frame REQUIRES headers: ' + ",".join([header for header in frame.required_headers]))

        return frame

    def get_frame_class(self,command):
        frame_class = Frames.FRAMES.get(command)
        if frame_class is None:
            raise RuntimeError('There is no frame type: ' + command)
        return frame_class
