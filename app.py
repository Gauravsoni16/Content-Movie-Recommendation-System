import streamlit as st
import pickle
import pandas as pd
import requests
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('image.png')

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=0801e204f4527cf4a78827c23aac0698&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def truncate_title(title, max_length=13):
    if len(title) > max_length:
        return title[:max_length] + "..."
    return title

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_title = truncate_title(movies.iloc[i[0]].title)  # Truncate the title if needed
        recommended_movies.append(recommended_movie_title)

        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

def on_movie_select(movie_name):
    names, posters = recommend(movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"<p style='text-align: center;'><b>{names[0]}</b></p>", unsafe_allow_html=True)
        st.image(posters[0], use_column_width=True)
    with col2:
        st.markdown(f"<p style='text-align: center;'><b>{names[1]}</b></p>", unsafe_allow_html=True)
        st.image(posters[1], use_column_width=True)
    with col3:
        st.markdown(f"<p style='text-align: center;'><b>{names[2]}</b></p>", unsafe_allow_html=True)
        st.image(posters[2], use_column_width=True)
    with col4:
        st.markdown(f"<p style='text-align: center;'><b>{names[3]}</b></p>", unsafe_allow_html=True)
        st.image(posters[3], use_column_width=True)
    with col5:
        st.markdown(f"<p style='text-align: center;'><b>{names[4]}</b></p>", unsafe_allow_html=True)
        st.image(posters[4], use_column_width=True)

selected_movie_name = st.selectbox(
            'Select a movie',
            movies['title'].values,
            key='movie_select')

st.write("Selected:", selected_movie_name)
on_movie_select(selected_movie_name)
