import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7cbeab97f96d37bab8fb9b30f25e16d&language=en-US".format(movie_id)
    try:
        data = requests.get(url, timeout=5).json()
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=No+Image"

    poster_path = data.get('poster_path')
    if not poster_path:
        return "https://via.placeholder.com/500x750?text=No+Image"
    return "https://image.tmdb.org/t/p/w500/" + poster_path

def recommend(movie_name):
    movie_ind = movies_list[movies_list['title'] == movie_name].index[0]
    dist = similarity[movie_ind]
    order = sorted(list(enumerate(dist)),
               reverse=True,
               key=lambda x: x[1])[1: 6]

    rec_movies = []
    rec_posters = []
    for i in order:
        movie_id = movies_list.iloc[i[0]].id
        rec_movies.append(movies_list.iloc[i[0]].title)
        # fetch poster from API
        rec_posters.append(fetch_poster(movie_id))

    return rec_movies, rec_posters


movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = movies_list['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'What would you like to watch?',
    movies)

if st.button('Recommend'):
    names, posters = (recommend(selected_movie_name))

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
