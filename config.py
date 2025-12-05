# src/config.py

WINDOW_NAME = "Live Voice Overlay"
MAX_TEXT_LINES = 5  # how many recent phrases to show

# OpenCV text settings
FONT = 0  # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
FONT_THICKNESS = 2

TEXT_COLOR = (255, 255, 255)  # white
BOX_COLOR = (0, 0, 0)         # black (for background box)
BOX_ALPHA = 0.5               # transparency (0-1)
LINE_SPACING = 30             # pixels between lines
MARGIN_X = 20
MARGIN_Y = 20
