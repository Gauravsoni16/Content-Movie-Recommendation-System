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

def fetch_movie_details(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0801e204f4527cf4a78827c23aac0698&language=en-US')
    data = response.json()
    return data

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

def truncate_description(description, max_length=500):
    if len(description) > max_length:
        return description[:max_length] + "..."
    return description

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_ratings = []
    recommended_movies_descriptions = []
    recommended_movies_release_dates = []  # List to store release dates

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_title = truncate_title(movies.iloc[i[0]].title)
        recommended_movies.append(recommended_movie_title)

        movie_details = fetch_movie_details(movie_id)
        recommended_movies_ratings.append(movie_details.get('vote_average', 'N/A'))

        recommended_movie_description = movie_details.get('overview', 'No description available')
        recommended_movies_descriptions.append(recommended_movie_description)

        recommended_movie_release_date = movie_details.get('release_date', 'N/A')
        recommended_movies_release_dates.append(recommended_movie_release_date)

        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters, recommended_movies_ratings, recommended_movies_descriptions,\
        recommended_movies_release_dates



movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
def on_movie_select(movie_name):
    names, posters, ratings, descriptions, release_dates = recommend(movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"<p style='text-align: center;'><b>{names[0]}</b></p>", unsafe_allow_html=True)
        st.image(posters[0], use_column_width=True)
        st.write(f"Rating: {ratings[0]}")
        st.write(f"Release Date: {release_dates[0]}")
        with st.expander(f"Read more"):
            st.write(truncate_description(descriptions[0]))

    with col2:
        st.markdown(f"<p style='text-align: center;'><b>{names[1]}</b></p>", unsafe_allow_html=True)
        st.image(posters[1], use_column_width=True)
        st.write(f"Rating: {ratings[1]}")
        st.write(f"Release Date: {release_dates[1]}")
        with st.expander(f"Read more"):
            st.write(truncate_description(descriptions[1]))

    with col3:
        st.markdown(f"<p style='text-align: center;'><b>{names[2]}</b></p>", unsafe_allow_html=True)
        st.image(posters[2], use_column_width=True)
        st.write(f"Rating: {ratings[2]}")
        st.write(f"Release Date: {release_dates[2]}")
        with st.expander(f"Read more"):
            st.write(truncate_description(descriptions[2]))

    with col4:
        st.markdown(f"<p style='text-align: center;'><b>{names[3]}</b></p>", unsafe_allow_html=True)
        st.image(posters[3], use_column_width=True)
        st.write(f"Rating: {ratings[3]}")
        st.write(f"Release Date: {release_dates[3]}")
        with st.expander(f"Read more"):
            st.write(truncate_description(descriptions[3]))

    with col5:
        st.markdown(f"<p style='text-align: center;'><b>{names[4]}</b></p>", unsafe_allow_html=True)
        st.image(posters[4], use_column_width=True)
        st.write(f"Rating: {ratings[4]}")
        st.write(f"Release Date: {release_dates[4]}")
        with st.expander(f"Read more"):
            st.write(truncate_description(descriptions[4]))

selected_movie_name = st.selectbox(
            'Select a movie',
            movies['title'].values,
            key='movie_select')

st.write("Selected:", selected_movie_name)
on_movie_select(selected_movie_name)
