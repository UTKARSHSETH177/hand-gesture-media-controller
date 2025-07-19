
import cv2
import mediapipe as mp
import pyautogui
import PySimpleGUI as sg
import numpy as np
import math
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

# Gesture settings
PINCH_MIN, PINCH_MAX = 20, 200
SMOOTHING = 5

# Build GUI layout
layout = [
    [sg.Image(key='-IMAGE-')],
    [sg.Text("Volume:"), sg.Slider(range=(0,100), orientation='h', key='-VOL-')],
    [sg.Text("Last Gesture:"), sg.Text("", key='-GESTURE-')]
]
window = sg.Window("Hand Gesture Media Controller", layout, location=(100,100))

def count_fingers(landmarks, w, h):
    tips = [4, 8, 12, 16, 20]
    count = 0
    # Thumb: compare x positions
    if landmarks[tips[0]].x * w < landmarks[tips[0]-1].x * w:
        count += 1
    # Other fingers: tip above pip
    for i in range(1, 5):
        if landmarks[tips[i]].y * h < landmarks[tips[i]-2].y * h:
            count += 1
    return count

last_vol = 0
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = ""
    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark
        mp_draw.draw_landmarks(frame, result.multi_hand_landmarks[0],
                               mp_hands.HAND_CONNECTIONS)

        # Pinch for volume
        x1, y1 = int(lm[4].x*w), int(lm[4].y*h)
        x2, y2 = int(lm[8].x*w), int(lm[8].y*h)
        dist = math.hypot(x2-x1, y2-y1)
        vol = int(np.interp(dist, [PINCH_MIN, PINCH_MAX], [0,100]))
        if abs(vol - last_vol) > SMOOTHING:
            pyautogui.press("volumeup" if vol > last_vol else "volumedown")
            last_vol = vol
        gesture = f"Volume: {last_vol}%"

        # Other gestures
        fingers = count_fingers(lm, w, h)
        if fingers == 0:
            pyautogui.press("volumemute")
            gesture = "Mute/Unmute"
            time.sleep(0.5)
        elif fingers == 5:
            pyautogui.press("playpause")
            gesture = "Play/Pause"
            time.sleep(0.5)
        elif fingers == 2:
            pyautogui.press("nexttrack")
            gesture = "Next Track"
            time.sleep(0.5)
        elif fingers == 3:
            pyautogui.press("prevtrack")
            gesture = "Previous Track"
            time.sleep(0.5)

    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    window['-IMAGE-'].update(data=imgbytes)
    window['-VOL-'].update(last_vol)
    window['-GESTURE-'].update(gesture)

    if window.read(timeout=20)[0] == sg.WIN_CLOSED:
        break

cap.release()
window.close()
