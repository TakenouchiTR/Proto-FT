import mediapipe as mp
import cv2

from face_tracking_parameters import FaceTrackingParameters
import mp_landmarks
import settings
import shape_thresholds

class FaceTracker():
    def __init__(self):
        cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.FT_CAPTURE_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.FT_CAPTURE_HEIGHT)
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

        self.cap = cap
        self.face_mesh = face_mesh
        self.average_values = {}
        self.rolling_average_amount = 0
        self.parameters = FaceTrackingParameters()

    def average(self, values):
        return sum(values) / len(values)

    def update_averages(self, landmarks):
        for id, lm in enumerate(landmarks):
            values = self.average_values.get(id, [])
            values.append((lm.x, lm.y))
            if len(values) > settings.ROLLING_AVERAGE_MAX:
                values.pop(0)
            self.average_values[id] = values

    def update_scale(self, landmarks):
        left_edge = landmarks[mp_landmarks.HEAD_LEFT_EDGE]
        right_edge = landmarks[mp_landmarks.HEAD_RIGHT_EDGE]
        self.scale =  1 / abs(left_edge.x - right_edge.x)

    def get_mouth_openness(self):
        top = self.average(list(map(lambda x: x[1], self.average_values[mp_landmarks.TOP_LIP_BOTTOM_CENTER])))
        bottom = self.average(list(map(lambda x: x[1], self.average_values[mp_landmarks.BOTTOM_LIP_TOP_CENTER])))
        raw_openness = abs(bottom - top) * self.scale
        return shape_thresholds.MOUTH_OPENNESS.lerp(raw_openness)
    
    def get_right_eye_openness(self):
        top = self.average(list(map(lambda x: x[1], self.average_values[mp_landmarks.RIGHT_EYE_TOP])))
        bottom = self.average(list(map(lambda x: x[1], self.average_values[mp_landmarks.RIGHT_EYE_BOTTOM])))
        raw_openness = abs(bottom - top) * self.scale
        print(raw_openness)
        return shape_thresholds.EYE_OPENNESS.lerp(raw_openness)

    def render_debug(self, frame, landmarks):
        try:
            values = [
                v for k, v in vars(mp_landmarks).items()
                if not k.startswith("__") and not callable(v)
            ]
            for id, lm in enumerate(landmarks):
                if id not in values and not settings.SHOW_ALL_DEBUG_LANDMARKS:
                    continue
                x = int(lm.x * settings.FT_CAPTURE_WIDTH)
                y = int(lm.y * settings.FT_CAPTURE_HEIGHT)
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                cv2.putText(frame, str(id), (x + 2, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1)
            cv2.imshow("Face Tracking Debug", frame)
            cv2.waitKey(1)
        except:
            pass

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            if settings.SHOW_DEBUG:
                self.render_debug(frame, [])
            return None
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if not results.multi_face_landmarks:
            if settings.SHOW_DEBUG:
                self.render_debug(frame, [])
            return None

        landmarks = results.multi_face_landmarks[0].landmark
        self.update_averages(landmarks)

        self.update_scale(landmarks)
        self.parameters.mouth_openness = self.get_mouth_openness()
        self.parameters.right_eye_openness = self.get_right_eye_openness()

        if settings.SHOW_DEBUG:
            self.render_debug(frame, landmarks)

        return self.parameters