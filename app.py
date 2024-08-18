import streamlit as st
import pickle
import requests
import pandas as pd
import base64

# Set the page configuration to wide mode
st.set_page_config(layout="wide")

# Function to fetch the movie poster using TMDb API
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7f5a2d56924a98528681d9d7f9ea09e2&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Function to recommend movies based on the selected movie
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('Movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Function to convert local image to base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set the path to your local image

img_path = "app_background.jpg"  # Replace with your image path

# Convert the image to base64
img_base64 = get_base64(img_path)

# CSS for full-screen background
page_bg_img = f'''
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    filter: blur(80%);
}}
</style>
'''

# Inject the custom CSS into the Streamlit app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Streamlit app content
st.title('🎦 Movie Recommendation System')

# Movie selection dropdown
selected_movie_name = st.selectbox("Choose your Movie: ", movies['title'].values)

# Display recommendations when the button is clicked
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    
    # Display the first 5 recommended movies in one row
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])
    
    # Display the next 5 recommended movies in another row
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(names[i + 5])
            st.image(posters[i + 5])
