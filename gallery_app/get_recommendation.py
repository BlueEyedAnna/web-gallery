import pandas as pd
import numpy as np
import seaborn as sns
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


# import warnings
# warnings.simplefilter(action='ignore', category=FutureWarning)


class Similar:
    def __init__(self, arts, ratings):
        self.arts = arts
        self.ratings = ratings

    def _create_matrix(self, df):
        N = len(df['userId'].unique())
        M = len(df['artId'].unique())

        # id -> индекс
        user_mapper = dict(zip(np.unique(df["userId"]), list(range(N))))
        art_mapper = dict(zip(np.unique(df["artId"]), list(range(M))))

        # индекс -> ID
        user_inv_mapper = dict(zip(list(range(N)), np.unique(df["userId"])))
        art_inv_mapper = dict(zip(list(range(M)), np.unique(df["artId"])))

        user_index = [user_mapper[i] for i in df['userId']]
        art_index = [art_mapper[i] for i in df['artId']]

        X = csr_matrix((df["rating"], (art_index, user_index)), shape=(M, N))

        return X, user_mapper, art_mapper, user_inv_mapper, art_inv_mapper

    def _find_similar_arts(self, art_id, X, k, art_mapper, art_inv_mapper):
        neighbour_ids = []

        art_ind = art_mapper[art_id]
        art_vec = X[art_ind]
        k += 1
        kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric='cosine')
        kNN.fit(X)
        art_vec = art_vec.reshape(1, -1)
        neighbour = kNN.kneighbors(art_vec, return_distance=False)
        for i in range(0, k):
            n = neighbour.item(i)
            neighbour_ids.append(art_inv_mapper[n])
        neighbour_ids.pop(0)

        return neighbour_ids

    def get_result(self, art_id, k=10):
        user_freq = self.ratings[['userId', 'artId']].groupby('userId').count().reset_index()
        user_freq.columns = ['userId', 'n_ratings']

        art_stats = self.ratings.groupby('artId')[['rating']].agg(['count', 'mean'])
        art_stats.columns = art_stats.columns.droplevel()

        X, user_mapper, art_mapper, user_inv_mapper, art_inv_mapper = self._create_matrix(self.ratings)

        # search_word = 'Последний день Помпеи'
        # art_search = self.arts[self.arts['title'].str.contains(search_word, case=False, na=False)]
        # art_id = int(art_search.iloc[0]['artId'])

        art_titles = dict(zip(self.arts['artId'], self.arts['title']))
        # art_title = art_titles[str(art_id)]

        similar_ids = self._find_similar_arts(art_id, X, k, art_mapper, art_inv_mapper)
        # similar_arts = [art_titles[str(i)] for i in similar_ids]

        return map(int, similar_ids)
