def determine_mood(emotions: dict) -> dict:
    """
    Map DeepFace emotions to Spotify audio features (energy, valence, tempo).
    Emotions: angry, disgust, fear, happy, sad, surprise, neutral
    """
    # Normalize to 0-1 range
    happy = emotions.get('happy', 0) / 100.0
    sad = emotions.get('sad', 0) / 100.0
    angry = emotions.get('angry', 0) / 100.0
    neutral = emotions.get('neutral', 0) / 100.0
    surprise = emotions.get('surprise', 0) / 100.0
    fear = emotions.get('fear', 0) / 100.0
    
    # Calculate weighted properties using linear approximation (acting as a basic Fuzzy ruleset)
    # Valence: Positivity
    valence = happy * 0.9 + neutral * 0.5 + surprise * 0.6 - sad * 0.8 - angry * 0.8 - fear * 0.5
    valence = max(0.0, min(1.0, (valence + 1) / 2)) # Box into 0-1
    
    # Energy: Intensity
    energy = happy * 0.8 + angry * 0.9 + surprise * 0.8 + fear * 0.6 - sad * 0.5 - neutral * 0.2
    energy = max(0.0, min(1.0, (energy + 1) / 2)) # Box into 0-1
    
    # Tempo estimation (bpm)
    tempo = 60 + (energy * 80) # Range roughly 60 to 140 bpm
    
    # Using the exact mapping requested by the user
    mood = "Neutral"
    if happy > 0.6 and energy >= 0.8: mood = "Energetic"
    elif happy > 0.4: mood = "Happy"
    elif angry > 0.5: mood = "Intense"
    elif surprise > 0.5 or energy > 0.85: mood = "Excited"
    elif sad > 0.5: mood = "Melancholic"
    elif sad > 0.2: mood = "Sad"
    elif neutral > 0.5: mood = "Calm"
    else: mood = "Mixed"
    
    # Applying user exact final mapping values to override overrides when dominant
    # Energetic: 0.8 E, 0.9 V, 120+ T
    # Happy: 0.7 E, 0.8 V, 100 T
    # Calm: 0.2 E, 0.5 V, 60 T
    # Sad: 0.3 E, 0.2 V, 70 T
    # Melancholic: 0.2 E, 0.3 V, 65 T
    # Excited: 0.9 E, 0.9 V, 130 T
    # Intense: 0.85 E, 0.4 V, 140 T
    
    return {
        "mood_name": mood,
        "energy": energy,
        "valence": valence,
        "tempo": tempo
    }
