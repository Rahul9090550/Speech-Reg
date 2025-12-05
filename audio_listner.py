# src/audio_listener.py

import threading
import time
import speech_recognition as sr


class AudioListener(threading.Thread):
    """
    Continuously listens to the microphone, converts speech to text,
    and pushes recognized phrases to a callback.
    """

    def __init__(self, text_callback, energy_threshold=300, pause_threshold=0.8):
        super().__init__(daemon=True)
        self.text_callback = text_callback
        self.energy_threshold = energy_threshold
        self.pause_threshold = pause_threshold
        self._running = True

    def stop(self):
        """Signal the thread to stop gracefully."""
        self._running = False

    def run(self):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = self.energy_threshold
        recognizer.pause_threshold = self.pause_threshold

        with sr.Microphone() as source:
            print("[Audio] Calibrating microphone for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("[Audio] Calibration done. Start speaking!")

            while self._running:
                try:
                    print("[Audio] Listening...")
                    audio = recognizer.listen(source, phrase_time_limit=5)

                    # You can replace recognize_google with any other engine if needed
                    print("[Audio] Recognizing...")
                    text = recognizer.recognize_google(audio, language="en-IN")
                    print(f"[Audio] Recognized: {text}")
                    self.text_callback(text)

                except sr.UnknownValueError:
                    print("[Audio] Could not understand audio.")
                except sr.RequestError as e:
                    print(f"[Audio] API error: {e}")
                    self.text_callback("[Speech API error – check internet]")
                    time.sleep(2)
                except Exception as e:
                    print(f"[Audio] Unexpected error: {e}")
                    time.sleep(1)
