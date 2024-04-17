#import required modules
import cv2
from .XEnum import StreamType
from modules.const import ENV
from modules.capture_util import xmsg, xerr

#gstreamer pipeline constructor
def gstreamer_pipeline_csi(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    framerate=30,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=0 ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
        )
    )

#gstreamer pipeline constructor
def gstreamer_pipeline_usb(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    framerate=30,
):

    return (
        "v4l2src device=/dev/video%d ! "
        "image/jpeg, format=MJPG, width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvv4l2decoder mjpeg=1 ! "
        "nvvidconv ! "
        "videoconvert ! video/x-raw, format=BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate
        )
    )

    # return (
    #     "v4l2src device=/dev/video%d ! "
    #     "image/jpeg, format=YUYV, width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
    #     "nvv4l2decoder mjpeg=0 ! "
    #     "nvvidconv ! "
    #     "videoconvert ! video/x-raw, format=BGR ! appsink"
    #     % (
    #         sensor_id,
    #         capture_width,
    #         capture_height,
    #         framerate
    #     )
    # )


    # return (
    #     "v4l2src device=/dev/video%d ! "
    #     "image/jpeg, format=MJPG, width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
    #     "nvv4l2decoder mjpeg=1 ! "
    #     "nvvidconv ! "
    #     "video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink"
    #     % (
    #         sensor_id,
    #         capture_width,
    #         capture_height,
    #         framerate
    #     )
    # )

    # return (
    #     "v4l2src device=/dev/video%d ! "
    #     "video/x-raw, width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
    #     "videoconvert ! "
    #     "video/x-raw, format=(string)BGR ! "
    #     "appsink"
    #     % (
    #         sensor_id,
    #         capture_width,
    #         capture_height,
    #         framerate
    #     )
    # )

    # return " ! ".join(["v4l2src device=/dev/video0",
    #                    "video/x-raw, width=640, height=480, framerate=30/1",
    #                    "videoconvert",
    #                    "video/x-raw, format=(string)BGR",
    #                    "appsink"
    #                    ])

#main class for storing stream
class Stream():
    def __init__(self, stream_type = StreamType.csi, device_id=0):
        self.stream_type = stream_type
        self.device_id = device_id

    def get_capture(self, csi_config = {
        'capture_w': 1920,
        'capture_h': 1080,
        'frame_rate': 30
    }):
        #getting csi camera configurations
        capture_width = csi_config['capture_w']
        capture_height = csi_config['capture_h']
        framerate = csi_config['frame_rate']

        if self.stream_type is StreamType.csi:
            # create the pipeline
            gp = gstreamer_pipeline_csi(sensor_id=self.device_id, capture_width=capture_width, capture_height=capture_height, framerate=framerate)
            xmsg(f'gst pipeline: {gp}')
            cap = cv2.VideoCapture(gp, cv2.CAP_GSTREAMER)
            return cap
        elif self.stream_type is StreamType.usb:
            # return cv2.VideoCapture(self.device_id, cv2.CAP_V4L2)
            #cap = cv2.VideoCapture(0, cv2.CAP_V4L2 if ENV == 'jetson' else None)
            gp = gstreamer_pipeline_usb(sensor_id=1, capture_width=capture_width, capture_height=capture_height,framerate=framerate)
            xmsg(f'gst pipeline: {gp}')
            cap = cv2.VideoCapture(gp, cv2.CAP_GSTREAMER)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, capture_width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, capture_height)
            # cap.set(cv2.CAP_PROP_FPS, 2)
            return cap