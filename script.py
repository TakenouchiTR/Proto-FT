import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import cv2
import mediapipe as mp
import settings
import shape
from lerp_shape import LerpShape
import json
import mp_landmarks
import shape_thresholds

# Load mouth shapes
with open("shapes/mouth_closed.json", "r") as f:
    mouth_closed = shape.from_json(json.load(f))
with open("shapes/mouth_open.json", "r") as f:
    mouth_open = shape.from_json(json.load(f))
lerp_shape = LerpShape(mouth_closed)
lerp_shape.add_shape("open", mouth_open)

# Initialize Mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Tkinter setup
root = tk.Tk()
root.title("LED Panel Simulation")
canvas_width = settings.MATRIX_WIDTH * 10
canvas_height = settings.MATRIX_HEIGHT * 10
panel = tk.Label(root)
panel.pack()

# Webcam capture setup
cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640 * 3)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480 * 3)

rolling_average_amount = 0
rolling_average_max = 10
average_values = {}

def average(values):
    return sum(values) / len(values)

# Function to calculate mouth openness
def get_mouth_openness():
    global average_values

    top = average(list(map(lambda x: x[1], average_values[mp_landmarks.TOP_LIP_BOTTOM_CENTER])))
    bottom = average(list(map(lambda x: x[1], average_values[mp_landmarks.BOTTOM_LIP_TOP_CENTER])))
    return abs(bottom - top)

def update_averages(landmarks):
    global average_values, rolling_average_max

    for id, lm in enumerate(landmarks):
        values = average_values.get(id, [])
        values.append((lm.x, lm.y))
        if len(values) > rolling_average_max:
            values.pop(0)
        average_values[id] = values

def update_frame():
    ret, frame = cap.read()
    if not ret:
        root.after(50, update_frame)
        return

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = rgb_frame.shape
    results = face_mesh.process(rgb_frame)

    img = Image.new('RGB', (settings.MATRIX_WIDTH, settings.MATRIX_HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        update_averages(landmarks)
        open_value = get_mouth_openness()
        openness = shape_thresholds.MOUTH_OPENNESS.lerp(open_value)


        lerp_shape.update_shape_strength("open", openness)
        # if openness > 15:
        #     lerp_shape.update_shape_strength("closed", 0)
        # else:
        #     lerp_shape.update_shape_strength("closed", 1)

        draw.polygon(lerp_shape.lerped_shape.points, fill=(255, 100, 100))

        # Draw landmarks with IDs on camera frame
        for id, lm in enumerate(landmarks):
            x = int(lm.x * image_width)
            y = int(lm.y * image_height)
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
            cv2.putText(frame, str(id), (x + 2, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1)

    # Show debug camera feed
    cv2.imshow("Face Tracking Debug", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        root.destroy()
        cap.release()
        cv2.destroyAllWindows()
        return

    # Update LED simulation
    imgtk = ImageTk.PhotoImage(img.resize((canvas_width, canvas_height), resample=Image.NEAREST))
    panel.config(image=imgtk)
    panel.image = imgtk

    root.after(1, update_frame)

# Start the loop in main thread
update_frame()
root.mainloop()
