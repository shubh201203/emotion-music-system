from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from schemas import AnalysisResponse, FeedbackRequest
from utils import decode_image
from emotion_model import emotion_analyzer
from fuzzy_engine import determine_mood
from spotify_client import spotify_client
from database import db_client

app = FastAPI(title="Emotion to Music Recommender API")

# CORS: Allow both local dev and deployed Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",       # Vite dev server
        "http://localhost:3000",       # Alternate dev port
        "https://*.vercel.app",        # All Vercel preview deploys
        "*",                           # Fallback — tighten after deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "mode": "deployed"}

class AnalyzeRequest(BaseModel):
    image_base64: str

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalyzeRequest):
    try:
        # 1. Decode and preprocess the base64 image
        img = decode_image(request.image_base64)
        
        # 2. Extract emotion using DeepFace
        dominant_emotion, emotions = emotion_analyzer.analyze_emotion(img)
        
        # 3. Convert emotion probabilities to Spotify audio features (Mood)
        mood_data = determine_mood(emotions)
        
        # 4. Fetch songs from Spotify (or mock data if unconfigured)
        songs = spotify_client.get_recommendations(mood_data, limit=4)
        
        return AnalysisResponse(
            primary_emotion=dominant_emotion,
            emotion_scores=emotions,
            detected_mood=mood_data["mood_name"],
            songs=songs
        )
        
    except Exception as e:
        # Fallback response for graceful UI error handling
        return AnalysisResponse(
            primary_emotion="Error",
            emotion_scores={},
            detected_mood="Error",
            songs=[],
            error=str(e)
        )

@app.post("/feedback")
async def handle_feedback(req: FeedbackRequest):
    # Save the feedback into MongoDB history
    success = db_client.save_feedback(req.mood, req.song_id, req.feedback)
    return {"status": "success", "learned": success}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
