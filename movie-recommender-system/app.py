import streamlit as st
import pandas as pd
import pickle
import requests
import warnings

warnings.filterwarnings('ignore')
# Load data
movies_list_dict = pickle.load(open('new_df_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_list_dict)

# TMDb API Key (replace with your key)
TMDB_API_KEY = "8cbef398f8b4c40cb123d1b0acb4b895"

# Fetch movie poster from TMDb
def fetch_poster(movie_name):
    search_url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': movie_name
    }
    response = requests.get(search_url, params=params)
    data = response.json()

    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Poster"

# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommendations = []
    for i in movies_list:
        title = movies.iloc[i[0]]['title']
        poster_url = fetch_poster(title)
        recommendations.append((title, poster_url))
    return recommendations

# Streamlit UI
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Which movie would you like to get recommentions for?",
    movies['title'],
)

if st.button("Recommend", type="primary"):
    recommendations = recommend(selected_movie)
    cols = st.columns(5)
    for i, (title, poster_url) in enumerate(recommendations):
        with cols[i]:
            st.image(poster_url, use_container_width=True)
            st.caption(title)
