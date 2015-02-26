from lib.datasource import *
from lib.scorer import SimpleUserUserItemScorer


def get_movies():
    with open('./data/movie-titles.csv', 'rU') as mfile:
        movie_title = dict()
        reader = csv.reader(mfile, delimiter=',')
        for id, title in reader:
            movie_title[id] = title
    return movie_title

fileName = './data/ratings.csv'
ds = DataSource(True)
ds.load(fileName)

m = ds.get_matrix()

pa3fileName = './data/pa3_sample.txt'
scorer = SimpleUserUserItemScorer(m)
scorer.compute_mean_ratings()

#user_id = 1024
#movie_id = 36955
#print user_id, movie_id, scorer.score(ds.new_user_idx(user_id), ds.new_item_idx(movie_id), ds)
#print 'Right rating: ', 3.9698 , 2.3524

titles = get_movies()

with open(pa3fileName, 'rbU') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=':')
    for user_id, movie_id in csv_reader:
        user_id = int(user_id)
        movie_id = int(movie_id)
        print '%d,%d,%.4f,%s' % (user_id, movie_id,
                                 scorer.score(ds.new_user_idx(user_id), ds.new_item_idx(movie_id)),
                                 titles[str(movie_id)][:-1])
