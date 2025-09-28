import json

from face_tracking_parameters import FaceTrackingParameters
from lerp_shape import LerpShape
import settings


def load_face_shapes_from_file(filename):
    with open(filename, 'r') as f:
        shapes = json.load(f)
    
    left_mouth_lerp_shape = LerpShape(shapes["mouth"]["closed"])
    left_mouth_lerp_shape.add_shape("open", shapes["mouth"]["open"])
    left_mouth_lerp_shape.add_shape("smile", shapes["mouth"]["smile"])
    left_mouth_lerp_shape.add_shape("frown", shapes["mouth"]["frown"])
    left_mouth_lerp_shape.add_shape("pog", shapes["mouth"]["pog"])


    right_mouth_lerp_shape = LerpShape(shapes["mouth"]["closed"])
    right_mouth_lerp_shape.add_shape("open", shapes["mouth"]["open"])
    right_mouth_lerp_shape.add_shape("smile", shapes["mouth"]["smile"])
    right_mouth_lerp_shape.add_shape("frown", shapes["mouth"]["frown"])
    right_mouth_lerp_shape.add_shape("pog", shapes["mouth"]["pog"])

    right_eye_lerp_shape = LerpShape(shapes["eye"]["closed"])
    right_eye_lerp_shape.add_shape("open", shapes["eye"]["open"])

    left_eye_lerp_shape = LerpShape(shapes["eye"]["closed"])
    left_eye_lerp_shape.add_shape("open", shapes["eye"]["open"])
    
    face_shapes = FaceShapes()
    face_shapes.left_mouth = left_mouth_lerp_shape
    face_shapes.right_mouth = right_mouth_lerp_shape
    face_shapes.left_eye = left_eye_lerp_shape
    face_shapes.right_eye = right_eye_lerp_shape

    face_shapes._shapes = [
        left_mouth_lerp_shape,
        right_mouth_lerp_shape,
        left_eye_lerp_shape,
        right_eye_lerp_shape
    ]

    return face_shapes
    

class FaceShapes:
    def __init__(self):
        self.left_mouth: LerpShape
        self.right_mouth: LerpShape
        self.left_eye: LerpShape
        self.right_eye: LerpShape

        self._shapes = []
    
    def apply_weights(self, parameters: FaceTrackingParameters):
        self.right_mouth.update_shape_strength("open", parameters.mouth_openness)
        self.right_mouth.update_shape_strength("smile", parameters.smile_right)
        self.right_mouth.update_shape_strength("frown", parameters.frown_right)
        self.right_mouth.update_shape_strength("pog", parameters.mouth_pog)
        self.left_mouth.update_shape_strength("open", parameters.mouth_openness)
        self.left_mouth.update_shape_strength("smile", parameters.smile_left)
        self.left_mouth.update_shape_strength("frown", parameters.frown_left)
        self.left_mouth.update_shape_strength("pog", parameters.mouth_pog)
        self.right_eye.update_shape_strength("open", parameters.right_eye_openness)
        self.left_eye.update_shape_strength("open", parameters.left_eye_openness)
    
    def __iter__(self):
        return iter(self._shapes)

    def __getitem__(self, index):
        return self._shapes[index]
