# src/audio_listener_simple.py

import threading
import time
import speech_recognition as sr


class AudioListener(threading.Thread):
    """
    Simple audio listener:
    - Listens to microphone in a background thread
    - Uses Google STT via SpeechRecognition
    - Sends recognized text to a callback
    """

    def __init__(self, text_callback, energy_threshold=300, pause_threshold=0.8):
        super().__init__(daemon=True)
        self.text_callback = text_callback
        self.energy_threshold = energy_threshold
        self.pause_threshold = pause_threshold
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = self.energy_threshold
        recognizer.pause_threshold = self.pause_threshold

        try:
            with sr.Microphone() as source:
                print("[Audio] Calibrating mic for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("[Audio] Done. Start speaking!")

                while self._running:
                    try:
                        print("[Audio] Listening...")
                        audio = recognizer.listen(source, phrase_time_limit=5)

                        print("[Audio] Recognizing...")
                        text = recognizer.recognize_google(audio, language="en-IN")
                        print(f"[Audio] Recognized: {text}")
                        self.text_callback(text)

                    except sr.UnknownValueError:
                        print("[Audio] Could not understand audio.")
                    except sr.RequestError as e:
                        msg = f"[Speech API error: {e}]"
                        print("[Audio]", msg)
                        self.text_callback(msg)
                        time.sleep(2)
                    except Exception as e:
                        print(f"[Audio] Unexpected error: {e}")
                        time.sleep(1)
        except Exception as e:
            print(f"[Audio] Failed to open microphone: {e}")
            self.text_callback("[Mic error – check input device]")
