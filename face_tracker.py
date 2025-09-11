import mediapipe as mp
import cv2

from face_tracking_parameters import FaceTrackingParameters
import mp_landmarks
import settings
import shape_thresholds

ROLLING_AVERAGE_MAX = 20

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
            if len(values) > ROLLING_AVERAGE_MAX:
                values.pop(0)
            self.average_values[id] = values

    def get_mouth_openness(self):
        top = self.average(list(map(lambda x: x[1], self.average_values[mp_landmarks.TOP_LIP_BOTTOM_CENTER])))
        bottom = self.average(list(map(lambda x: x[1], self.average_values[mp_landmarks.BOTTOM_LIP_TOP_CENTER])))
        return abs(bottom - top)
    
    def render_debug(self, frame, landmarks):
        for id, lm in enumerate(landmarks):
            x = int(lm.x * settings.FT_CAPTURE_WIDTH)
            y = int(lm.y * settings.FT_CAPTURE_HEIGHT)
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
            cv2.putText(frame, str(id), (x + 2, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1)
        cv2.imshow("Face Tracking Debug", frame)

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if not results.multi_face_landmarks:
            return None

        landmarks = results.multi_face_landmarks[0].landmark
        self.update_averages(landmarks)
        open_value = self.get_mouth_openness()
        self.parameters.mouth_openness = shape_thresholds.MOUTH_OPENNESS.lerp(open_value)

        if settings.SHOW_DEBUG:
            self.render_debug(frame, landmarks)

        return self.parameters