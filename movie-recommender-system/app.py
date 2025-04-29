import streamlit as st
import  pandas as pd
import pickle

movies_list_dict=pickle.load(open('new_df_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_list_dict)

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    y = []
    for i in movies_list:
        y.append(movies.iloc[i[0]]['title'])
    return y

st.title("Movie Recommender System")

selected_movie = st.selectbox(
    "Which movie would you like to watch??",
    movies['title'],
)
if st.button("Recommend", type="primary"):
    recommended_movies = recommend(selected_movie)
    for i in recommended_movies:
        st.write(i)
