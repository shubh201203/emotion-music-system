from pydantic import BaseModel
from typing import List, Optional, Dict

class Song(BaseModel):
    id: str
    title: str
    artist: str
    album_art: str
    url: str
    preview_url: Optional[str] = None
    genre: Optional[str] = None

class AnalysisResponse(BaseModel):
    primary_emotion: str
    emotion_scores: Dict[str, float]
    detected_mood: str
    songs: List[Song]
    error: Optional[str] = None

class FeedbackRequest(BaseModel):
    mood: str
    song_id: str
    feedback: str  # "like" or "dislike"
