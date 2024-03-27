#import required modules
from modules.stream import Stream, StreamType
import cv2, time, argparse, threading
from modules.XEnum import StreamType, YoloModelType, SignalType
from ultralytics import YOLO
from modules.signal import Signal
from modules.const import *
import RPi.GPIO as GPIO

#update signal
def update_signal(signal_type, active=False):
    try:
        GPIO.setmode(GPIO.BCM)
        if signal_type is SignalType.person:
            GPIO.setup(PERSON_PIN_NUM, GPIO.OUT)
            if active:
                GPIO.output(PERSON_PIN_NUM, GPIO.HIGH)
            else:
                GPIO.output(PERSON_PIN_NUM, GPIO.LOW)

        elif signal_type is SignalType.forklift:
            GPIO.setup(FORKLIST_PIN_NUM, GPIO.OUT)
            if active:
                GPIO.output(FORKLIST_PIN_NUM, GPIO.HIGH)
            else:
                GPIO.output(FORKLIST_PIN_NUM, GPIO.LOW)
    except:
        print('[err]: GPIO encounters some errors.')
    finally:
        GPIO.cleanup()

#thread declaration
person_signal = Signal(SignalType.person)
forklift_signal = Signal(SignalType.forklift)
person_signal.set_callback(update_signal)
forklift_signal.set_callback(update_signal)

#load yolo model
def load_model(model_name):
    print(f"[msg]: Start loading yolo model [ {model_name} ].")
    model = YOLO(f"./models/{model_name}.pt")
    print('[msg]: Completed Model loading.')
    return model

#get all detected object class
def get_detected_cls(results):
    classes = [int(i.cls.cpu().numpy()) for i in results[0].boxes]
    return classes

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
    print(f'[msg]: Completed opencv VideoCap. | Cap is opened: {cap.isOpened()}')

    if not cap.isOpened():
        print('[msg]: cap is not opened!')
        cap.release()
        cv2.destroyAllWindows()
        exit()

    print('[msg]: Start object detection.')

    prev_time = time.time()
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print('[err]: Failed to read the stream')
            break
        
        # Display the resulting frame
        if frame.size != 0:
            results = model(frame, verbose=False, classes=[0, 2])
            frame = results[0].plot() #person and car

            #update for fps calculation
            frame_count += 1
            current_time = time.time()
            elapsed_time = current_time - prev_time

            #re-calculate the fps for every new second
            if elapsed_time >= 1.0:
                #check detected class for alerting PLC LED light
                detected_cls = get_detected_cls(results)
                person_signal.active = True if 0 in detected_cls else False
                forklift_signal.active = True if 2 in detected_cls else False

                fps = frame_count / elapsed_time
                frame_count = 0
                prev_time = current_time

            #plot the metadata to the frame
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

    # # Create threads
    # yolo_thread = threading.Thread(target=read_video, args = (args.source, args.model))
    # signal_thread = threading.Thread(target=update_signal, args=(SignalType.person,))
    

    # # Start threads
    # yolo_thread.start()
    # signal_thread.start()

    # # Wait for threads to complete
    # yolo_thread.join()
    # signal_thread.join()