import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

from Luma_recommender import (
    get_recommendations,
    get_movie_details,
    get_poster,
    get_backdrop
)

from Luma_ai import ask_luma


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Luma",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "wishlist": [],
    "recommendations": [],
    "recent_searches": [],
    "messages": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

movies_df = pd.read_csv("Luma_movies_dataset.csv")


# --------------------------------------------------
# BACKGROUND
# --------------------------------------------------

def set_background(url):

    st.markdown(
        f"""
        <style>

        [data-testid="stAppViewContainer"]{{
            background-image:url("{url}");
            background-size:cover;
            background-position:center;
            background-attachment:fixed;
        }}

        [data-testid="stHeader"]{{
            background:rgba(0,0,0,0);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown(
"""
<style>

/* Hide Streamlit menu */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}


/* Sidebar */

[data-testid="stSidebar"]{
background:#111111;
}


/* Text */

h1,h2,h3,h4,h5,h6,p,label{
color:white !important;
}


/* Recommendation Card */

.movie-card{

background:rgba(20,20,20,.85);

padding:18px;

border-radius:18px;

border:1px solid rgba(255,255,255,.08);

margin-bottom:15px;

transition:.3s;
}

.movie-card:hover{

transform:scale(1.02);

border:1px solid #E50914;

box-shadow:0 0 20px rgba(229,9,20,.4);

}


/* Login */

.login-box{

background:rgba(0,0,0,.75);

padding:35px;

border-radius:25px;

text-align:center;

}


/* Buttons */

.stButton>button{

background:#E50914;

color:white;

border:none;

border-radius:10px;

font-weight:bold;

}

.stButton>button:hover{

background:#ff1f2f;

}


/* Chat */

[data-testid="stChatMessage"]{

background:rgba(20,20,20,.75);

border-radius:15px;

padding:10px;

}

</style>

""",
unsafe_allow_html=True
)


# --------------------------------------------------
# TOP MENU
# --------------------------------------------------

page = option_menu(

    menu_title=None,

    options=[
        "Profile",
        "Picks",
        "Wishlist",
        "History",
        "Trending",
        "AI Assistant"
    ],

    icons=[
        "person-circle",
        "camera-reels",
        "heart-fill",
        "clock-history",
        "fire",
        "robot"
    ],

    orientation="horizontal"
)


# --------------------------------------------------
# BACKGROUND OF EACH PAGE
# --------------------------------------------------

backgrounds = {

    "Profile":
    "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba",

    "Picks":
    "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba",

    "Wishlist":
    "https://images.unsplash.com/photo-1516035069371-29a1b244cc32",

    "History":
    "https://images.unsplash.com/photo-1478720568477-152d9b164e26",

    "Trending":
    "https://images.unsplash.com/photo-1519608487953-e999c86e7455"
}


if page != "AI Assistant":

    set_background(backgrounds[page])

else:

    st.markdown(
        """
        <style>

        [data-testid="stAppViewContainer"]{

        background:#000000;

        }

        </style>
        """,
        unsafe_allow_html=True
    )
# --------------------------------------------------
# PROFILE PAGE
# --------------------------------------------------

if page == "Profile":

    st.markdown(
        """
        <div class="login-box">
            <h1>🎬 LUMA</h1>
            <h3>Discover Movies You'll Love</h3>
            <p>Your Personal Netflix-style Movie Recommender</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("👤 Username")

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    if st.button("🚀 Login"):

        if username and password:

            st.success(f"Welcome, {username}!")

            st.balloons()

        else:

            st.warning("Please enter username and password.")


    st.divider()

    st.subheader("🔥 Popular Movies")

    popular = movies_df.sort_values(
        "popularity",
        ascending=False
    ).head(8)

    cols = st.columns(4)

    for i, (_, movie) in enumerate(popular.iterrows()):

        with cols[i % 4]:

            poster = get_poster(movie["title"])

            if poster:
                st.image(
                    poster,
                    use_container_width=True
                )

            st.markdown(
                f"**{movie['title']}**"
            )

            st.caption(
                f"⭐ {movie['vote_average']}"
            )


# --------------------------------------------------
# PICKS PAGE
# --------------------------------------------------

elif page == "Picks":

    st.title("🎬 Movie Recommendation System")

    st.write(
        "Choose your favourite movie and let Luma recommend similar movies."
    )

    movie_list = sorted(
        movies_df["title"]
        .dropna()
        .unique()
    )

    selected_movie = st.selectbox(
        "Choose a Movie",
        movie_list
    )

    num = st.slider(
        "Recommendations",
        1,
        10,
        5
    )

    if st.button("🎥 Get Recommendations"):

        recommendations = get_recommendations(
            selected_movie,
            num
        )

        if recommendations:

            st.session_state.recommendations = recommendations

            if selected_movie in st.session_state.recent_searches:

                st.session_state.recent_searches.remove(
                    selected_movie
                )

            st.session_state.recent_searches.insert(
                0,
                selected_movie
            )

            st.session_state.recent_searches = (
                st.session_state.recent_searches[:10]
            )


    if st.session_state.recommendations:

        st.subheader("🍿 Recommended Movies")

        for i, movie in enumerate(st.session_state.recommendations):

            details = get_movie_details(movie)

            poster = get_poster(movie)

            col1, col2, col3 = st.columns(
                [2,5,1]
            )

            with col1:

                if poster:

                    st.image(
                        poster,
                        use_container_width=True
                    )

            with col2:

                st.markdown(
                    f"""
                    <div class="movie-card">

                    <h3>{details['title']}</h3>

                    ⭐ Rating :
                    {details['vote_average']}

                    <br><br>

                    🌍 Language :
                    {details['original_language'].upper()}

                    <br><br>

                    📅 Release :
                    {details['release_date']}

                    <br><br>

                    🔥 Popularity :
                    {round(details['popularity'],2)}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:

                if movie in st.session_state.wishlist:

                    st.button(
                        "✅",
                        key=f"saved_{movie}",
                        disabled=True
                    )

                else:

                    if st.button(
                        "❤️",
                        key=f"wish_{i}_{movie}"
                    ):

                        st.session_state.wishlist.append(
                            movie
                        )

                        st.rerun()

# --------------------------------------------------
# WISHLIST PAGE
# --------------------------------------------------

elif page == "Wishlist":

    st.title("❤️ My Wishlist")

    if not st.session_state.wishlist:

        st.info("Your wishlist is empty.")

    else:

        for movie in st.session_state.wishlist:

            details = get_movie_details(movie)
            poster = get_poster(movie)

            col1, col2, col3 = st.columns([2,5,1])

            with col1:

                if poster:
                    st.image(
                        poster,
                        use_container_width=True
                    )

            with col2:

                st.markdown(
                    f"""
                    <div class="movie-card">

                    <h3>{details['title']}</h3>

                    ⭐ Rating :
                    {details['vote_average']}

                    <br><br>

                    📅 {details['release_date']}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:

                if st.button(
                    "❌",
                    key=f"remove_{movie}"
                ):

                    st.session_state.wishlist.remove(movie)
                    st.rerun()

        st.divider()

        if st.button("🗑️ Clear Wishlist"):

            st.session_state.wishlist.clear()
            st.rerun()


# --------------------------------------------------
# HISTORY PAGE
# --------------------------------------------------

elif page == "History":

    st.title("🕒 Search History")

    if not st.session_state.recent_searches:

        st.info("No searches yet.")

    else:

        for movie in st.session_state.recent_searches:

            details = get_movie_details(movie)
            poster = get_poster(movie)

            col1, col2 = st.columns([2,5])

            with col1:

                if poster:
                    st.image(
                        poster,
                        use_container_width=True
                    )

            with col2:

                st.markdown(
                    f"""
                    <div class="movie-card">

                    <h3>{details['title']}</h3>

                    ⭐ {details['vote_average']}

                    <br><br>

                    📅 {details['release_date']}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if st.button("🗑️ Clear History"):

            st.session_state.recent_searches.clear()
            st.rerun()


# --------------------------------------------------
# TRENDING PAGE
# --------------------------------------------------

elif page == "Trending":

    st.title("🔥 Trending Movies")

    trending = movies_df.sort_values(
        "popularity",
        ascending=False
    ).head(20)

    cols = st.columns(4)

    for i, (_, movie) in enumerate(trending.iterrows()):

        with cols[i % 4]:

            poster = get_poster(movie["title"])

            if poster:

                st.image(
                    poster,
                    use_container_width=True
                )

            st.markdown(
                f"**{movie['title']}**"
            )

            st.caption(
                f"⭐ {movie['vote_average']}"
            )


# --------------------------------------------------
# AI ASSISTANT
# --------------------------------------------------

elif page == "AI Assistant":

    st.title("🤖 Luma AI")

    st.write(
        "Ask anything about movies, actors, directors, genres or TV shows."
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask Luma..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role":"user",
                "content":prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        answer = ask_luma(
            st.session_state.messages
        )

        with st.chat_message("assistant"):

            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )
# --------------------------------------------------
# TRENDING PAGE
# --------------------------------------------------

elif page == "Trending":

    st.title("🔥 Trending Movies")

    trending = (
        movies_df
        .sort_values(
            by="popularity",
            ascending=False
        )
        .head(20)
    )

    cols = st.columns(4)

    for i, (_, movie) in enumerate(trending.iterrows()):

        with cols[i % 4]:

            poster = get_poster(movie["title"])

            if poster:
                st.image(
                    poster,
                    use_container_width=True
                )

            st.markdown(
                f"### {movie['title']}"
            )

            st.write(f"⭐ {movie['vote_average']}")
            st.write(f"🔥 Popularity: {round(movie['popularity'],1)}")

            st.caption(movie["release_date"])

            if st.button(
                "❤️ Save",
                key=f"trend_{movie['title']}"
            ):

                if movie["title"] not in st.session_state.wishlist:

                    st.session_state.wishlist.append(
                        movie["title"]
                    )

                    st.success("Added to Wishlist!")
# --------------------------------------------------
# AI ASSISTANT
# --------------------------------------------------

elif page == "AI Assistant":

    st.title("🤖 Luma AI")

    st.write(
        "Ask me anything about movies, actors, directors, genres or TV shows!"
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask Luma..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        answer = ask_luma(
            st.session_state.messages
        )

        with st.chat_message("assistant"):

            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
