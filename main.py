import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from flask import Flask, request, render_template, jsonify
# from fuzzywuzzy import process, fuzz

app = Flask(__name__)

animes = pd.read_csv('anime_cleaned.csv', index_col=False)
similarity = pd.read_csv("matrix.csv", index_col=0)
anime_titles = animes["name"].tolist()

def input_processor(user_input):
    user_input = user_input.lower()
    user_input = re.sub('[^0-9a-zA-Z\s]+', '', user_input)

    return user_input

def get_anime_id(anime_name):
    matching_anime_df = animes[animes['name'] == anime_name]
    if matching_anime_df.empty:
        return ""
    anime_id = list(matching_anime_df['anime_id'].unique())
    return anime_id[0]

def get_recommendations(anime_id):
    n = 10
    recommendations = similarity[str(anime_id)].sort_values(ascending=False)
    top_anime_ids = recommendations.iloc[1:n+1].index.tolist()
    top_anime_names = []
    for anime_id in top_anime_ids:
        anime_name = animes.loc[animes['anime_id'] == anime_id, 'name'].values[0]
        top_anime_names.append(anime_name)
    return top_anime_names

@app.route('/anime_names')
def anime_names():
    anime_names = [title for title in anime_titles if not pd.isna(title)]
    return jsonify(anime_names=anime_names)


@app.route("/", methods=["GET", "POST"])
def index():
    # if request.method == "POST":
    #     anime_name = request.form["anime_name"].lower()
    #     if anime_name not in anime_titles:
    #         error_message = "Anime not found. Please enter a valid anime name."
    #         return render_template("index.html", error_message=error_message)
    #     # anime_id = get_anime_id(anime_name)
    #     # recommendations = get_recommendations(anime_id)
    #     # return render_template("recommendations.html", recommendations=recommendations, anime_name=anime_name)
    # else:
        return render_template("index.html")
    
@app.route("/recommendations", methods=["GET", "POST"])
def recommendations():
    if request.method == "POST":
        anime_name = request.form["anime_name"].lower()
        if anime_name not in anime_titles:
            error_message = "Anime not found. Please enter a valid anime name."
            return render_template("index.html", error_message=error_message)
        else:
            anime_id = get_anime_id(anime_name)
            recommendations = get_recommendations(anime_id)
            return render_template("rec.html", recommendations=recommendations, anime_name=anime_name.title())
    else:
        return render_template("rec.html")    

if __name__ == "__main__":
    app.run(debug=False)
