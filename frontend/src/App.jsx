import { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Camera, Music, PlayCircle, Loader2, ThumbsUp, ThumbsDown, CheckCircle, RefreshCw } from 'lucide-react';

// Reads from env at build time. Set VITE_API_URL in Vercel dashboard.
// Falls back to localhost for local development.
const BACKEND = import.meta.env.VITE_API_URL || "http://localhost:8000";
const API_URL = `${BACKEND}/analyze`;
const FEEDBACK_URL = `${BACKEND}/feedback`;

export default function App() {
  const webcamRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [feedbackGiven, setFeedbackGiven] = useState({});
  const [scanHistory, setScanHistory] = useState([]);
  const [toastMessage, setToastMessage] = useState("");

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(""), 3000);
  };

  const captureAndAnalyze = useCallback(async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) return;

    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(API_URL, {
        image_base64: imageSrc
      });
      if (response.data.error) {
        setError(response.data.error);
        setResult(null);
      } else {
        setResult(response.data);
        setFeedbackGiven({}); // Reset feedback on new scan
        showToast("Emotion detected successfully!");
        setScanHistory(prev => {
          const entry = `${response.data.primary_emotion.toUpperCase()} ➔ ${response.data.detected_mood}`;
          return [entry, ...prev].slice(0, 3);
        });
      }
    } catch (err) {
      console.error(err);
      setError("Failed to connect to the analysis engine. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }, [webcamRef]);

  // Color mapping for emotion bars
  const getEmotionColor = (emotion) => {
    const colors = {
      happy: '#22c55e',
      sad: '#3b82f6',
      angry: '#ef4444',
      neutral: '#94a3b8',
      surprise: '#eab308',
      fear: '#8b5cf6',
      disgust: '#c026d3'
    };
    return colors[emotion] || '#6366f1';
  };

  const submitFeedback = async (songId, feedbackType) => {
    if (!result) return;
    
    // Optimistic UI update
    setFeedbackGiven(prev => ({
      ...prev,
      [songId]: feedbackType
    }));

    try {
      await axios.post(FEEDBACK_URL, {
        mood: result.detected_mood,
        song_id: songId,
        feedback: feedbackType
      });
    } catch (err) {
      console.error("Failed to submit feedback", err);
    }
  };

  return (
    <div className="app-container">
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="header"
      >
        <h1>Emotion-Driven Beats</h1>
        <p>AI detects your mood and curates the perfect Spotify playlist.</p>
      </motion.div>

      <div className="main-content">
        {/* Left Col: Camera */}
        <motion.div 
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-panel camera-container"
        >
          <div style={{ position: 'relative', width: '100%' }}>
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              className="webcam-feed"
              videoConstraints={{ facingMode: "user" }}
              onUserMediaError={() => setError("Camera access denied! Please check permissions.")}
            />
            
            <AnimatePresence>
              {loading && (
                <motion.div 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="loader-overlay"
                >
                  <div className="spinner"></div>
                  <div className="loading-text">Analyzing your emotions...</div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <button 
            className="glow-button"
            onClick={captureAndAnalyze}
            disabled={loading}
          >
            {loading ? <Loader2 className="animate-spin" size={20} /> : <Camera size={20} />}
            {loading ? 'Processing...' : 'Detect Mood & Get Music'}
          </button>
          
          {error && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="error-message">
              {error}
            </motion.div>
          )}

          {scanHistory.length > 0 && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="history-panel">
              <h4 style={{ color: '#e2e8f0', marginBottom: '8px', fontSize: '0.9rem' }}>🕒 Emotion History</h4>
              {scanHistory.map((h, i) => (
                <div key={i} className="history-item">Recent: {h}</div>
              ))}
            </motion.div>
          )}
        </motion.div>

        {/* Right Col: Results */}
        <motion.div 
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-panel results-container"
        >
          {!result ? (
            <div style={{ textAlign: 'center', color: '#94a3b8', margin: 'auto', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
              <Music size={48} opacity={0.5} />
              <p>Snap a photo to reveal your music recommendations.</p>
            </div>
          ) : (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ staggerChildren: 0.1 }}
              style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <h3 style={{ marginBottom: '12px', color: '#e2e8f0' }}>🎧 Mood Detected</h3>
                  <div className="mood-badge" style={{ fontSize: '1.3rem', letterSpacing: '1px', textTransform: 'uppercase', boxShadow: '0 0 15px rgba(99, 102, 241, 0.4)'}}>
                    {result.detected_mood}
                  </div>
                </div>
                <button 
                  onClick={() => setResult(null)} 
                  className="glow-button" 
                  style={{ padding: '8px 16px', fontSize: '0.9rem', background: 'transparent', border: '1px solid #6366f1' }}
                >
                  <RefreshCw size={16} /> Scan Again
                </button>
              </div>

              {/* Confidence Bars */}
              <div className="emotion-bars">
                <h4 style={{ color: '#cbd5e1', fontSize: '0.9rem', marginBottom: '8px' }}>Emotion Analysis</h4>
                {Object.entries(result.emotion_scores || {})
                  .sort(([, a], [, b]) => b - a)
                  .slice(0, 4) // Show top 4 emotions
                  .map(([emotion, score]) => (
                    <div key={emotion} className="emotion-bar-item">
                      <span className="emotion-label">{emotion}</span>
                      <div className="bar-track">
                        <motion.div 
                          className="bar-fill"
                          initial={{ width: 0 }}
                          animate={{ width: `${Math.max(2, score)}%` }}
                          style={{ backgroundColor: getEmotionColor(emotion) }}
                        />
                      </div>
                      <span className="emotion-value">{score.toFixed(0)}%</span>
                    </div>
                ))}
              </div>

              {/* Recommended Songs */}
              <div>
                <h3 style={{ marginBottom: '16px', color: '#e2e8f0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <PlayCircle size={20} color="#6366f1" /> Personalized Playlist
                </h3>
                {result.songs.length === 0 ? (
                  <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>No songs found for this mood.</p>
                ) : (
                  <div className="songs-grid">
                    {result.songs.map((song, idx) => (
                      <motion.div 
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.1 }}
                        key={song.id} 
                        className="song-card"
                      >
                        <img src={song.album_art} alt={song.title} className="song-art" />
                        <div className="song-info">
                          <h4>{song.title}</h4>
                          <p>{song.artist}</p>
                          {song.genre && <span className="genre-tag">{song.genre}</span>}
                          
                          {song.preview_url ? (
                            <audio controls src={song.preview_url} />
                          ) : (
                            <p style={{fontSize: '0.75rem', marginTop: '6px', fontStyle: 'italic', color: '#64748b'}}>Audio preview not available</p>
                          )}
                          
                          <a href={song.url} target="_blank" rel="noreferrer" className="spotify-link spotify-flex" style={{marginTop: '10px'}}>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                              <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.24 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.24 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.6.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.54-1.02.72-1.56.3z" />
                            </svg>
                            Listen on Spotify
                          </a>
                        </div>
                        <div className="feedback-actions">
                          <button 
                            className={`feedback-btn ${feedbackGiven[song.id] === 'like' ? 'active-like' : ''}`}
                            onClick={() => submitFeedback(song.id, 'like')}
                          >
                            <ThumbsUp size={14} /> Like
                          </button>
                          <button 
                            className={`feedback-btn ${feedbackGiven[song.id] === 'dislike' ? 'active-dislike' : ''}`}
                            onClick={() => submitFeedback(song.id, 'dislike')}
                          >
                            <ThumbsDown size={14} /> Dislike
                          </button>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </motion.div>
      </div>

      {/* Toast Notification */}
      <AnimatePresence>
        {toastMessage && (
          <motion.div 
            initial={{ opacity: 0, y: 50 }} 
            animate={{ opacity: 1, y: 0 }} 
            exit={{ opacity: 0, y: 50 }} 
            className="toast"
          >
            <CheckCircle size={18} /> {toastMessage}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Authenticity Footer */}
      <div style={{ textAlign: 'center', marginTop: '3rem', paddingBottom: '1rem', color: '#64748b', fontSize: '0.85rem', letterSpacing: '1.5px', textTransform: 'uppercase' }}>
        Engineered by <span style={{ color: '#8b5cf6', fontWeight: 'bold', textShadow: '0 0 10px rgba(139, 92, 246, 0.4)' }}>Shubh • Harshit • Aritra</span>
      </div>
    </div>
  );
}
