import cv2
import dlib
from face_tracking.face_tracker import FaceTracker
import settings
import numpy as np


class DlibTracker(FaceTracker):
    def __init__(self):
        super().__init__()
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("data/shape_predictor_68_face_landmarks.dat")

    def update(self):
        ret, frame = self.cap.read()
        w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        K = np.array([[w, 0, w/2],
                    [0, w, h/2],
                    [0, 0, 1]], dtype=np.float32)

        # Rough fisheye distortion coefficients
        # Try tweaking these until the image looks less warped
        D = np.array([-0.3, 0.1, 0, 0], dtype=np.float32)
        if not ret:
            if settings.SHOW_DEBUG:
                self.render_debug(frame, [])
            return None
        
        new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(
            K, D, (w, h), np.eye(3), balance=0.0
        )
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(
            K, D, np.eye(3), new_K, (w, h), cv2.CV_16SC2
        )
        undistorted = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR)
        
        gray = cv2.cvtColor(undistorted, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        cv2.imshow("Undistorted", undistorted)

        for face in faces:
            print("test")
            landmarks = self.predictor(gray, face)
            for n in range(68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        cv2.imshow("Face Landmarks", frame)
        cv2.waitKey(1)