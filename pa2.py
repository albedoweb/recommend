# -*- coding: utf-8 -*-

"""

2766
4088
561
2760
3665

1. подготовка тегов
- подсчет всего тегов
- подсчет по каждому фильму встречаемости тегов
- подсчет редкости тегов

на выходе
- список тегов
- подсчитанные векторы по каждому фильму

2. вектор юзера
- для каждого юзера находим все фильмы, которые он оценил >= 3.5
- суммируем векторы каждого фильма

3.

"""
from gensim import corpora, models, similarities, matutils, utils
from lib.score import get_result_by_user_weighted
from lib.data_import import *

#convertToGensim()
#test_users = "4045 144 3855 1637 2919".split()
test_users = "2766 4088 561 2760 3665".split() #real users

#загружаем ид фильмов и названия
movies, movie_titles = get_movies()

#load users rating
rating, watched = get_rating_all(test_users, movies)

#загружаем теги
mm = corpora.MmCorpus('./result/corpus.mm')

#строим модель TF-IDF
tfidf = models.TfidfModel(mm)

#рассчет метрики для каждого фильма-документа
tfidf_matrix = [tfidf[ m] for m in mm]
#переводим матрицу в scipy sparse формат
tfidf_matrix = matutils.corpus2csc(tfidf_matrix)
dense_matrix = tfidf_matrix.todense()

with open('./result/test_part1.txt', 'w+') as f:
    for test_user in test_users:
        result = get_result_by_user_weighted(test_user, rating, dense_matrix, watched)

        f.write("recommendations for user %s:\n" % test_user)
        for k,v in result[0:5]:
            f.write('  %s: %.4f\n' % (movies[k], round(v, 4)))



