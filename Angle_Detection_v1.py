import time
import sys
import cv2
import math
import numpy as np
from random import randint
import Draw_Angle_Grid_Module as draw
from scipy.spatial import distance as dist


capture = cv2.VideoCapture(0)

recording_flag = True
# Select boxes
bboxes = []
colors = []
mid_points = []
trackerType = "CSRT"
TrackerType = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def safe_div(x,y):
    if y == 0:
        return 0
    return x / y

def createTrackerByName(trackerType):
    # Create a tracker based on tracker name
    if trackerType == TrackerType[0]:
        tracker = cv2.legacy.TrackerBoosting_create()
    elif trackerType == TrackerType[1]:
        tracker = cv2.legacy.TrackerMIL_create()
    elif trackerType == TrackerType[2]:
        tracker = cv2.legacy.TrackerKCF_create()
    elif trackerType == TrackerType[3]:
        tracker = cv2.legacy.TrackerTLD_create()
    elif trackerType == TrackerType[4]:
        tracker = cv2.legacy.TrackerMedianFlow_create()
    elif trackerType == TrackerType[5]:
        tracker = cv2.legacy.TrackerGOTURN_create()
    elif trackerType == TrackerType[6]:
        tracker = cv2.legacy.TrackerMOSSE_create()
    elif trackerType == TrackerType[7]:
        tracker = cv2.legacy.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in TrackerType:
            print(t)

    return tracker



multiTracker = cv2.legacy.MultiTracker_create()

def main():
    global recording_flag,mid_points,bboxes,colors,multiTracker
    while True:

        ret, frame = capture.read()
        key = cv2.waitKey(1)
        cv2.putText(frame,"Press S to start/stop recording", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame,"Press space key two time for select", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame,"Press q to exit from selection", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        if key & 0XFF == 27:
            break
        elif key & 0XFF == 115:
            if recording_flag :
                angle_grid = draw.Angle_Grid(frame)
                frame_copy, frame = angle_grid.get_frame(frame)
                colors = []
                mid_points = []
                bboxes = []
                multiTracker = cv2.legacy.MultiTracker_create()
                while True :

                    bbox = cv2.selectROI('FRAME', frame)
                    bboxes.append(bbox)
                    colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
                    print("Press q to quit selecting boxes and start tracking")
                    print("Press any other key to select next object")
                    k = cv2.waitKey(0) & 0xFF
                    print(k)
                    if k == 113 :  # q is pressed
                        break

                createTrackerByName(trackerType)


                # Initialize MultiTracker
                for bbox in bboxes :
                    multiTracker.add(createTrackerByName(trackerType), frame, bbox)

                recording_flag = False
            else:
                recording_flag = True

        if recording_flag:
            angle_grid = draw.Angle_Grid(frame)
            frame_copy, frame = angle_grid.get_frame(frame)
            success, boxes = multiTracker.update(frame)

            if success :
                for i, newbox in enumerate(boxes) :
                    p1 = (int(newbox[0]), int(newbox[1]))
                    p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))

                    cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
                    mid_point = (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))
                    cv2.circle(frame, mid_point, 5, (0, 0, 255), -1)
                    cv2.putText(frame, "P" + str(i), (mid_point[0] + 5, mid_point[1] + 5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.75,
                                (0, 0, 255), 2)
                    mid_points.append(mid_point)

                    if len(mid_points) == 3 :
                        cv2.line(frame, mid_points[0], mid_points[1], (0, 0, 255), 2)
                        cv2.line(frame, mid_points[1], mid_points[2], (0, 255, 0), 2)
                        x = mid_points[-2][0] - mid_points[-3][0]
                        y = mid_points[-2][0] - mid_points[-1][0]
                        z = mid_points[-2][1] - mid_points[-3][1]
                        w = mid_points[-2][1] - mid_points[-1][1]

                        p = x * y + z * w

                        q = math.sqrt(pow(x, 2) + pow(z, 2))
                        r = math.sqrt(pow(y, 2) + pow(w, 2))

                        s = q * r

                        angle = p / s

                        theta = math.acos(angle)

                        theta = theta * 180 / math.pi  # conversion from rad to degree

                        theta = round(theta, 2)

                        cv2.ellipse(frame, mid_points[1], (50, 50), 0, 0, -(0 + theta), (0, 120, 255), 2)

                        cv2.putText(frame, str(theta), (mid_points[-2][0] + 50, mid_points[-2][1] - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    theta / 100 + 0.1,
                                    (255, 255, 255), 1, cv2.LINE_AA)
                        mid_points = []
            else :
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0, 0, 255),2)

            cv2.imshow('FRAME', frame)


    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
