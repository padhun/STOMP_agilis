import Utils

class Decoder(object):

    def __init__(self):
        pass

    def get_frame_class(self,command):
        frame_class = Utils.Frames.FRAMES.get(command)
        if frame_class is None:
            raise Exception('There is no frame type: ' + command)
        return frame_class

    def decode(self,message):
        """
        :param message:
        :return:
        """
        command, headers, msg = message.split('\n')[0], \
                                message.split('\n\n')[0].split('\n')[1:], \
                                None if message.split('\n\n')[1] == '\x00' else message.split('\n\n')[1][:-1]
        frame_class = self.get_frame_class(command)
        frame_args = dict([[Utils.util.replace_all(Utils.Frames.UNESCAPE, part) for part in item.split(":")] for item in headers])
        frame = frame_class(msg=msg,**frame_args)
        if not frame.has_required():
            raise Exception(command + 'frame REQUIRES headers: ' + ",".join([header for header in frame.required_headers()]))
        return frame