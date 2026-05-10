import streamlit as st
import pickle
import pandas as pd
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Netflix Recommender",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

body {
    background-color: #141414;
    color: white;
}

.stApp {
    background-color: #141414;
}

/* MAIN TITLE */
.main-title {
    font-size: 65px;
    font-weight: bold;
    color: #E50914;
    text-align: center;
    text-shadow: 4px 4px 15px rgba(229, 9, 20, 0.9);
    letter-spacing: 4px;
    margin-top: 10px;
}

/* SUB TITLE */
.sub-title {
    font-size: 28px;
    color: white;
    text-align: center;
    background-color: rgba(229, 9, 20, 0.15);
    padding: 15px;
    border-radius: 15px;
    margin-top: 15px;
    margin-bottom: 35px;
    border: 2px solid #E50914;
    box-shadow: 0px 0px 20px rgba(229, 9, 20, 0.5);
}

/* SELECT TITLE */
.select-title {
    font-size: 24px;
    color: #E50914;
    font-weight: bold;
    margin-bottom: 10px;
}

/* MOVIE CARD */
.movie-card {
    background-color: #1f1f1f;
    padding: 10px;
    border-radius: 15px;
    transition: 0.3s;
    text-align: center;
    box-shadow: 0px 0px 10px rgba(255,255,255,0.1);
}

.movie-card:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 20px rgba(229, 9, 20, 0.7);
}

/* MOVIE TITLE */
.movie-title {
    font-size: 18px;
    font-weight: bold;
    color: white;
    margin-top: 10px;
}

/* BUTTON */
div.stButton > button {
    background-color: #E50914;
    color: white;
    border-radius: 10px;
    height: 3.2em;
    width: 100%;
    font-size: 20px;
    font-weight: bold;
    border: none;
}

div.stButton > button:hover {
    background-color: #b20710;
    color: white;
}

/* FOOTER */
.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------- FETCH POSTER ----------------
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=969b48b2bc370220f87edb147152cd04&language=en-US"

    data = requests.get(url).json()

    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# ---------------- RECOMMEND FUNCTION ----------------
def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(
            movies.iloc[i[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_posters

# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">🎬 NETFLIX MOVIE RECOMMENDER</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">🍿 Find movies similar to your favorite one!</div>',
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📺 Netflix Menu")

st.sidebar.markdown("""
- 🏠 Home
- 🔥 Trending
- ⭐ Top Rated
- 🎭 Genres
- 🎬 Latest Movies
""")

# ---------------- SELECT MOVIE ----------------

st.markdown(
    '<div class="select-title">🎥 Choose a Movie</div>',
    unsafe_allow_html=True
)

selected_movie_name = st.selectbox(
    "",
    movies['title'].values
)

# ---------------- RECOMMEND BUTTON ----------------

if st.button('🍿 Recommend Movies'):

    with st.spinner("Finding Best Movies For You..."):

        names, posters = recommend(selected_movie_name)

        st.write("## Recommended For You ❤️")

        col1, col2, col3, col4, col5 = st.columns(5)

        cols = [col1, col2, col3, col4, col5]

        for idx, col in enumerate(cols):

            with col:

                st.markdown('<div class="movie-card">', unsafe_allow_html=True)

                st.image(posters[idx])

                st.markdown(
                    f'<div class="movie-title">{names[idx]}</div>',
                    unsafe_allow_html=True
                )

                trailer_url = f"https://www.youtube.com/results?search_query={names[idx]} trailer"

                st.link_button("▶ Watch Trailer", trailer_url)

                st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------

st.markdown(
    '<div class="footer">Made with ❤️ using Streamlit</div>',
    unsafe_allow_html=True
)