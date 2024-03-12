import cv2, time
import argparse
from ultralytics import YOLO
import matplotlib.pyplot as plt

def read_video(source, model_name):
    #load yolo model
    print(f"[+] Loading yolo model [ {model_name} ].")
    model = YOLO(f"./models/{model_name}.pt")
    print('[+] Model loading completed!')

    print('[+] Loading opencv VideoCap.')
    cap = cv2.VideoCapture('/home/dbnis/Downloads/yolo_test/video.mp4')
    # cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if source == 'camera':
        cap = cv2.VideoCapture(0)
    elif source == 'file':
        video_file = input("Enter the video file name ./videos/: ")
        cap = cv2.VideoCapture(f'./videos/{video_file}')
    else:
        raise ValueError("Invalid source type. Please use --camera, --file.")
    
    print('[+] Start detection.')
    prev_time = 0
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        if frame.size != 0:
            frame = model(frame, verbose=False, classes=[0, 2])[0].plot() #person and car
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time
            cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read video from camera, file.")
    parser.add_argument('--source', type=str, required=True, choices=['camera', 'file'],
                        help="Specify the video source: 'camera' for camera, 'file' for video file")
    parser.add_argument('--model', type=str, default= 'yolov8n', choices=['yolov8n', 'yolov8s', 'yolov8m', 'yolov8x'],
                        help="Specify the Yolov8 models type.")
    args = parser.parse_args()
    read_video(args.source, args.model)