import pandas as pd
import numpy as np
from sklearn.metrics import jaccard_score
from tqdm import tqdm
import pickle
import os

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


def search_with_id(song_id: str, k: int = 100, measure='cosine'):
    """
    Retrieves top k similar songs based on text features.
    :param song_id: Song ID as string
    :param k: Number of Top elements, defaults to 10
    :param measure: Similarity measure, ['cosine', 'jaccard', 'inner_product'], default = cosine
    :return: list of top k song IDs
    """
    #if os.path.exists(measure + '_retrieved_ids.pkl'):
    #    with open(measure + '_retrieved_ids.pkl', 'rb') as f:
    #        retrieved_dict = pickle.load(f)
    #else:
    #    retrieved_dict = {}
    retrieved_dict = {}

    # first we get the id of the query song
    # song = id_information.loc[(id_information['artist']==artist)&(id_information['song']==song_query)]
    query_id = song_id
    if query_id in retrieved_dict and len(retrieved_dict[query_id]) >= k:
        top_k_ids = retrieved_dict[query_id]
        top_k_ids = top_k_ids[:k]
    else:
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
            tfidf_query[tfidf_query != 0.0] = 1
            tfidf_no_id[tfidf_no_id != 0.0] = 1
            scores = []
            for row in tqdm(tfidf_no_id):
                jaccard = jaccard_score(tfidf_query[0], row)
                scores.append(jaccard)
            subset_ids.insert(1, 'jaccard', scores)

        elif measure == 'inner_product':
            inner = np.dot(tfidf_query, tfidf_no_id.T).T
            subset_ids.insert(1, 'inner_tfidf', inner)

            inner = np.dot(bert_query, bert_no_id.T).T
            subset_ids.insert(1, 'inner_bert', inner)

            inner = np.dot(word2vec_query, word2vec_no_id.T).T
            subset_ids.insert(1, 'inner_word2vec', inner)
            subset_ids_without_id = subset_ids.drop(columns=['id'])

            avg_inner = subset_ids_without_id.mean(axis=1)
            subset_ids.insert(1, 'inner_product', avg_inner)

        # then we sort our values and get the top k
        subset_ids = subset_ids.sort_values(measure, ascending=False)
        sorted_measure = subset_ids.iloc[1:, :]
        top_k = sorted_measure.head(k)
        top_k_ids = np.array(top_k['id'])
        #retrieved_dict[query_id] = list(top_k_ids)
        #with open(measure + '_retrieved_ids.pkl', 'wb') as f:
        #    pickle.dump(retrieved_dict, f)
    return list(top_k_ids)


measure = 'cosine'
top_k_dict = {}
i = 0
for song_id in tqdm(id_information['id']):  #.head(10000)['id']):
    top_k = search_with_id(song_id, measure=measure)
    top_k_dict[song_id] = top_k
    i += 1
    if i % 1000 == 0:
        with open(measure + '_retrieved_ids.pkl', 'wb') as f:
            pickle.dump(top_k_dict, f)
with open(measure + '_retrieved_ids.pkl', 'wb') as f:
    pickle.dump(top_k_dict, f)



