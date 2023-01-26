import numpy as np
import pandas as pd
import os
import pickle


def precision(song_id: str, k: int, retrieved_dict: dict, genre_dict: dict):
    top_k_ids = retrieved_dict[song_id][:k]
    query_genre = genre_dict[song_id]
    # print(query_genre)
    tp = 0
    for idx in top_k_ids:
        genres = genre_dict[idx]
        # print(genres)
        if any(item in query_genre for item in genres):
            tp += 1
        # print(tp)
    prec = tp / len(top_k_ids)
    return prec


def reciprocal_rank(song_id: str, k: int, retrieved_dict: dict, genre_dict: dict):
    top_k_ids = retrieved_dict[song_id][:k]
    query_genre = genre_dict[song_id]
    k_u = 0
    for idx, s_id in enumerate(top_k_ids):
        genres = genre_dict[s_id]
        # print(genres)
        if any(item in query_genre for item in genres):
            k_u = idx + 1
            break
    if k_u == 0:
        rr = 0
    else:
        rr = 1 / k_u
    return rr


def dcg(song_id:str, k:int, retrieved_dict:dict, genre_dict:dict):
    top_k_ids = retrieved_dict[song_id][:k]
    query_genre = genre_dict[song_id]
    dcg_k = 0
    rel_count = 0
    for idx, s_id in enumerate(top_k_ids):
        genres = genre_dict[s_id]
        #print(genres)
        if any(item in query_genre for item in genres):
            rel = 1
            rel_count += 1
        else:
            rel = 0
        if idx == 0:
            dcg_k += rel
        else:
            dcg_k += (rel/np.log2(idx+1))
    return dcg_k, rel_count

def idcg(k, rel_count):
    idcg_k = 0
    for i in range(k):
        if i < rel_count:
            if i == 0:
                idcg_k += 1
            else:
                idcg_k += 1/np.log2(i+1)
        else:
            idcg_k += 0
    return idcg_k

def ndcg(song_id:str, k:int, retrieved_dict:dict, genre_dict:dict):
    dcg_at_k, rel_c = dcg(song_id, k, retrieved_dict, genre_dict)
    if rel_c == 0:
        ndcg_k = 0
    else:
        idcg_at_k = idcg(k, rel_c)
        ndcg_k = dcg_at_k/idcg_at_k
    return ndcg_k

def evaluation(retrieval_path: str, k: int = 10):
    """
    Computes Precision, MRR and nDCG based on genre as relevance criterion
    :param retrieval_path: Path to the pickled file of the retrieved top ids in dict format {ID: [ID_top1, ID_top2, ...]}
    :param k: number of top k items
    :return: List of [Average Precision, MRR, Average nDCG]
    """
    with open(retrieval_path, 'rb') as f:
        retrieved_dict = pickle.load(f)
    with open('genre_dictionary.pkl', 'rb') as f:
        genre_dict = pickle.load(f)
    prec_list = []
    rr_list = []
    ndcg_list = []
    for song_id in retrieved_dict:
        prec_list.append(precision(song_id, k, retrieved_dict, genre_dict))
        rr_list.append(reciprocal_rank(song_id, k, retrieved_dict, genre_dict))
        ndcg_list.append(ndcg(song_id, k, retrieved_dict, genre_dict))
    lst = [sum(prec_list) / len(prec_list), sum(rr_list) / len(rr_list), sum(ndcg_list) / len(ndcg_list)]
    return lst


evaluation_path = input('Path of [measure]_retrieved_ids.pkl file to be evaluated: ')

for k in [10, 100]:
    evals = evaluation(evaluation_path, k)
    print(f'Precision@{k} = {evals[0]} \nMRR@{k} = {evals[1]} \nnDCG@{k} = {evals[2]}')