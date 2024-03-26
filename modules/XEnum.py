#import required modules
from enum import Enum

#enum for type of stream
class StreamType(Enum):
    usb = 'usb'
    csi = 'csi'
    file = 'file'

    def __str__(self):
        return self.value
    
class YoloModelType(Enum):
    yolov8n = 'yolov8n'
    yolov8s = 'yolov8s'
    yolov8m = 'yolov8m'
    yolov8l = 'yolov8l'
    yolov8x = 'yolov8x'

    def __str__(self):
        return self.value