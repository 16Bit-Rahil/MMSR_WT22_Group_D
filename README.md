# MMSR_WT22_Group_D

__retrieval.py__ <br />
Is the main file for getting the top k songs based on one input song. Execute the file in the terminal with $python retrieval.py ,and enter the artist name, song title and number of songs to be retrieved. Output is a list of songs in the format ['artist', 'song_title']. The type of measure to use and which features to consider for recommendation can be chosen in the file. Main retrieval file.

__creating_genre_dict.py__ <br />
Creates a pickled dictionary of the genres in the format {ID: [Genres]} for the whole id_genres_mmsr.tsv file. Should be executed before executing evaluation.py. File is stored under 'genre_dictionary.pkl'

__create_top_k_dict.py__ <br />
Creates a pickled dictionary according to a given measure (default is an average of the cosine similarity over tf-idf, BERT and word2vec, other options are a jaccard similarity over tf-idf(not recommended due to computation time) or an average of the inner product over tf-idf, BERT and word2vec). Calculates the top 100 songs for each song in the files and stores their IDs in the format {SongID: [Top1ID, Top2ID,...]} . Retrieved IDs are stored after every 1000th song. File is stored under [measure]+'_retrieved_ids.pkl'. Basically same functionality as retrieval.py but it is adapted to more efficiently input all the songs as retrieval.py is more to be used using song title and artist name. <br />
A precomputed version for all songs using the different modalities can be downloaded here: [Top 100 retrievals](https://drive.google.com/drive/folders/1R-vhcWfzSW29o9DUaDRn0rByX_oqi7Uq?usp=sharing). You can find this file in the computing_dicts branch.

__evaluation.py__ <br />
Evaluates the file created in create_top_k_dict.py and prints the average precision, MMR and nDCG at 10 and 100 songs.

__PCA.ipynb__ <br />
Jupyter notebook to create the dimensionality reduction of the different datafiles using PCA.

__baseline.ipynb__ <br />
Jupyter notebook to create the baseline dictionary, where for each songs the a song with the genre rock is recommended for each k.

__genre_analysis.ipynb__ <br />
Jupyter notebook of the data analysis.

__kendall_tau_correlation.ipynb__ <br />
Jupyter notebook for computing the kendall tau correlation and creating the plots.

__precision_recall_plots.ipynb__ <br />
Jupyter notebook to efficiently compute the precision and recall for different k and creating the precision-recall plot.

__popularity.ipynb__ <br />
Jupyter notebook to compute the percent delta mean for k10 and k100.

Group members:

Agnes Hinterplattner, k01635183

Rahil Mujadidi, k11904249

Birgit Reiter, k12209548

Martin Seidl, k11908861

Sebastian Wolff, k12007396
