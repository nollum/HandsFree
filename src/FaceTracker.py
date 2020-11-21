import cv2
import numpy as np
import dlib
import math

class FaceTracker:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.direction = 3
        print("Camera warming up ...")

    def update_frame(self):
        _, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.detector(gray)
        for face in faces:
            # x1 = face.left()
            # y1 = face.top()
            # x2 = face.right()
            # y2 = face.bottom()
            # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            landmarks = self.predictor(gray, face)

            rightx = landmarks.part(16).x
            righty = landmarks.part(16).y
            leftx = landmarks.part(0).x
            lefty = landmarks.part(0).y
            eye1Lx = landmarks.part(36).x
            eye1Ly = landmarks.part(36).y
            eye2Rx = landmarks.part(45).x
            eye2Ry = landmarks.part(45).y

            frame = cv2.circle(frame, (rightx, righty), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (leftx, lefty), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (rightx, righty), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (leftx, lefty), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (eye1Lx, eye1Ly), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (eye2Rx, eye2Ry), 4, (255, 0, 0), -1)

                        
            eyeLine1 = math.sqrt(pow((eye1Lx - leftx), 2) + pow((eye1Ly - lefty), 2))
            eyeLine2 = math.sqrt(pow((rightx - eye2Rx), 2) + pow((righty - eye2Ry), 2))
 
            if(abs(eyeLine1 - eyeLine2) < 30):
                if lefty - righty > 60:
                    print("UP")
                    self.direction = 1
                elif lefty - righty < -60:
                    print("DOWN")
                    self.direction = 2
                else:
                    print("No movement")
                    self.direction = 3
            else:
                print("Not looking at camera")
                self.direction = 4
        return frame

    def get_direction(self):
        return self.direction

    def release_camera(self):
        self.cap.release()

def main():
   
    while True:
        test = FaceTracker()
        frame = test.update_frame()
        frame2 = cv2.resize(frame, (0, 0), fx = 0.75, fy = 0.75)
        cv2.imshow("frame", frame2)
        print(test.get_direction())
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    test.release_camera()
    return ()

if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()