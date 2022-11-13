import numpy as np
import re
import pandas as pd
import pickle


def create_dict(id_genre_path:str):
    """
    :param id_genre_path: Path to id_genre file
    :return: Saves a pickle file with a dictionary of {ID: List of genres}
    """
    ngr_part = pd.read_csv(id_genre_path, sep='\t')
    #ngr_part = pd.read_csv('id_genres_mmsr.tsv', sep='\t')
    ngr_part['genre_list'] = ngr_part['genre']
    ngr_part = ngr_part.dropna()

    r = -1
    for u in ngr_part['genre']:
        r += 1
        x = re.sub(r"[^a-zA-Z0-9, ]", "", u)
        y = x.split(",")
        genres_list2 = []
        for i in y:
            if i[0] == " ":
                j = i[1:]
                genres_list2.append(j)
            else:
                genres_list2.append(i)
        ngr_part.at[r, 'genre_list'] = genres_list2

    ngr_part2 = ngr_part.drop(columns=['genre'])
    genre_dict = {}
    for idx, row in ngr_part2.iterrows():
        genre_dict[row['id']] = row['genre_list']
    with open('genre_dictionary.pkl', 'wb') as f:
        pickle.dump(genre_dict, f)

