import cv2
import numpy as np
import dlib
import math
import constants as c

class FaceTracker:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.direction = 3
        self.noseOldx = 0
        self.noseOldy = 0
        self.reset = False
        self.click = False

        print("Camera warming up ...")

    def update_frame(self):
        _, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.detector(gray)

        if(len(faces) == 0):
            self.reset = True
            print("RESETTTTTT")
        else:
            self.reset = False

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
            nosex = landmarks.part(30).x
            nosey = landmarks.part(30).y
            # noseTopx = landmarks.part(29).x
            # noseTopy = landmarks.part(29).y

            mouthBottomx = landmarks.part(66).x
            mouthBottomy = landmarks.part(66).y

            mouthTopx = landmarks.part(62).x
            mouthTopy = landmarks.part(62).y

            faceMiddleLeftx = landmarks.part(2).x
            faceMiddleLefty = landmarks.part(2).y
            faceMiddleRightx = landmarks.part(14).x
            faceMiddleRighty = landmarks.part(14).y


            frame = cv2.circle(frame, (rightx, righty), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (leftx, lefty), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (rightx, righty), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (leftx, lefty), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (eye1Lx, eye1Ly), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (eye2Rx, eye2Ry), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (nosex, nosey), 6, (0, 0, 255), -1)
            frame = cv2.circle(frame, (faceMiddleLeftx, faceMiddleRighty), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (faceMiddleRightx, faceMiddleRighty), 4, (255, 0, 0), -1)
            # frame = cv2.circle(frame, (noseTopx, noseTopy), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (mouthBottomx, mouthBottomy), 4, (255, 0, 0), -1)
            frame = cv2.circle(frame, (mouthTopx, mouthTopy), 4, (255, 0, 0), -1)

            # for n in range(0, 68):
            #     x = landmarks.part(n).x
            #     y = landmarks.part(n).y
            #     cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)


            eyeLine1 = math.sqrt(pow((eye1Lx - leftx), 2) + pow((eye1Ly - lefty), 2))
            eyeLine2 = math.sqrt(pow((rightx - eye2Rx), 2) + pow((righty - eye2Ry), 2))

            # print(self.noseOldx - nosex)
            # print(self.noseOldy - nosey)
            # print(lefty - righty)
            self.noseChangey = ((faceMiddleLefty + faceMiddleRighty)/2) - nosey
            self.noseChangex = (abs(faceMiddleRightx - nosex) - abs(faceMiddleLeftx - nosex))


            # print(self.noseChangex)

            if(abs(mouthTopy-mouthBottomy) > 10):
                self.click = True
                print("CLICK")
            else:
                self.click = False

            self.noseOldx = nosex
            self.noseOldy = nosey

            if(abs(eyeLine1 - eyeLine2) < 30):
                if lefty - righty > 30:
                    print("UP")
                    self.direction = 1
                elif lefty - righty < -30:
                    print("DOWN")
                    self.direction = 2
                else:
                    print("No movement")
                    self.direction = 3
            else:
                print("Not looking at camera")
                self.direction = 4

            yMiddle = int((faceMiddleLefty + faceMiddleRighty)/2)
            xMiddle = int((faceMiddleRightx + faceMiddleLeftx)/2)

            cv2.rectangle(frame,(xMiddle - int(c.horizontal_x_sens/2) , yMiddle + c.vertical_y_sens),(xMiddle + int(c.horizontal_x_sens/2), yMiddle - c.vertical_y_sens),(0,255,0),3)
        frame = cv2.flip(frame, 1)
        return frame

    def get_direction(self):
        return self.direction

    def release_camera(self):
        self.cap.release()

    def get_nose_direction(self):
        return self.noseChangex, self.noseChangey

    def on_click(self):
        return self.click

    def on_reset(self):
        return self.reset



def main():
    test = FaceTracker()
    while True:
        frame = test.update_frame()
        frame2 = cv2.resize(frame, (0, 0), fx = 0.75, fy = 0.75)
        cv2.imshow("frame", frame2)
        # print(test.get_direction())
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    test.release_camera()
    return ()

if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
