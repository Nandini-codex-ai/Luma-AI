import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data():
    """
    Load movie dataset and prepare text columns.
    """

    df = pd.read_csv("Luma_movies_dataset.csv")

    # Fill missing values
    df["title"] = df["title"].fillna("")
    df["overview"] = df["overview"].fillna("")
    df["genre_ids"] = df["genre_ids"].fillna("").astype(str)

    return df


# Load dataset once
movies_df = load_data()

# --------------------------------------------------
# CREATE COMBINED FEATURES
# --------------------------------------------------

movies_df["combined_features"] = (
    movies_df["title"] + " " +
    movies_df["overview"] + " " +
    movies_df["genre_ids"]
)

# --------------------------------------------------
# TF-IDF
# --------------------------------------------------

vectorizer = TfidfVectorizer(stop_words="english")

tfidf_matrix = vectorizer.fit_transform(
    movies_df["combined_features"]
)

# --------------------------------------------------
# COSINE SIMILARITY
# --------------------------------------------------

similarity_matrix = cosine_similarity(
    tfidf_matrix,
    tfidf_matrix
)

# --------------------------------------------------
# RECOMMENDATION FUNCTION
# --------------------------------------------------

def get_recommendations(movie_title, num_recommendations=5):
    """
    Return a list of recommended movie titles.
    """

    if movie_title not in movies_df["title"].values:
        return None

    movie_index = movies_df[
        movies_df["title"] == movie_title
    ].index[0]

    similarity_scores = list(
        enumerate(similarity_matrix[movie_index])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Skip the selected movie
    similarity_scores = similarity_scores[1:]

    recommendations = []
    seen = set()

    for movie in similarity_scores:

        index = movie[0]

        title = movies_df.iloc[index]["title"]

        # Avoid duplicate movie titles
        if title not in seen:

            recommendations.append(title)
            seen.add(title)

        if len(recommendations) >= num_recommendations:
            break

    return recommendations


# --------------------------------------------------
# GET MOVIE DETAILS
# --------------------------------------------------

def get_movie_details(movie_title):
    """
    Return the complete row of a movie.
    """

    movie = movies_df[
        movies_df["title"] == movie_title
    ]

    if movie.empty:
        return None

    return movie.iloc[0]


# --------------------------------------------------
# POSTER URL
# --------------------------------------------------

POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"


def get_poster(movie_title):
    """
    Return full poster URL.
    """

    movie = get_movie_details(movie_title)

    if movie is None:
        return None

    if "poster_path" not in movie.index:
        return None

    poster_path = movie["poster_path"]

    if pd.isna(poster_path) or poster_path == "":
        return None

    return POSTER_BASE_URL + poster_path


# --------------------------------------------------
# BACKDROP URL
# --------------------------------------------------

BACKDROP_BASE_URL = "https://image.tmdb.org/t/p/original"


def get_backdrop(movie_title):
    """
    Return full backdrop URL.
    """

    movie = get_movie_details(movie_title)

    if movie is None:
        return None

    if "backdrop_path" not in movie.index:
        return None

    backdrop_path = movie["backdrop_path"]

    if pd.isna(backdrop_path) or backdrop_path == "":
        return None

    return BACKDROP_BASE_URL + backdrop_path