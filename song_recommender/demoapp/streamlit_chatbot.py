import streamlit as st
import google.generativeai as genai
import time

# Configure GenerativeAI
genai.configure(api_key='AIzaSyCLz47HJ1Ww_wue3nnYRKDdyXmksSpmZVo')
model = genai.GenerativeModel('gemini-pro')

# Page Title and Background Color
st.title('ECHO')

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Echo animation
st.write("Hi, I'm echo. How are you doing?")
time.sleep(1)
st.write("...")
time.sleep(1)
st.write("...")
time.sleep(1)
st.write("Good to have you here!")

def main():
    # Widgets for adding songs
    songs_list = st.sidebar.text_area('Enter songs (one per line):', '')
    songs_list = [song.strip() for song in songs_list.split('\n') if song.strip()]
    st.sidebar.subheader('Songs List:')
    st.sidebar.write(songs_list)

    # Widget for adding new song
    song_to_add = st.sidebar.text_input('Add a new song:', '')

    if song_to_add:
        songs_list.append(song_to_add)
        st.sidebar.success(f'"{song_to_add}" added to the list')

    # Widget for user input
    user_input = st.text_input('You:', '')

    # Widget for sending user message
    send_button = st.button('Send')

    # Widget for clearing conversation
    clear_button = st.button('Clear Conversation')

    # Chatbot response
    if send_button:
        if user_input:
            st.session_state.messages.append(f'You: {user_input}')
            st.success(f'You: {user_input}')

            # Handle common user queries
            if "recommend songs" in user_input.lower():
                recommended_songs = model.generate_content("Generate song recommendations based on user preferences.").text
                st.session_state.messages.append(f'Chatbot: {recommended_songs}')
                st.warning(f'Chatbot: {recommended_songs}')
            else:
                # Generate Chatbot Response
                response_text = f"your response:greet the user with the response of your own !!if the user doesnt ask you to recommend songs recommend with the songs of your own , if the user gives a {songs_list}, recommend few songs from the songs list and recommend few songs by your own, analyse the {user_input},strcitly reply only on the basis of {user_input} and {songs_list} ,if user is feeling sad suggest sad songs, if the user is feeling happy recommend energetic songs, if the user is feeling romantic recommend romantic songs. Response text: . Song recommendation:I would recommend: song stricly from the {songs_list} and some songs not from the {songs_list}"
                response = model.generate_content(response_text).text

                # Display Chatbot Response
                st.session_state.messages.append(f'Chatbot: {response}')
                st.warning(f'Chatbot: {response}')

        else:
            st.warning('Please enter a message before sending.')

    # Clear conversation logic
    if clear_button:
        st.session_state.messages = []

if __name__ == "__main__":
    main()
