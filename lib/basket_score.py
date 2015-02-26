import numpy as np
from numpy.linalg import norm
from scipy.spatial.distance import cosine


class BasketItemScorer:
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

    def compute_similarity(self, movie_id):
        #get items which user rated
        #self.rated_items = [i for i, x in enumerate(list(self.ratings[:, user_id])) if x > 0.0]

        #compute cosine similarity, i use standard function from scipy library
        #if normalized vector has zero length (user rate all movies 4.0 for example) when we return 0 is this case

        return np.array([1-cosine(self.norm_ratings[movie_id, :], self.norm_ratings[x, :])
                    if norm(self.norm_ratings[x, :]) > 0
                        and cosine(self.norm_ratings[movie_id, :], self.norm_ratings[x, :]) <= 1 else 0
                    for x in range(self.ratings.shape[0])])

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

    def score(self, items):
        """ predict rate from given user_id and movie_id
        :param user_id:
        :param movie_id:
        :param neighborhood_size:
        """
        #compute similarity

        result = np.zeros((1, 100))
        for item in items:
            result = result + self.compute_similarity(item)
            print result.shape

        #print list(result[0])
        print sorted(enumerate(list(result[0])), key=lambda x:x[1], reverse=True)

        return sorted(enumerate(list(result[0])), key=lambda x:x[1], reverse=True)[len(items):len(items)+5]

    def __log(self, msg):
        if self.__verbose:
            print msg