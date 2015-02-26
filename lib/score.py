import numpy as np
from scipy.spatial.distance import cosine
import operator


def get_result_by_user(test_user, rating, dense_matrix, watched):
    movie_column = zip(*rating[ test_user])[0]
    rate_vec = np.zeros((dense_matrix.shape[0], 1))

    for m in movie_column:
        rate_vec += dense_matrix[:, m]

    sim = [1-cosine(rate_vec.T, dense_matrix[:, x]) for x in range(0, 100)]

    result = dict((k, v) for k, v in enumerate(sim) if k not in watched[test_user])
    result = sorted(result.iteritems(), key=operator.itemgetter(1), reverse=True)
    return result


def get_result_by_user_weighted(test_user, rating, dense_matrix, watched):
    movie_column, rating_column = zip(*rating[ test_user])
    rate_vec = np.zeros((dense_matrix.shape[0], 1))

    print rating_column
    avg = sum(rating_column) / float(len(rating_column))
    print avg

    for k, m in enumerate(movie_column):
        rate_vec += (rating_column[k] - avg)*dense_matrix[:, m]

    sim = [1-cosine(rate_vec.T, dense_matrix[:, x]) for x in range(0, 100)]

    result = dict((k, v) for k, v in enumerate(sim) if k not in watched[test_user])
    result = sorted(result.iteritems(), key=operator.itemgetter(1), reverse=True)
    return result