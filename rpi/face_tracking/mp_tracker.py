import cv2
from face_tracking import landmarks as landmark_enum
from face_tracking.face_tracker import FaceTracker
import settings
import mediapipe as mp

from utils import average

mp_landmark_mapping = {
    0: landmark_enum.TOP_LIP_TOP_CENTER,
    13: landmark_enum.TOP_LIP_BOTTOM_CENTER,
    14: landmark_enum.BOTTOM_LIP_TOP_CENTER,
    17: landmark_enum.BOTTOM_LIP_BOTTOM_CENTER,

    291: landmark_enum.MOUTH_RIGHT_EDGE,
    61: landmark_enum.MOUTH_LEFT_EDGE,

    473: landmark_enum.RIGHT_EYE_CENTER,
    475: landmark_enum.RIGHT_EYE_TOP,
    477: landmark_enum.RIGHT_EYE_BOTTOM,
    398: landmark_enum.RIGHT_EYE_INNER,
    263: landmark_enum.RIGHT_EYE_OUTER,

    386: landmark_enum.RIGHT_EYE_LID_TOP,
    374: landmark_enum.RIGHT_EYE_LID_BOTTOM,

    468: landmark_enum.LEFT_EYE_CENTER,
    470: landmark_enum.LEFT_EYE_TOP,
    472: landmark_enum.LEFT_EYE_BOTTOM,
    173: landmark_enum.LEFT_EYE_INNER,
    33: landmark_enum.LEFT_EYE_OUTER,

    159: landmark_enum.LEFT_EYE_LID_TOP,
    145: landmark_enum.LEFT_EYE_LID_BOTTOM,

    234: landmark_enum.HEAD_LEFT_EDGE,
    454: landmark_enum.HEAD_RIGHT_EDGE,
}

class MpTracker(FaceTracker):
    def __init__(self):
        super().__init__()

        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
        self.face_mesh = face_mesh

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            if settings.SHOW_DEBUG:
                self.render_debug(frame, [])
            return None
        
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (512, 512))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if not results.multi_face_landmarks:
            if settings.SHOW_DEBUG:
                self.render_debug(frame, [])
            return None

        mp_landmarks = results.multi_face_landmarks[0].landmark
        landmarks = {mp_landmark_mapping[id]: mp_landmarks[id] for id in mp_landmark_mapping.keys()}
        self.update_averages(landmarks)

        self.update_scale(landmarks)
        self.update_parameters()

        if settings.SHOW_DEBUG:
            self.render_debug(frame, landmarks)

        return self.parameters