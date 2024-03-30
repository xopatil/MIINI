import streamlit as st
import google.generativeai as genai
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configure GenerativeAI
genai.configure(api_key='GEN AI KEY')
model = genai.GenerativeModel('gemini-pro')

# Spotify API Credentials
SPOTIFY_CLIENT_ID = 'YOUR CLIENT ID'
SPOTIFY_CLIENT_SECRET = 'YOUR CLIENT SECRET'

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

# Page Title and Background Color
st.title('ECHO')
st.write("Hi, I'm echo.")
time.sleep(1)
st.write("...")
time.sleep(1)
st.write("Good to have you here!")

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'playlist' not in st.session_state:
    st.session_state.playlist = []

# Function to fetch songs based on artist and mood
def fetch_artist_and_mood_songs(artist_name, mood, limit=10):
    if not artist_name:
        return []

    if mood.lower() == 'happy':
        query = f'happy {artist_name} songs playlist'
    elif mood.lower() == 'sad':
        query = f'sad {artist_name} songs playlist'
    elif mood.lower() == 'romantic':
        query = f'romantic {artist_name} songs playlist'
    elif mood.lower() == 'nostalgia':
        query = f'nostalgia {artist_name} songs playlist'
    elif mood.lower() == 'angry':
        query = f'angry {artist_name} songs playlist'
    elif mood.lower() == 'thrill':
        query = f'thrill {artist_name} songs playlist'
    elif mood.lower() == 'excited':
        query = f'excited {artist_name} songs playlist'
    else:
        return []

    results = sp.search(q=query, type='playlist', limit=5)
    if results['playlists']['items']:
        playlist_id = results['playlists']['items'][0]['id']
        playlist_tracks = sp.playlist_tracks(playlist_id, limit=limit)
        return [{'name': track['track']['name'], 'uri': track['track']['uri'], 'image_url': track['track']['album']['images'][0]['url']} for track in playlist_tracks['items']]
    else:
        return []

# Function to fetch Spotify URI of a song
def get_song_uri(song_name):
    result = sp.search(q='track:' + song_name, type='track', limit=1)
    if result['tracks']['items']:
        return result['tracks']['items'][0]['uri']
    else:
        return None

# Function to update song recommendations based on artist and mood
def update_song_recommendations(artist_name, mood):
    if artist_name and mood:
        artist_and_mood_songs = fetch_artist_and_mood_songs(artist_name, mood, limit=10)
        if artist_and_mood_songs:
            st.subheader(f'Songs by {artist_name} for {mood} mood:')
            images = [song['image_url'] for song in artist_and_mood_songs if 'image_url' in song]
            st.image(images, caption=[song['name'] for song in artist_and_mood_songs], width=100, use_column_width=False)
        else:
            st.warning(f'No songs found for {artist_name} and {mood} mood.')

def main():
    # Widget for user input
    user_input = st.text_input('You:', '')

    # Widget for sending user message
    send_button = st.button('Send', key='send_button')

    # Widget for clearing conversation
    clear_button = st.button('Clear Conversation', key='clear_button')

    # Chatbot response
    if send_button:
        if user_input:
            st.session_state.messages.append(f'You: {user_input}')
            user_input = ''  # Clear the text input field
            resp1 = model.generate_content(f"You are a powerful user emotional assistant. Your plan is to help the user, and understand their state of mind. Try to gain insights into the user's current mood, their artist of choice right now and other such information which might influence their musical choice right now. DO NOT RECOMMEND ANY SONGS TO THE USER ONLY TRY TO GAIN INFORMATION. The previous messages are {st.session_state.messages}. Respond to their last message: {user_input}").text
            st.session_state.messages.append(f'Chatbot: {resp1}')
            
            resp2 = model.generate_content(f"Based on the user's mood and artist choice, generate a search query which should be the best fit for the user. Generate a query tailor made for the user, to uplift their mood or help to focus etc based on the choice. The query should be as short as possible The previous messages are {st.session_state.messages}.").text
            st.sidebar.error(resp2)
            res = sp.search(q=resp2, type='track', limit=5)
            for i, track in enumerate(res['tracks']['items']):
                st.session_state.playlist.append({"text": f"{track['name']} - {track['artists'][0]['name']}", "image_url": track['album']['images'][0]['url'], "link": track['external_urls']['spotify']})

    # Clear conversation logic
    if clear_button:
        st.session_state.messages = []
        st.session_state.playlist = []

    # Display chat messages
    for message in st.session_state.messages:
        if message.startswith('You:'):
            st.success(message)
        elif message.startswith('Chatbot:'):
            st.warning(message)

    # Display playlist
    

    # Display recommended playlist
    st.sidebar.write('Recommended Songs:')
    for song in st.session_state.playlist:
        if 'image_url' in song:
            st.sidebar.image(song['image_url'], caption=song['text'], width=100, use_column_width=False,)
            st.sidebar.success(f" [{song['text']}]({song['link']})")

if __name__ == "__main__":
    main()
