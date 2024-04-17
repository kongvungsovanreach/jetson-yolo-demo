#import required modules
import tkinter as tk
from tkinter import simpledialog
import cv2
import numpy as np
from .capture_util import xmsg, xerr

#get user input from the GUI
def get_input(title, prompt):
    ROOT = tk.Tk()
    ROOT.withdraw()
    user_input = simpledialog.askstring(title=title,prompt=prompt)
    return user_input

def start_area_configuration(cap, show_window_size):
    #global variables
    drawing = False  #true if mouse is pressed
    mode = True  #true for polygon drawing
    points = []  #list of points for the current polygon
    polygons_list = []  #list to store all polygons' coordinates
    initial_frame = None  #store the initial frame for drawing
    frame = None  #initialize frame

    def draw_polygon(event, x, y, flags, param):
        nonlocal drawing, mode, points, frame, initial_frame

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            points = [(x, y)]
            initial_frame = frame.copy()  #store the initial frame for drawing

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                frame = initial_frame.copy()  #use the initial frame for drawing
                points.append((x, y))
                for i in range(len(points) - 1):
                    cv2.line(frame, points[i], points[i + 1], (0, 0, 255), 2)
                cv2.imshow('Draw Polygons', frame)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            points.append((x, y))
            cv2.fillPoly(initial_frame, [np.array(points)], (255, 255, 255))  #fill the polygon on initial frame
            cv2.polylines(initial_frame, [np.array(points)], isClosed=True, color=(0, 0, 255), thickness=2)  #draw red border on initial frame
            polygons_list.append(points)  #store the polygon coordinates
            points = []

    ret, frame = cap.read()
    frame = cv2.resize(frame, show_window_size)
    ih, iw = frame.shape[:2]  #get frame height and width
    cv2.namedWindow('Draw Polygons')
    cv2.setMouseCallback('Draw Polygons', draw_polygon)

    while True:
        cv2.imshow('Draw Polygons', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('m'):  #toggle between drawing mode
            mode = not mode

        elif key == ord('q'):  #ESC key to exit
            break

    cv2.destroyAllWindows()
    xmsg(f'polygons counts: {len(polygons_list)}')
    return polygons_list, frame