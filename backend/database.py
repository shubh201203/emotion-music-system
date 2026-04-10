from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

class DatabaseClient:
    def __init__(self):
        try:
            # Timeout quickly if MongoDB isn't running so the API doesn't hang
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            self.db = self.client["emotion_music_db"]
            self.feedback_coll = self.db["user_feedback"]
            
            # Ping to verify
            self.client.admin.command('ping')
            self.is_connected = True
            print("🧠 MongoDB Connected: AI Learning System Active")
            
        except Exception as e:
            self.is_connected = False
            print(f"⚠️ MongoDB not detected. Running without AI Memory learning. (Install MongoDB locally to enable) Error: {e}")

    def save_feedback(self, mood: str, song_id: str, feedback: str):
        if self.is_connected:
            doc = {
                "mood": mood,
                "song_id": song_id,
                "feedback": feedback, # "like" or "dislike"
            }
            self.feedback_coll.insert_one(doc)
            return True
        return False

    def get_learned_genre_preference(self, mood: str, default_genres: list) -> list:
        """
        AI Logic: Modifies the Spotify seed genres based on user history.
        If the user dislikes songs in a specific mood heavily, adapt the genres!
        """
        if not self.is_connected:
            return default_genres
            
        # Count recent negative feedback for this mood
        dislikes = self.feedback_coll.count_documents({"mood": mood, "feedback": "dislike"})
        
        # Artificial Intelligence Pivot Logic
        if dislikes >= 2:
            # If they keep disliking what we give for this mood, pivot the genre completely!
            if mood in ['Energetic', 'Excited']: return ['pop', 'indie'] # Pivot from dance
            if mood in ['Calm', 'Neutral']: return ['classical', 'piano'] # Pivot from acoustic
            if mood in ['Sad', 'Melancholic']: return ['blues', 'soul'] # Pivot from sad
            if mood == 'Intense': return ['electronic', 'techno'] # Pivot from rock
        
        return default_genres

db_client = DatabaseClient()
