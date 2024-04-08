#import required modules
import cv2
from .XEnum import StreamType

#gstreamer pipeline constructor
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

#main class for storing stream
class Stream():
    def __init__(self, stream_type = StreamType.csi):
        self.stream_type = stream_type

    def get_capture(self, csi_config = {
        'capture_w': 1920,
        'capture_h': 1080,
        'display_w': 1920,
        'display_h': 1080,
        'frame_rate': 30,
        'flip_method': 0 
    }):
        if self.stream_type is StreamType.csi:
            #getting csi camera configurations
            capture_width = csi_config['capture_w']
            capture_height = csi_config['capture_h']
            display_width = csi_config['display_w']
            display_height = csi_config['display_h'] 
            framerate = csi_config['frame_rate']
            flip_method = csi_config['flip_method']

            # create the pipeline
            gp = gstreamer_pipeline(sensor_id=0, capture_width=capture_width, capture_height=capture_height, display_width=display_width, display_height=display_height,framerate=framerate,flip_method=flip_method)
            cap = cv2.VideoCapture(gp, cv2.CAP_GSTREAMER)
            return cap
        elif self.stream_type is StreamType.usb:
            cap = cv2.VideoCapture(0, cv2.CAP_V4L2 if ENV is 'jetson' else None)
            return cap