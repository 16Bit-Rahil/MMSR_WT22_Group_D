import pandas as pd
import numpy as np
from sklearn.metrics import jaccard_score
from tqdm import tqdm
import pickle
import os

path  = '/media/sebastian/Seagate Backup Plus Drive/MMSR/task2/'
artist, song, k = str(input('Artist name: ')), str(input('Song title: ')), int(input('Number of returned songs: '))
# for this task we decided to compute the similarity only with the average of the cosine values of tf-idf, bert and word2vec
# as it computes the top k songs in a more reasonable time than the jaccard score and achieves better values than the
# inner product
measure = 'cosine'
features = 'best'
# measure = str(input(measure: ))
# features = str(input(features: ))
id_information = pd.read_csv(path + 'id_information_mmsr.tsv', sep='\t')
#id_genres = pd.read_csv(path + 'id_genres_mmsr.tsv', sep='\t')
#id_genres = id_genres.sort_values('id', ascending=True)
#id_bert = pd.read_csv(path + 'id_bert_pca.tsv', sep='\t')
#id_bert = id_bert.sort_values('id', ascending=True)
#id_lyrics_tfidf = pd.read_csv(path + 'id_lyrics_tfidf_pca.tsv', sep='\t')
#id_lyrics_tfidf = id_lyrics_tfidf.sort_values('id', ascending=True)
#id_lyrics_word2vec = pd.read_csv(path + 'id_lyrics_word2vec_pca.tsv', sep='\t')
#id_lyrics_word2vec = id_lyrics_word2vec.sort_values('id', ascending=True)
#id_feature = pd.read_csv(path + f'{features}.tsv', sep='\t')


def cosine_similarities(x, Y):
    nx = np.linalg.norm(x)
    nY = np.linalg.norm(Y, axis=1, keepdims=True)
    DotP = np.dot(x, Y.T).T

    return DotP / ((nx * nY) + 1e-10)

def normal(x):
    return (x-0.494)/(0.606 - 0.494)  # values are hardcoded as it is only used for one fixed method


def search(artist: str, song_query: str, k: int = 10, measure='cosine', features='basic'):
    """
    Retrieves top k similar songs based on text features.
    :param artist: Artist name as string
    :param song_query: Song title as string
    :param k: Number of Top elements, defaults to 10
    :param measure: Similarity measure, ['cosine', 'jaccard', 'inner_product'], default = cosine
    :param features: Which feature to use for calculation. Can either use the basic lyric features implementation or
                    choose one of the new features, ['basic', 'feature_name', 'best']
    :return: list of lists with artist and song of top k songs
    """

    if features == 'basic':

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
            id_bert = pd.read_csv(path + 'id_bert_pca.tsv', sep='\t')
            id_lyrics_tfidf = pd.read_csv(path + 'id_lyrics_tfidf_pca.tsv', sep='\t')
            id_lyrics_word2vec = pd.read_csv(path + 'id_lyrics_word2vec_pca.tsv', sep='\t')

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
                # for this to work do not use the downprojected tf-idf set
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
    elif features == 'best':  # computes ranking with best feature combination and late fusion, for this we first have to run it for 100
        # otherwise we get wrong results for 10
        # first we check if there is a dictionary for the measure available
        if os.path.exists(path +f'best_retrieved_ids.pkl'):
            with open(path +f'best_retrieved_ids.pkl', 'rb') as f:
                retrieved_dict = pickle.load(f)
        else:
            retrieved_dict = {}
        song_id = id_information.loc[(id_information['artist'] == artist) & (id_information['song'] == song_query)]
        query_id = song_id.iloc[0]['id']
        # check if the id is already in the dictionary
        if query_id in retrieved_dict and len(retrieved_dict[query_id]) >= k:
            top_k_ids = retrieved_dict[query_id]
            top_k_ids = top_k_ids[:k]
        else:
            file_list = []
            # for each of the three chosen features we compute the similarity and store it
            for features in ['id_resnet', 'id_bert', 'id_mfcc_bow']:
                if os.path.exists(path + f'{features}' + '_cosine_retrieved_ids.pkl'):
                    with open(path + f'{features}' + '_cosine_retrieved_ids.pkl', 'rb') as f:
                        retrieved_dict_feat = pickle.load(f)
                else:
                    retrieved_dict_feat = {}
                id_feature = pd.read_csv(path + f'{features}_pca.tsv', sep='\t')
                if query_id in retrieved_dict_feat and len(retrieved_dict_feat[query_id]) >= k:
                    top_k_ids = retrieved_dict_feat[query_id]
                    top_k_ids = top_k_ids[:k]
                else:
                    feat_query = id_feature.loc[id_feature['id'] == query_id]
                    feat_query = np.array(feat_query.drop(columns=['id']))
                    subset_ids = id_feature[['id']].copy()

                    feat_no_id = np.array(id_feature.drop(columns=['id']))

                    # next we apply our similarity measure
                    cosine = cosine_similarities(feat_query, feat_no_id)
                    subset_ids.insert(1, 'cosine', cosine)


                    # then we sort our values and get the top k
                    subset_ids = subset_ids.sort_values(measure, ascending=False)
                    sorted_measure = subset_ids.iloc[1:, :]
                    top_k = sorted_measure.head(k)
                    top_k_ids = np.array(top_k['id'])
                    retrieved_dict_feat[query_id] = list(top_k_ids)
                    with open(path +f'{features}' + '_cosine_retrieved_ids.pkl', 'wb') as f:
                        pickle.dump(retrieved_dict_feat, f)
                    file_list.append(f'{features}' + '_cosine_retrieved_ids.pkl')
            print(file_list)
            dict_dict = {}
            # we create a dictionary of the similarities
            for file in file_list:
                with open(path + file, 'rb') as f:
                    retrieved_dict = pickle.load(f)
                    dict_dict[file] = retrieved_dict
            weights = [0.606, 0.574, 0.603] # hardcoded weights for the fixed files, based on ndcg@10 value
            nor_weight = []
            #normalize the weights
            for x in weights:
                nor_weight.append(normal(x))
            borda_dict = {}
            # create a dictionary of the weighted borda count votes
            for song_idx in [query_id]:
                vote_dict = {}
                for idc, method in enumerate(file_list):  # [1:]:
                    for vote, idx in enumerate(dict_dict[method][song_idx]):
                        if idx in vote_dict:
                            vote_dict[idx] += nor_weight[idc] * (100 - vote)
                        else:
                            vote_dict[idx] = nor_weight[idc] * (100 - vote)
                borda_dict[song_idx] = vote_dict
            # create new rankings according to borda count
            for song_idx in [query_id]:
                borda_df = pd.DataFrame.from_dict(borda_dict[song_idx], orient='index', columns=['counts'])
                borda_df = borda_df.sort_values('counts', ascending=False)
                new_list = list(borda_df.index.values)[:100]
                retrieved_dict[song_idx] = new_list
            # store new ranking in pkl file
            with open(path + 'best_retrieved_ids.pkl', 'wb') as f:
                pickle.dump(retrieved_dict, f)
            # get top k ids
            top_k_ids = retrieved_dict[query_id]
            top_k_ids = top_k_ids[:k]

    else:
        # first we check if there is a dictionary for the measure available
        if os.path.exists(f'{features}' + '_' + measure + '_retrieved_ids.pkl'):
            with open(f'{features}' + '_' + measure + '_retrieved_ids.pkl', 'rb') as f:
                retrieved_dict = pickle.load(f)
        else:
            retrieved_dict = {}
        song_id = id_information.loc[(id_information['artist'] == artist) & (id_information['song'] == song_query)]
        query_id = song_id.iloc[0]['id']
        # check if the id is already in the dictionary
        if query_id in retrieved_dict and len(retrieved_dict[query_id]) >= k:
            top_k_ids = retrieved_dict[query_id]
            top_k_ids = top_k_ids[:k]
        else:
            id_feature = pd.read_csv(path + f'{features}_pca.tsv', sep='\t')
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

                elif measure == 'inner_product':
                    inner = np.dot(feat_query, feat_no_id.T).T
                    subset_ids.insert(1, 'inner_product', inner)

                # then we sort our values and get the top k
                subset_ids = subset_ids.sort_values(measure, ascending=False)
                sorted_measure = subset_ids.iloc[1:, :]
                top_k = sorted_measure.head(k)
                top_k_ids = np.array(top_k['id'])
                retrieved_dict[query_id] = list(top_k_ids)
                with open(f'{features}' + '_' + measure + '_retrieved_ids.pkl', 'wb') as f:
                    pickle.dump(retrieved_dict, f)

    # a list of lists with the artist and song of the top k songs is returned
    retr = []
    for idx in top_k_ids:
        retr.append(list(id_information.loc[(id_information['id'] == idx)][['artist', 'song']].values[0]))
    return retr


print(search(artist, song, k, measure, features))
