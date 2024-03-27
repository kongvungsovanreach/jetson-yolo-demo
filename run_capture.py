#import required modules
from modules.stream import Stream, StreamType
import cv2, time, argparse
from modules.XEnum import StreamType
from modules.capture_util import random_save


#capture some frames from stream
def img_capture(source = StreamType.csi, threshold = 10, folder_count = 10):
    #load video cap
    print('[msg]: Start loading opencv VideoCap.')
    stream = Stream(source)
    csi_config = {
        'capture_w': 1920,
        'capture_h': 1080,
        'display_w': 1920,
        'display_h': 1080,
        'frame_rate': 5,
        'flip_method': 0 
    }
    cap = stream.get_capture(csi_config=csi_config)
    print(f'[msg]: Completed opencv VideoCap. | Cap is opended: {cap.isOpened()}')

    if not cap.isOpened():
        print('[msg]: cap is not opened!')
        cap.release()
        cv2.destroyAllWindows()
        exit()
    
    print('[msg]: Start capturing frames and save them.')
    
    criteria_store = {'prev_f_gray': None, 'saved_count': 0}
    while True:
        ret, frame = cap.read()
        oframe = frame.copy()
        if not ret:
            print('[err]: Failed to read the stream')
            break
        
        #display the resulting frame
        if frame.size != 0:
            #convert it to grayscale to ensure the efficiency
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            #initalize the criteria state to avoid error on first frame
            if criteria_store['prev_f_gray'] is None:
                criteria_store['prev_f_gray'] = gray_blurred
                continue

            #compute absolute difference between the current frame and previous frame
            frame_diff = cv2.absdiff(criteria_store['prev_f_gray'], gray_blurred)

            #apply the fixed threshold value
            _, thresholded = cv2.threshold(frame_diff, 20, 255, cv2.THRESH_BINARY)
            
            #calculate the mean of the pixel differences
            mean_diff = frame_diff.mean()

            #plot the info on the frame
            cv2.putText(frame, f'FPS: {csi_config["frame_rate"]}  |  Threshold: {threshold}  |  Mean diff: {mean_diff:.2f}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f'Frame saved count: {criteria_store["saved_count"]}', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            #check if mean difference exceeds the threshold
            if mean_diff > threshold:
                random_save(oframe, folder_count)
                criteria_store['saved_count'] += 1
                cv2.putText(frame, f'Criteria matched | Frame was saved.', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                pass
            
            #show realtime plot of stream
            show_win_size = (960, 540)
            cv2.imshow('Stream', cv2.resize(frame, show_win_size))
            cv2.imshow('Motion', cv2.resize(thresholded, show_win_size))

            #update frame states
            criteria_store['prev_f_color'] = oframe
            criteria_store['prev_f_gray'] = gray_blurred

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
    parser.add_argument('--threshold', type=int, default=10,
                        help="Specify the threhold for frame saving. Ex: 20, 30, 40,...")
    
    parser.add_argument('--folder_count', type=int, default=10,
                        help="Specify the number of folder images will be randomly saved in.")
    args = parser.parse_args()
    img_capture(args.source, args.threshold, args.folder_count)
