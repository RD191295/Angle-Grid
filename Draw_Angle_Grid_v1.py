import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret,frame = cap.read()
    frame_copy = frame.copy()
    if ret :
        # DRAW ANGLE GRID
        rows,cols,ch = frame.shape
        point_1 = (cols//2,rows-50)
        length =270

        # CREATE BASELINE
        cv2.line(frame_copy,(50,rows-50),(cols-50,rows-50),(0,0,255),2)

        # CREATE CENTRAL POINT
        cv2.circle(frame_copy, point_1, 5, (0, 0, 255), -1)

          # GRID CIRCLE
        cv2.ellipse(frame_copy, point_1, (100,100), 0, 180, 360, (255,0,0), 2)
        cv2.ellipse(frame_copy, point_1, (200,200), 0, 180, 360, (255,0,0), 2)
        cv2.ellipse(frame_copy, point_1, (270,270), 0, 180, 360, (255,0,0), 2)


        # DRAW ANGLE LINE FROM CENTRAL POINT TO SPECIFIC DEGREE
        for i in range(0,180,30):
            theta = i * 3.14 / 180.0
            x2 = int(point_1[0] -length * np.cos(theta))
            y2 = int(point_1[1] - length * np.sin(theta))
            cv2.line(frame_copy,(x2,y2),point_1,(0,0,255),2)
            cv2.putText(frame_copy, str(180-i), (x2 - 10, y2 - 15), cv2.FONT_HERSHEY_SIMPLEX,0.7, (255, 10, 35), 2)


        # PUT TEXT AT ANGLE 0
        cv2.putText(frame_copy,"0", (cols-40, rows - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 75, 155), 1)

        result = cv2.addWeighted(frame_copy, 0.25, frame, 1 - 0.25, 0)

        cv2.imshow('result',result)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
