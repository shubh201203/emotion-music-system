from deepface import DeepFace
import cv2
import numpy as np

class EmotionRecommender:
    def __init__(self):
        print("Initializing Emotion Model...")
        # Build the model upfront to avoid lag on first request
        try:
            DeepFace.build_model("Emotion")
            print("Emotion Model cached successfully.")
        except Exception as e:
            print(f"Warning: Model pre-build failed. {e}")

    def analyze_emotion(self, img: np.ndarray):
        """
        Analyzes emotion from image.
        """
        try:
            # enforce_detection=False allows processing even if face is partially visible
            results = DeepFace.analyze(
                img_path=img, 
                actions=['emotion'], 
                enforce_detection=False,
                silent=True
            )
            # DeepFace returns a list of results if multiple faces. We take the primary one.
            res = results[0]
            emotions = res['emotion']
            dominant = res['dominant_emotion']
            return dominant, emotions
        except Exception as e:
            raise Exception(f"Emotion analysis failed: {str(e)}")

# Singleton instance
emotion_analyzer = EmotionRecommender()
