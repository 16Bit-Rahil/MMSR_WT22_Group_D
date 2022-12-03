import pandas as pd
import numpy as np
from sklearn.metrics import jaccard_score
from tqdm import tqdm
import pickle
import os

# Path zu dem Path ändern wo das neue Dataset gespeichert ist, bevorzugt die pca version davon
# wichtig ist das neue id_information_mmsr.tsv file zu verwenden weil es weniger songs sind als beim alten
# bei id_essentia würde ich eher die normale file nehmen anstatt der pca file weil in der pca file nur eine spalte ist
# keine ahnung wieso
path = '/media/sebastian/Seagate Backup Plus Drive/MMSR/task2/'

id_information = pd.read_csv(path + 'id_information_mmsr.tsv', sep='\t')
# hier den namen der richtigen feature file einfügen
id_feature = pd.read_csv(path + 'id_blf_spectral_pca.tsv', sep='\t')


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
        feat_query = id_feature.loc[id_feature['id'] == query_id]
        feat_query = np.array(feat_query.drop(columns=['id']))
        subset_ids = id_feature[['id']].copy()

        feat_no_id = np.array(id_feature.drop(columns=['id']))

        # next we apply our similarity measure
        if measure == 'cosine':
            cosine = cosine_similarities(feat_query, feat_no_id)
            subset_ids.insert(1, 'cosine', cosine)

        #elif measure == 'jaccard':
        #    tfidf_query[tfidf_query != 0.0] = 1
        #    tfidf_no_id[tfidf_no_id != 0.0] = 1
        #    scores = []
        #    for row in tqdm(tfidf_no_id):
        #        jaccard = jaccard_score(tfidf_query[0], row)
        #        scores.append(jaccard)
        #    subset_ids.insert(1, 'jaccard', scores)

        elif measure == 'inner_product':
            inner = np.dot(feat_query, feat_no_id.T).T
            subset_ids.insert(1, 'inner_product', inner)

        # then we sort our values and get the top k
        subset_ids = subset_ids.sort_values(measure, ascending=False)
        sorted_measure = subset_ids.iloc[1:, :]
        top_k = sorted_measure.head(k)
        top_k_ids = np.array(top_k['id'])
        #retrieved_dict[query_id] = list(top_k_ids)
        #with open(measure + '_retrieved_ids.pkl', 'wb') as f:
        #    pickle.dump(retrieved_dict, f)
    return list(top_k_ids)


measures = ['cosine', 'inner_product']
top_k_dict = {}
i = 0
for measure in measures:
    for song_id in tqdm(id_information.head(1000)['id']):
        top_k = search_with_id(song_id, measure=measure)
        top_k_dict[song_id] = top_k
        i += 1
        if i % 1000 == 0:
            with open(path + measure + '_retrieved_ids.pkl', 'wb') as f:
                pickle.dump(top_k_dict, f)
    with open(path + measure + '_retrieved_ids.pkl', 'wb') as f:
        pickle.dump(top_k_dict, f)



