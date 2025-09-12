import cv2
import dlib
from face_tracking.face_tracker import FaceTracker
import settings


class DlibTracker(FaceTracker):
    def __init__(self):
        super().__init__()
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("data/shape_predictor_68_face_landmarks.dat")

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            if settings.SHOW_DEBUG:
                self.render_debug(frame, [])
            return None
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        for face in faces:
            landmarks = self.predictor(gray, face)
            for n in range(68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        cv2.imshow("Face Landmarks", frame)
        cv2.waitKey(1)