import cv2

from face_tracking_parameters import FaceTrackingParameters
import face_tracking.landmarks as landmark_enum
import settings
import shape_thresholds
from utils import average

class FaceTracker():
    def __init__(self):
        cap = cv2.VideoCapture(0)
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
    
    def update_parameters(self):
        self.parameters.mouth_openness = self.get_mouth_openness()
        self.parameters.mouth_pog = self.get_mouth_pog()
        self.parameters.smile_right = self.get_mouth_smile_right()
        self.parameters.smile_left = self.get_mouth_smile_left()
        self.parameters.frown_right = self.get_mouth_frown_right()
        self.parameters.frown_left = self.get_mouth_frown_left()
        self.parameters.right_eye_openness = self.get_right_eye_openness()
        self.parameters.left_eye_openness = self.get_left_eye_openness()

    def get_average_for_landmark(self, id):
        values = self.average_values.get(id, [])
        return average(list(map(lambda x: x[1], values)))

    def get_mouth_openness(self):
        top = average(list(map(lambda x: x[1], self.average_values[landmark_enum.TOP_LIP_BOTTOM_CENTER])))
        bottom = average(list(map(lambda x: x[1], self.average_values[landmark_enum.BOTTOM_LIP_TOP_CENTER])))
        raw_openness = abs(bottom - top) * self.scale

        return shape_thresholds.MOUTH_OPENNESS.lerp(raw_openness)
    
    def get_mouth_pog(self):
        top = average(list(map(lambda x: x[1], self.average_values[landmark_enum.TOP_LIP_BOTTOM_CENTER])))
        bottom = average(list(map(lambda x: x[1], self.average_values[landmark_enum.BOTTOM_LIP_TOP_CENTER])))
        left = average(list(map(lambda x: x[0], self.average_values[landmark_enum.MOUTH_LEFT_EDGE])))
        right = average(list(map(lambda x: x[0], self.average_values[landmark_enum.MOUTH_RIGHT_EDGE])))

        width = abs(right - left)
        height = bottom - top

        raw_pog = height / width
        return shape_thresholds.MOUTH_POG.lerp(raw_pog)

    def get_mouth_smile_right(self):
        edge = average(list(map(lambda x: x[1], self.average_values[landmark_enum.MOUTH_RIGHT_EDGE])))
        top_center = average(list(map(lambda x: x[1], self.average_values[landmark_enum.TOP_LIP_TOP_CENTER])))
        bottom_center = average(list(map(lambda x: x[1], self.average_values[landmark_enum.BOTTOM_LIP_BOTTOM_CENTER])))
        center = (top_center + bottom_center) / 2
        raw_smile = (center - edge) * self.scale

        return shape_thresholds.MOUTH_SMILE.lerp(raw_smile)
    
    def get_mouth_smile_left(self):
        edge = average(list(map(lambda x: x[1], self.average_values[landmark_enum.MOUTH_LEFT_EDGE])))
        top_center = average(list(map(lambda x: x[1], self.average_values[landmark_enum.TOP_LIP_TOP_CENTER])))
        bottom_center = average(list(map(lambda x: x[1], self.average_values[landmark_enum.BOTTOM_LIP_BOTTOM_CENTER])))
        center = (top_center + bottom_center) / 2
        raw_smile = (center - edge) * self.scale

        return shape_thresholds.MOUTH_SMILE.lerp(raw_smile)

    def get_mouth_frown_right(self):
        edge = average(list(map(lambda x: x[1], self.average_values[landmark_enum.MOUTH_RIGHT_EDGE])))
        top_center = average(list(map(lambda x: x[1], self.average_values[landmark_enum.TOP_LIP_TOP_CENTER])))
        bottom_center = average(list(map(lambda x: x[1], self.average_values[landmark_enum.BOTTOM_LIP_BOTTOM_CENTER])))
        center = (top_center + bottom_center) / 2
        raw_frown = (edge - center) * self.scale

        return shape_thresholds.MOUTH_FROWN.lerp(raw_frown)

    def get_mouth_frown_left(self):
        edge = average(list(map(lambda x: x[1], self.average_values[landmark_enum.MOUTH_LEFT_EDGE])))
        top_center = average(list(map(lambda x: x[1], self.average_values[landmark_enum.TOP_LIP_TOP_CENTER])))
        bottom_center = average(list(map(lambda x: x[1], self.average_values[landmark_enum.BOTTOM_LIP_BOTTOM_CENTER])))
        center = (top_center + bottom_center) / 2
        raw_frown = (edge - center) * self.scale

        return shape_thresholds.MOUTH_FROWN.lerp(raw_frown)

    def get_right_eye_openness(self):
        top = average(list(map(lambda x: x[1], self.average_values[landmark_enum.RIGHT_EYE_TOP])))
        bottom = average(list(map(lambda x: x[1], self.average_values[landmark_enum.RIGHT_EYE_BOTTOM])))
        inner = average(list(map(lambda x: x[1], self.average_values[landmark_enum.RIGHT_EYE_INNER])))
        outer = average(list(map(lambda x: x[1], self.average_values[landmark_enum.RIGHT_EYE_OUTER])))

        height = abs(bottom - top)
        width = abs(inner - outer)

        aspect_ratio = 1 - width / height
        return shape_thresholds.EYE_OPENNESS.lerp(aspect_ratio)

    def get_left_eye_openness(self):
        top = average(list(map(lambda x: x[1], self.average_values[landmark_enum.LEFT_EYE_TOP])))
        bottom = average(list(map(lambda x: x[1], self.average_values[landmark_enum.LEFT_EYE_BOTTOM])))
        inner = average(list(map(lambda x: x[1], self.average_values[landmark_enum.LEFT_EYE_INNER])))
        outer = average(list(map(lambda x: x[1], self.average_values[landmark_enum.LEFT_EYE_OUTER])))

        height = abs(bottom - top)
        width = abs(inner - outer)

        aspect_ratio = 1 - width / height
        return shape_thresholds.EYE_OPENNESS.lerp(aspect_ratio)

    def render_debug(self, frame, landmarks):
        if frame is None:
            print("Frame missing")
            return
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