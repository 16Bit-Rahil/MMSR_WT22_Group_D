import pandas as pd
import numpy as np
from sklearn.metrics import jaccard_score
from tqdm import tqdm
import pickle
import os

artist, song, k = str(input('Artist name: ')), str(input('Song title: ')), int(input('Number of returned songs: '))
# for this task we decided to compute the similarity only with the average of the cosine values of tf-idf, bert and word2vec
# as it computes the top k songs in a more reasonable time than the jaccard score and achieves better values than the
# inner product
measure = 'cosine'
# measure = str(input(measure: ))
id_information = pd.read_csv('id_information_mmsr.tsv', sep='\t')
#id_information = id_information.sort_values('id', ascending=True)
id_genres = pd.read_csv('id_genres_mmsr.tsv', sep='\t')
#id_genres = id_genres.sort_values('id', ascending=True)
id_bert = pd.read_csv('id_bert_mmsr.tsv', sep='\t')
#id_bert = id_bert.sort_values('id', ascending=True)
id_lyrics_tfidf = pd.read_csv('id_lyrics_tf-idf_mmsr.tsv', sep='\t')
#id_lyrics_tfidf = id_lyrics_tfidf.sort_values('id', ascending=True)
id_lyrics_word2vec = pd.read_csv('id_lyrics_word2vec_mmsr.tsv', sep='\t')
#id_lyrics_word2vec = id_lyrics_word2vec.sort_values('id', ascending=True)


def cosine_similarities(x, Y):
    nx = np.linalg.norm(x)
    nY = np.linalg.norm(Y, axis=1, keepdims=True)
    DotP = np.dot(x, Y.T).T

    return DotP / ((nx * nY) + 1e-10)


def search(artist: str, song_query: str, k: int = 10, measure='cosine'):
    """
    Retrieves top k similar songs based on text features.
    :param artist: Artist name as string
    :param song_query: Song title as string
    :param k: Number of Top elements, defaults to 10
    :param measure: Similarity measure, ['cosine', 'jaccard', 'inner_product'], default = cosine
    :return: list of lists with artist and song of top k songs
    """

    # first we check if there is a dictionary for the measure available
    if os.path.exists(measure + '_retrieved_ids.pkl'):
        with open(measure + '_retrieved_ids.pkl', 'rb') as f:
            retrieved_dict = pickle.load(f)
    else:
        retrieved_dict = {}

    # we get the id of the query song
    song_id = id_information.loc[(id_information['artist'] == artist) & (id_information['song'] == song_query)]
    query_id = song_id.iloc[0]['id']
    # check if the id is already in the dictionary
    if query_id in retrieved_dict and len(retrieved_dict[query_id]) >= k:
        top_k_ids = retrieved_dict[query_id]
        top_k_ids = top_k_ids[:k]
    else:
        # we get our sets for calcualting the measures without the id value
        tfidf_subset = id_lyrics_tfidf
        tfidf_query = id_lyrics_tfidf.loc[id_lyrics_tfidf['id'] == query_id]
        tfidf_query = np.array(tfidf_query.drop(columns=['id']))
        subset_ids = tfidf_subset[['id']].copy()

        tfidf_no_id = np.array(tfidf_subset.drop(columns=['id']))

        bert_subset = id_bert
        bert_query = id_bert.loc[id_bert['id'] == query_id]
        bert_query = np.array(bert_query.drop(columns=['id']))

        bert_no_id = np.array(bert_subset.drop(columns=['id']))
        word2vec_subset = id_lyrics_word2vec
        word2vec_query = id_lyrics_word2vec.loc[id_lyrics_word2vec['id'] == query_id]
        word2vec_query = np.array(word2vec_query.drop(columns=['id']))

        word2vec_no_id = np.array(word2vec_subset.drop(columns=['id']))

        # next we apply our similarity measure
        if measure == 'cosine':
            # for cosine we calculate the cosine similarity over tf-idf, bert and word2vec and take the average
            cosine = cosine_similarities(tfidf_query, tfidf_no_id)
            subset_ids.insert(1, 'cosine_ifidf', cosine)

            cosine = cosine_similarities(bert_query, bert_no_id)
            subset_ids.insert(1, 'cosine_bert', cosine)

            cosine = cosine_similarities(word2vec_query, word2vec_no_id)
            subset_ids.insert(1, 'cosine_word2vec', cosine)
            subset_ids_without_id = subset_ids.drop(columns=['id'])

            avg_cosin = subset_ids_without_id.mean(axis=1)
            subset_ids.insert(1, 'cosine', avg_cosin)

        elif measure == 'jaccard':
            # for the jaccard score we only calculate it over a modified tf-idf set
            tfidf_query[tfidf_query != 0.0] = 1
            tfidf_no_id[tfidf_no_id != 0.0] = 1
            scores = []
            for row in tqdm(tfidf_no_id):
                jaccard = jaccard_score(tfidf_query[0], row)
                scores.append(jaccard)
            subset_ids.insert(1, 'jaccard', scores)

        elif measure == 'inner_product':
            # for inner product we calculate the inner product over tf-idf, bert and word2vec and take the average
            inner = np.dot(tfidf_query, tfidf_no_id.T).T
            subset_ids.insert(1, 'inner_tfidf', inner)

            inner = np.dot(bert_query, bert_no_id.T).T
            subset_ids.insert(1, 'inner_bert', inner)

            inner = np.dot(word2vec_query, word2vec_no_id.T).T
            subset_ids.insert(1, 'inner_word2vec', inner)
            subset_ids_without_id = subset_ids.drop(columns=['id'])

            avg_inner = subset_ids_without_id.mean(axis=1)
            subset_ids.insert(1, 'inner_product', avg_inner)

        # then we sort our values according to the measure and get the top k songs
        subset_ids = subset_ids.sort_values(measure, ascending=False)
        sorted_measure = subset_ids.iloc[1:, :]
        top_k = sorted_measure.head(k)
        top_k_ids = np.array(top_k['id'])
        retrieved_dict[query_id] = list(top_k_ids)
        # we store the retrieved songs in a dictionary in a pickle file
        with open(measure + '_retrieved_ids.pkl', 'wb') as f:
            pickle.dump(retrieved_dict, f)
    # a list of lists with the artist and song of the top k songs is returned
    retr = []
    for idx in top_k_ids:
        retr.append(list(id_information.loc[(id_information['id'] == idx)][['artist', 'song']].values[0]))
    return retr


print(search(artist, song, k, measure))