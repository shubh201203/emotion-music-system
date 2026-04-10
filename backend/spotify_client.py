import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from schemas import Song
from database import db_client

class SpotifyRecommender:
    def __init__(self):
        self.client = None
        if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET and SPOTIFY_CLIENT_ID != "your_id":
            try:
                auth_manager = SpotifyClientCredentials(
                    client_id=SPOTIFY_CLIENT_ID, 
                    client_secret=SPOTIFY_CLIENT_SECRET
                )
                self.client = spotipy.Spotify(auth_manager=auth_manager)
                print("Spotify API initialized successfully.")
            except Exception as e:
                print(f"Spotify Init Error: {e}")
        else:
            print("Running in MOCK mode. Insert Spotify credentials in .env to use real API.")

    def get_recommendations(self, mood_data: dict, limit: int = 5) -> list[Song]:
        if not self.client:
            return self._get_mock_data(mood_data['mood_name'], limit)
            
        try:
            mood = mood_data['mood_name']
            
            # Seed genres based on mood
            seed_genres = ['pop']
            if mood in ['Energetic', 'Excited']: seed_genres = ['dance', 'work-out']
            elif mood in ['Calm', 'Neutral']: seed_genres = ['acoustic', 'chill']
            elif mood in ['Sad', 'Melancholic']: seed_genres = ['sad', 'indie']
            elif mood == 'Intense': seed_genres = ['rock', 'metal']
            elif mood == 'Happy': seed_genres = ['happy', 'pop']
            
            # AI LEARNING INJECTION: Intercept genres and pivot them if user history shows dislikes
            seed_genres = db_client.get_learned_genre_preference(mood, seed_genres)
            
            # Since playlists can sometimes be private and throw 401 errors without a user login,
            # the safest modern method is to Search for Tracks directly using mood keywords!
            search_query = f"{mood} {seed_genres[0]}"
            
            # Step 1: Find tracks matching our mood. 
            # We omit `limit` argument because Spotify sometimes throws 400 Invalid Limit for custom numbers.
            search_results = self.client.search(q=search_query, type='track')
            
            if not search_results['tracks']['items']:
                return self._get_mock_data(mood_data['mood_name'], limit)
                
            # Grab a random selection of tracks from the search results up to our limit
            valid_tracks = search_results['tracks']['items']
            selected_tracks = random.sample(valid_tracks, min(limit, len(valid_tracks)))
            
            songs = []
            for track in selected_tracks:
                album_art = ""
                if track['album']['images'] and len(track['album']['images']) > 0:
                    album_art = track['album']['images'][0]['url']
                    
                songs.append(Song(
                    id=track['id'],
                    title=track['name'],
                    artist=track['artists'][0]['name'] if track['artists'] else "Unknown Artist",
                    album_art=album_art,
                    url=track['external_urls']['spotify'] if 'spotify' in track['external_urls'] else "#",
                    preview_url=track.get('preview_url'),
                    genre=seed_genres[0].capitalize()
                ))
            return songs
            
        except Exception as e:
            print(f"Spotify API Error: {e}")
            return self._get_mock_data(mood_data['mood_name'], limit)
            
    def _get_mock_data(self, mood: str, limit: int) -> list[Song]:
        """Provides mock data when API keys are not supplied."""
        mock_songs = [
            Song(id="m1", title=f"{mood} Vibes Track 1", artist="Demo Artist", album_art="https://placehold.co/300x300/1DB954/FFFFFF?text=Spotify", url="#"),
            Song(id="m2", title=f"Feeling {mood} Today", artist="The Mockers", album_art="https://placehold.co/300x300/1DB954/FFFFFF?text=Music", url="#"),
            Song(id="m3", title=f"Chill {mood} Beats", artist="LoFi Generator", album_art="https://placehold.co/300x300/191414/FFFFFF?text=Vibes", url="#"),
            Song(id="m4", title=f"Ultimate {mood} Mix", artist="DJ System", album_art="https://placehold.co/300x300/535353/FFFFFF?text=Mix", url="#"),
            Song(id="m5", title=f"{mood} State of Mind", artist="AI Composer", album_art="https://placehold.co/300x300/B3B3B3/FFFFFF?text=Track", url="#")
        ]
        return random.sample(mock_songs, min(limit, len(mock_songs)))

spotify_client = SpotifyRecommender()
