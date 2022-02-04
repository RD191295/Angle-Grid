import cv2
import numpy as np

class Angle_Grid :
    def __init__(self,frame):
        self.camera_port = 0
        self.frame = frame
        self.base_line_color = (0,0,255)
        self.central_point_color = (0,255,0)
        self.grid_circle_color = (255,0,0)
        self.start_angle = 0
        self.end_angle = 180
        self.interval_angle = 30

    def get_frame(self,frame):
        self.frame_copy = self.frame.copy()

        # FRAME SIZE
        self.rows,self.cols,self.channels = self.frame.shape
        self.point_1 = (self.cols//2,self.rows-50)
        self.length = 270 # length of the line

        # CREATE BASELINE
        cv2.line(self.frame_copy,(50,self.rows-50),(self.cols-50,self.rows-50),self.base_line_color,2)

        # CREATE CENTRAL POINT
        cv2.circle(self.frame_copy,self.point_1,5,self.central_point_color,-1)

        # GRID CIRCLES
        cv2.ellipse(self.frame_copy, self.point_1, (100, 100), 0, 180, 360, self.grid_circle_color, 2)
        cv2.ellipse(self.frame_copy, self.point_1, (200, 200), 0, 180, 360, self.grid_circle_color, 2)
        cv2.ellipse(self.frame_copy, self.point_1, (270, 270), 0, 180, 360, self.grid_circle_color, 2)

        # CREATE ANGLE GRID LINES
        for i in range(self.start_angle, self.end_angle, self.interval_angle):
            self.theta = i * np.pi / 180
            x2 = int(self.point_1[0] - self.length * np.cos(self.theta))
            y2 = int(self.point_1[1] - self.length * np.sin(self.theta))
            cv2.line(self.frame_copy, (x2, y2), self.point_1, self.base_line_color, 2)
            cv2.putText(self.frame_copy, str(180 - i), (x2 - 10, y2 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 10, 35),2)

            # PUT TEXT AT ANGLE 0
            cv2.putText(self.frame_copy, "0", (self.cols - 40, self.rows - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 75, 155), 1)

            self.result = cv2.addWeighted(self.frame_copy, 0.25, frame, 0.75, 0)

        return self.frame_copy,self.result


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        _,frame = cap.read()
        angle_grid = Angle_Grid(frame)
        frame_copy,result = angle_grid.get_frame(frame)
        cv2.imshow('frame',frame)
        cv2.imshow('result',result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()