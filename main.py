# src/main.py
import cv2
from .audio_listener_simple import AudioListener
from .video_overlay import TextOverlayState, draw_text_widget
from .translation_pipeline import make_translating_callback
from . import config

def main():
    text_state = TextOverlayState()

    # Wrap the original callback with a translating layer
    translated_callback = make_translating_callback(
        text_state.add_line,
        target_lang="en",  # convert everything to English
    )

    # --- Start audio listener thread ---
    audio_thread = AudioListener(text_callback=translated_callback)
    audio_thread.start()

    # --- Start camera capture ---
    cap = cv2.VideoCapture(0)  # 0 = default camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        audio_thread.stop()
        return

    cv2.namedWindow(config.WINDOW_NAME)

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from camera.")
            break

        # Get the latest lines to display
        lines = text_state.get_lines()

        # Draw the widget on the frame
        frame = draw_text_widget(frame, lines)

        cv2.imshow(config.WINDOW_NAME, frame)

        # Exit on 'q'
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # Cleanup
    print("Shutting down...")
    audio_thread.stop()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
