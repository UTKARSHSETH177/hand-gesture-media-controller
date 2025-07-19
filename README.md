
# Hand Gesture Media Controller

This project lets you control system volume and media playback with hand gestures:
- Pinch (thumb + index) for volume.
- Fist for mute/unmute.
- Open palm for play/pause.
- Two fingers for next track.
- Three fingers for previous track.

## Setup

1. Clone the repo  
   ```bash
   git clone https://github.com/your-username/hand-gesture-media-controller.git
   cd hand-gesture-media-controller
   ```
2. (Optional) Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   ```
3. Install dependencies
   pip install -r requirements.txt

Usage
python src/gesture_controller.py

Make sure your webcam is connected. A GUI window will open showing live video, volume slider, and last gesture performed.
Customization
- Adjust pinch distance range and smoothing in gesture_controller.py.
- Add new gestures by extending the finger-count logic.
- Swap pyautogui for keyboard or pynput for cross-platform media keys.

