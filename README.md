# MMSR_WT22_Group_D

retrieval.py 
is the main file for getting the top k songs based on one input song. Execute the file in the terminal with $python retrieval.py ,and enter the artist name, song title and number of songs to be retrieved. Output is a list of songs in the format ['artist', 'song_title']. 

creating_genre_dict.py 
creates a pickled dictionary of the genres in the format {ID: [Genres]} for the whole id_genres_mmsr.tsv file. Should be executed before executing evaluation.py. File is stored under 'genre_dictionary.pkl'

create_top_k_dict.py
Creates a pickled dictionary according to a given measure (default is an average of the cosine similarity over tf-idf, BERT and word2vec, other options are a jaccard similarity over tf-idf(not recommended due to computation time) or an average of the inner product over tf-idf, BERT and word2vec). Calculates the top 100 songs for each song in the files and stores their IDs in the format {SongID: [Top1ID, Top2ID,...]} . Retreived IDs are stored after every 1000th song. File is stored under [measure]+'_retrieved_ids.pkl'

evaluation.py
Evaluates the file created in create_top_k_dict.py and prints the average precision, MMR and nDCG at 10 and 100 songs.

Group members:
Agnes Hinterplattner, k01635183
Rahil Mujadidi, k11904249
Birgit Reiter, k12209548
Martin Seidl, k11908861
Sebastian Wolff, k12007396
