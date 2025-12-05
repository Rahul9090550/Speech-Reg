# src/video_overlay.py

import threading
import cv2
import numpy as np
from . import config


class TextOverlayState:
    """
    Thread-safe storage for recent recognized text lines.
    """

    def __init__(self, max_lines=None):
        self._lock = threading.Lock()
        self._lines = []
        self.max_lines = max_lines or config.MAX_TEXT_LINES

    def add_line(self, text: str):
        text = text.strip()
        if not text:
            return
        with self._lock:
            self._lines.append(text)
            # Keep only last N lines
            self._lines = self._lines[-self.max_lines:]

    def get_lines(self):
        with self._lock:
            return list(self._lines)


def draw_text_widget(frame, lines):
    """
    Draws the semi-transparent widget at the bottom of the frame
    containing the recent recognized text lines.
    """
    if not lines:
        return frame

    h, w, _ = frame.shape

    # Calculate widget height based on number of lines
    box_height = config.MARGIN_Y * 2 + config.LINE_SPACING * len(lines)
    y1 = h - box_height
    y2 = h

    # Create overlay for transparency
    overlay = frame.copy()
    cv2.rectangle(
        overlay,
        (0, y1),
        (w, y2),
        config.BOX_COLOR,
        thickness=-1
    )

    # Blend overlay with original frame
    cv2.addWeighted(
        overlay, config.BOX_ALPHA,
        frame, 1 - config.BOX_ALPHA,
        0,
        frame
    )

    # Put text lines
    y_text = y1 + config.MARGIN_Y + 20
    for line in lines:
        cv2.putText(
            frame,
            line,
            (config.MARGIN_X, y_text),
            config.FONT,
            config.FONT_SCALE,
            config.TEXT_COLOR,
            config.FONT_THICKNESS,
            cv2.LINE_AA
        )
        y_text += config.LINE_SPACING

    return frame
