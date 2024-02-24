from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Spotify API credentials
client_id = "006049209cc54382b143026df4894208"
client_secret = "250ebaff18904d528b322fe9cdadd5c5"

# Authenticate with Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artist_name = request.form['artist']
        song_name = request.form['song']
        recommendations = get_recommendations(artist_name, song_name)
        return render_template('recommendations.html', recommendations=recommendations)
    return render_template('index.html')
def get_recommendations(artist_name, song_name):
        # Fetch the track information from Spotify
        track_results = sp.search(q=f'artist:{artist_name} track:{song_name}', type='track', limit=1)
        if len(track_results['tracks']['items']) > 0:
            track = track_results['tracks']['items'][0]
            track_id = track['id']

        # Fetch the audio features of the track
        audio_features = sp.audio_features(track_id)[0]
        # Extract the desired features
        features = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
        track_feature_values = [audio_features[feature] for feature in features]

        # Use the extracted features to get recommendations from Spotify
        recommendations = sp.recommendations(seed_tracks=[track_id], limit=10, target_audio_features=track_feature_values)['tracks']

        # Return the song name, artist name, and album image URL for each recommendation
        result = []
        for recommendation in recommendations:
            album_id = recommendation['album']['id']
            album_info = sp.album(album_id)
            album_image = album_info['images'][0]['url']

            result.append({
                'song_name': recommendation['name'],
                'artist_name': recommendation['artists'][0]['name'],
                'album_image': album_image
            })
            return result
        else:
            return None

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)


