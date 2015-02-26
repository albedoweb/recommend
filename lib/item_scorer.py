import numpy as np
from numpy.linalg import norm
from scipy.spatial.distance import cosine


class SimpleItemItemScorer:
    """
    Class implements user-user collaborative filtering
    """
    def __init__(self, r, verbose=True):
        """
        class constructor

        :param r: matrix contain all ratings. Columns represent users, rows - movies
        :param verbose: flag - print logs yes/no
        """
        self.ratings = r
        self.__verbose = verbose

    #compute mean centered ratings for each user
    def compute_mean_ratings(self):
        #for each user compute mean rating, only non zero values used
        self.mean_rating = [np.mean(filter(bool, self.ratings[:, i])) for i in range(self.ratings.shape[1])]

        #substruct mean from users movie ratings
        delta = self.ratings - self.mean_rating

        #create new matrix with  mean-centered ratings. zero values does not changed
        self.norm_ratings = np.where(self.ratings, delta, self.ratings)

    def compute_item_mean_ratings(self, movie_id):
        self.users_who_rated = [i for i, x in enumerate(list(self.ratings[movie_id, :])) if x > 0.0]
        #for each item compute mean rating, only non zero values used
        return [np.mean(filter(bool, self.ratings[i, self.users_who_rated])) for i in range(self.ratings.shape[0])]

    def compute_similarity(self, user_id, movie_id):
        #get items which user rated
        self.rated_items = [i for i, x in enumerate(list(self.ratings[:, user_id])) if x > 0.0]

        #compute cosine similarity, i use standard function from scipy library
        #if normalized vector has zero length (user rate all movies 4.0 for example) when we return 0 is this case
        self.sim = [1-cosine(self.norm_ratings[movie_id, :], self.norm_ratings[x, :])
                    if norm(self.norm_ratings[x, :]) > 0 else 0
                    for x in self.rated_items]
        self.sim = [x if x > 0 else 0 for x in self.sim]

    def get_neighbors(self, movie_id, size=20):
        """
        get top 30 neighbors of given user

        :param user_id: given user id
        :param size: size of neighborhood, default = 30
        """

        #sort similarity vector and get only top 31 result
        self.neighbors_idx = [self.rated_items[i[0]]
                              for i in sorted(enumerate(self.sim), key=lambda x:x[1], reverse=True)][0:size+1]

        #remove given user from neighbors
        #after this we have exactly top 30 neighbors
        self.neighbors_idx = self.neighbors_idx[1:size+1] if movie_id in self.rated_items \
            else self.neighbors_idx[0:size]

        #return mean centered ratings of neighbors
        return self.norm_ratings[:, self.neighbors_idx]

    def score(self, user_id, movie_id, neighborhood_size=20):
        """ predict rate from given user_id and movie_id
        :param user_id:
        :param movie_id:
        :param neighborhood_size:
        """
        #compute similarity
        self.compute_similarity(user_id, movie_id)
        #get mean centered ratings of user neighbors for given movie
        norm_ratings = self.get_neighbors(movie_id, neighborhood_size)[movie_id, :]

        #convert similarity list to numpy matrix
        m_sim = np.array(self.sim)

        #get similarity vector only for neighbors
        n_sim = m_sim[[self.rated_items.index(idx) for idx in self.neighbors_idx]]

        #given user average rating
        user_rates = self.ratings[self.neighbors_idx, user_id]

        #compute sum of similarity absolute values
        sim_abs_sum = sum([abs(x) for x in n_sim])

        #compute prediction and round in for 4 digits
        #so this is the main formula :)
        p = round(user_rates.dot(n_sim)/sim_abs_sum, 4)
        return p

    def __log(self, msg):
        if self.__verbose:
            print msg