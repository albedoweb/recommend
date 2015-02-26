import csv
import numpy


def convertToGensim():
    movies = set()
    tags_by_movie = dict()
    with open('./data/movie-tags.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for movie, tag in reader:
            if int(movie) not in movies:
                movies.add(int(movie))
                tags_by_movie[int(movie)] = list()
            tags_by_movie[int(movie)].append(tag.replace(' ', '_'))

    movies = sorted(movies)
    with open('./result/tags.txt', 'w+') as myfile:
        myfile.write('%d\n' % len(movies))
        for k, v in enumerate(movies):
            myfile.write("%s\n" % " ".join(tags_by_movie[v]))


def get_rating_good(users, movies):
    rating = dict()
    watched = dict()
    with open('./data/ratings.csv', 'rU') as ratings_file:
        reader = csv.reader(ratings_file, delimiter=',')
        for user, movie, rate in reader:
            if user in users:
                if user not in rating.keys():
                    rating[user] = []
                    watched[user] = []
                if float(rate) >= 3.5:
                    rating[user].append((movies.index(int(movie)), float(rate)))
                watched[user].append(movies.index(int(movie)))
    return rating, watched


def get_rating_all(users, movies):
    rating = dict()
    watched = dict()
    with open('./data/ratings.csv', 'rU') as ratings_file:
        reader = csv.reader(ratings_file, delimiter=',')
        for user, movie, rate in reader:
            if user in users:
                if user not in rating.keys():
                    rating[user] = []
                    watched[user] = []
                rating[user].append((movies.index(int(movie)), float(rate)))
                watched[user].append(movies.index(int(movie)))
    return rating, watched


def get_rating_matrix():
    with open('./data/ratings.csv', 'rU') as ratings_file:
        reader = csv.reader(ratings_file, delimiter=',')
        m = [(int(r[0]), int(r[1]), float(r[2])) for r in reader]
    return m


def get_movies():
    with open('./data/movie-titles.csv', 'rU') as mfile:
        movies = set()
        movie_title = dict()
        reader = csv.reader(mfile, delimiter=',')
        for id, title in reader:
            movies.add(int(id))
            movie_title[id] = title
    return sorted(movies), movie_title