#import required modules
from modules.stream import Stream, StreamType
import cv2, time, argparse
from modules.XEnum import StreamType, YoloModelType
from ultralytics import YOLO

#load yolo model
def load_model(model_name):
    print(f"[msg]: Start loading yolo model [ {model_name} ].")
    model = YOLO(f"./models/{model_name}.pt")
    print('[msg]: Completed Model loading.')
    return model

def read_video(source = StreamType.csi, model_name = YoloModelType.yolov8n):
    #load yolo model
    model = load_model(model_name)

    #load video cap
    print('[msg]: Start loading opencv VideoCap.')
    stream = Stream(source)
    csi_config = {
        'capture_w': 1920,
        'capture_h': 1080,
        'display_w': 1920,
        'display_h': 1080,
        'frame_rate': 30,
        'flip_method': 0 
    }
    cap = stream.get_capture(csi_config=csi_config)
    print(f'[msg]: Completed opencv VideoCap. | Cap is opended: {cap.isOpened()}')

    if not cap.isOpened():
        print('[msg]: cap is not opened!')
        cap.release()
        cv2.destroyAllWindows()
        exit()

    print('[msg]: Start object detection.')
    prev_time = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print('[err]: Failed to read the stream')
            break
        
        # Display the resulting frame
        if frame.size != 0:
            frame = model(frame, verbose=False, classes=[0, 2])[0].plot() #person and car
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time
            cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Frame', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#starting point of the application
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read video from CSI camera, USB camera, or file.")
    parser.add_argument('--source', type=StreamType, default=StreamType.csi, choices=list(StreamType),
                        help="Specify the video source: 'csi' for CSI camera, 'usb' for USB camera, 'file' for video file")
    parser.add_argument('--model', type=YoloModelType, default=YoloModelType.yolov8n, choices=list(YoloModelType),
                        help="Specify the Yolov8 models type.")
    args = parser.parse_args()
    read_video(args.source, args.model)