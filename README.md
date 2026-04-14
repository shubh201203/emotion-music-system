# 🎧 Emotion-Driven Beats (AI Top 1% Project)

## 🌐 Live Demo
- **Frontend**: [https://emotion-music-system.vercel.app](https://emotion-music-system.vercel.app)
- **Backend API**: [https://emotion-music-system-unge.onrender.com](https://emotion-music-system-unge.onrender.com)

## 🧠 What is this?
An industry-grade, full-stack application that utilizes **Real-Time Facial Emotion Recognition** mapped dynamically through a **Fuzzy Logic Math Engine** to seamlessly request curated, personalized audio playback from the **Spotify Web API**. It learns over time via an AI feedback loop!

## 💻 Tech Stack
- **Frontend**: React + Vite + Framer Motion (Glassmorphism & pure Vanilla CSS styling)
- **Backend**: FastAPI + Python (Asynchronous Architecture)
- **AI Core**: DeepFace + OpenCV (Local Mode) / Lightweight Pixel Analysis (Deployed Mode)
- **Database**: MongoDB (User Learning History)
- **APIs**: Spotify Developer APIs (Tracks, Genres, Music Previews)

## 🔄 Dual-Mode Architecture

### 💻 LOCAL MODE (Full AI Demo)
- Full DeepFace + TensorFlow inference
- Real CNN-based facial emotion recognition
- Best for live demos and presentations

### 🌐 DEPLOYED MODE (Online Submission)
- Lightweight pixel-analysis emotion engine
- Zero heavy ML dependencies — fast cold starts
- Crash-free on Render free tier

## 🚀 Local Development
1. **Start the Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```
2. **Start the Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## ☁️ Deployment

### Backend → Render
1. Create a **Web Service** on [render.com](https://render.com)
2. Connect your GitHub repo
3. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. Add ENV variables: `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`
5. Deploy → Get your backend URL

### Frontend → Vercel
1. Import repo on [vercel.com](https://vercel.com)
2. Set **Root Directory**: `frontend`
3. Add ENV variable: `VITE_API_URL=https://your-backend.onrender.com`
4. Deploy → Get your frontend URL

*(This project was highly optimized for latency, robust Spotify Search engine integration, and complete API resilience).*
