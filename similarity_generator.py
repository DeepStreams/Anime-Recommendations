import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import numpy as np
import re
from fuzzywuzzy import fuzz, process
from flask import Flask, request


animes = pd.read_csv("anime.csv")
ratings = pd.read_csv("rating.csv")
anime_titles = animes["name"].tolist()
merged_data = pd.merge(animes, ratings, on='anime_id')
merged_data = merged_data.drop(columns=['rating_x', 'genre', 'type', 'episodes', 'members'])
merged_data = merged_data.dropna()
merged_data = merged_data[merged_data.rating_y != -1]
user_ratings = merged_data.pivot_table(index=['user_id'], columns=['anime_id'], values='rating_y')
user_ratings = user_ratings.dropna(thresh=50, axis=1).fillna(0)




item_similarity = cosine_similarity(user_ratings.T)
item_similarity_df = pd.DataFrame(item_similarity, index=user_ratings.columns, columns=user_ratings.columns)
print("starting")
item_similarity_df.to_csv('matrix.csv')
print("finished")
quit()
# similar = item_similarity_df[5114]
# similar = similar.sort_values(ascending=False)
# print(similar)


# anime_df["name"] = anime_df["name"].apply(lambda x: re.sub('[^0-9a-zA-Z\s]+', '', x.lower()))
# anime_df["name"] = anime_df["name"].apply(lambda x: re.sub(r'\s+', ' ', x.strip()))
# anime_cleaned = anime_df[["name", "anime_id"]]
# anime_cleaned.to_csv("anime_cleaned.csv", index=False)


# def input_processor(user_input):
#     user_input = user_input.lower()
#     user_input = re.sub('[^0-9a-zA-Z\s]+', '', user_input)

#     return user_input

# def get_anime_ids(anime_name):
#     animes['name'] = animes['name'].str.strip()
#     animes['name'] = animes['name'].str.lower()
#     animes['name'] = animes['name'].apply(lambda x: re.sub('[^0-9a-zA-Z\s]+', '', x))
#     matching_anime_df = animes[animes['name'].str.contains(anime_name)]
#     anime_names = list(matching_anime_df['name'].unique())
#     return anime_names