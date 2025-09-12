import mediapipe as mp
import cv2

from face_tracking_parameters import FaceTrackingParameters
import mp_landmarks
import face_tracking.landmarks as landmark_enum
import settings
import shape_thresholds
from utils import average

class FaceTracker():
    def __init__(self):
        cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.FT_CAPTURE_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.FT_CAPTURE_HEIGHT)
        
        self.cap = cap
        self.average_values = {}
        self.rolling_average_amount = 0
        self.parameters = FaceTrackingParameters()

    def update_averages(self, landmarks):
        for id in landmarks:
            lm = landmarks[id]

            values = self.average_values.get(id, [])
            values.append((lm.x, lm.y))
            if len(values) > settings.ROLLING_AVERAGE_MAX:
                values.pop(0)
            self.average_values[id] = values

    def update_scale(self, landmarks):
        left_edge = landmarks[landmark_enum.HEAD_LEFT_EDGE]
        right_edge = landmarks[landmark_enum.HEAD_RIGHT_EDGE]
        self.scale =  1 / abs(left_edge.x - right_edge.x)

    def get_mouth_openness(self):
        top = average(list(map(lambda x: x[1], self.average_values[landmark_enum.TOP_LIP_BOTTOM_CENTER])))
        bottom = average(list(map(lambda x: x[1], self.average_values[landmark_enum.BOTTOM_LIP_TOP_CENTER])))
        raw_openness = abs(bottom - top) * self.scale

        return shape_thresholds.MOUTH_OPENNESS.lerp(raw_openness)
    
    def get_right_eye_openness(self):
        top = average(list(map(lambda x: x[1], self.average_values[landmark_enum.RIGHT_EYE_TOP])))
        bottom = average(list(map(lambda x: x[1], self.average_values[landmark_enum.RIGHT_EYE_BOTTOM])))
        inner = average(list(map(lambda x: x[1], self.average_values[landmark_enum.RIGHT_EYE_INNER])))
        outer = average(list(map(lambda x: x[1], self.average_values[landmark_enum.RIGHT_EYE_OUTER])))

        height = abs(bottom - top)
        width = abs(inner - outer)

        aspect_ratio = 1 - width / height
        print(aspect_ratio)
        return shape_thresholds.EYE_OPENNESS.lerp(aspect_ratio)

    def render_debug(self, frame, landmarks):
        try:
            if landmarks:
                for id in landmarks.keys():
                    lm = landmarks[id]
                    x = int(lm.x * settings.FT_CAPTURE_WIDTH)
                    y = int(lm.y * settings.FT_CAPTURE_HEIGHT)
                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                    cv2.putText(frame, str(id), (x + 2, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1)
            cv2.imshow("Face Tracking Debug", frame)
            cv2.waitKey(1)
        except Exception as e:
            print("Failed to render debug")
            print(e)
    
    def update(self):
        pass