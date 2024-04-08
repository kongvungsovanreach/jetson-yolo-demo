#import required modules
from modules.stream import Stream, StreamType
import cv2, time, argparse
import numpy as np
from modules.XEnum import StreamType, CaptureMethod
from modules.capture_util import random_save, get_scaled_font, Config, xmsg, xerr
from modules.ui_helper import start_area_configuration

#global vars
config = Config()
config.cam_window_size = (2560, 1440)
config.show_window_size = (640, 480)
config.criteria_store = {'prev_f_gray': None, 'saved_count': 0}
config.font_size, config.font_thickness = None, None

#load cap for capturing
def load_local_cap(source, threshold, folder_count):
    xmsg('start loading opencv VideoCap.')
    stream = Stream(source)
    config.csi_config = {
        'capture_w': 1920,
        'capture_h': 1080,
        'display_w': 1920,
        'display_h': 1080,
        'frame_rate': 5,
        'flip_method': 0 
    }
    cap = stream.get_capture(csi_config=config.csi_config)

    # Set desired resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.cam_window_size[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.cam_window_size[1])
    cap.set(cv2.CAP_PROP_FPS, 2)

    xmsg(f'completed opencv VideoCap. | Cap is opended: {cap.isOpened()}.')

    if not cap.isOpened():
        xmsg(' cap is not opened!')
        cap.release()
        cv2.destroyAllWindows()
        exit()
    return cap

#capture some frames from stream
def img_capture(source = StreamType.csi, threshold = 10, folder_count = 10):
    cap = load_local_cap(source, threshold, folder_count)
    polygons, frame = start_area_configuration(cap, config.show_window_size)
    xmsg('start capturing frames and save them.')

    count = 0
    while True:
        count += 1
        ret, frame = cap.read()
        if (count % 30) != 0:
            continue        

        oframe = frame.copy()
        frame = cv2.resize(frame, config.show_window_size)

        #loop through each polygon
        for polygon_coords in polygons:
            pts = np.array(polygon_coords, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.fillPoly(frame, [pts], (0, 0, 0))  #fill polygon with black color

        if not ret:
            xerr('failed to read the stream.')
            break
        
        #display the resulting frame
        if frame.size != 0:
            if not config.font_size:
                config.font_size, config.font_thickness = get_scaled_font(frame.shape[1], frame.shape[0], size_ratio=0.9e-3, thickness_scale=2e-3)
                xmsg(f'scaled font size & thickness: {config.font_size} | {config.font_thickness}.')

            #convert it to grayscale to ensure the efficiency
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            #initalize the criteria state to avoid error on first frame
            if config.criteria_store['prev_f_gray'] is None:
                config.criteria_store['prev_f_gray'] = gray_blurred
                continue

            #compute absolute difference between the current frame and previous frame
            frame_diff = cv2.absdiff(config.criteria_store['prev_f_gray'], gray_blurred)

            #apply the fixed threshold value
            _, thresholded = cv2.threshold(frame_diff, 20, 255, cv2.THRESH_BINARY)
            thresholded = cv2.resize(thresholded, config.show_window_size)
            
            #calculate the mean of the pixel differences
            mean_diff = frame_diff.mean()

            #draw rectangle as background color
            # cv2.rectangle(img = frame, 
            #               pt1 = (0, 0), 
            #               pt2 = (300, 70), 
            #               color = (255, 255, 255), 
            #               thickness = -1)

            #plot the info on the frame
            cv2.putText(img = frame, 
                        text = f'FPS: {config.csi_config["frame_rate"]} | Threshold: {threshold} | Mean diff: {mean_diff:.2f}', 
                        org = (10, 20), 
                        fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
                        fontScale = config.font_size, 
                        color = (0, 0, 255), 
                        thickness = config.font_thickness)
            cv2.putText(img = frame, 
                        text = f'Frame saved count: {config.criteria_store["saved_count"]}', 
                        org = (10, 40), 
                        fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
                        fontScale = config.font_size, 
                        color = (0, 0, 255), 
                        thickness = config.font_thickness)

            #check if mean difference exceeds the threshold
            if mean_diff > threshold:
                random_save(oframe, folder_count)
                config.criteria_store['saved_count'] += 1
                cv2.putText(img = frame, 
                        text = f'Criteria matched | Frame was saved.', 
                        org = (10,60), 
                        fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
                        fontScale = config.font_size, 
                        color = (0, 0, 255), 
                        thickness = config.font_thickness)

            #horizontally concatenate the frames
            concatenated_frame = cv2.hconcat([frame, cv2.cvtColor(thresholded, cv2.COLOR_GRAY2RGB)])

            #show realtime plot of stream
            cv2.imshow('Stream & Motion', concatenated_frame)
            # cv2.imshow('Original', oframe)

            #update frame states
            config.criteria_store['prev_f_color'] = oframe
            config.criteria_store['prev_f_gray'] = gray_blurred

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
    parser.add_argument('--method', type=CaptureMethod, default=CaptureMethod.motion, choices=list(CaptureMethod),
                        help="Specify the method for triggering the capture/save function. Choice: {motion, yolo}")
    parser.add_argument('--threshold', type=int, default=20,
                        help="Specify the threhold for frame saving. Ex: 20, 30, 40,...")
    parser.add_argument('--folder_count', type=int, default=10,
                        help="Specify the number of folder images will be randomly saved in.")
    args = parser.parse_args()

    if args.method is CaptureMethod.motion:
        img_capture(args.source, args.threshold, args.folder_count)
    elif args.method is CaptureMethod.yolo:
       print('yolo method triggered')