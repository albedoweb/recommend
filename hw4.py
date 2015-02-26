import csv
import numpy as np
from scipy import sparse


def load_data():
    m = np.zeros(shape=(100, 25))
    movies = list()
    with open('./data/hw4.csv', 'rU') as ratings_file:
        reader = csv.reader(ratings_file, delimiter=',')
        i = 0
        for r in reader:
            i += 1
            if i == 1:
                continue
            m[i-2] = [float(rr) if rr != '' else 0.0 for rr in r[1:]]
            movies.append(r[0])

    return m, movies


m, movies = load_data()

import math

def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)

def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average([x[i] for i in range(len(x)) if x[i] > 0.0 and y[i] > 0.0])
    avg_y = average([y[i] for i in range(len(x)) if x[i] > 0.0 and y[i] > 0.0])
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = (x[idx] - avg_x) #if x[idx] > 0.0 and y[idx] == 0.0  else 1
        ydiff = (y[idx] - avg_y) #if x[idx] > 0.0 or y[idx] > 0.0  else 1
        diffprod += (xdiff * ydiff) if x[idx] > 0.0 and y[idx] > 0.0 else 0
        xdiff2 += xdiff * xdiff if x[idx] > 0.0 and y[idx] > 0.0 else 0
        ydiff2 += ydiff * ydiff if x[idx] > 0.0 and y[idx] > 0.0 else 0

    return diffprod / math.sqrt(xdiff2 * ydiff2)

corr = np.zeros(shape=(25,25))

for row in range(25):
    for col in range(25):
        corr[row,col] = pearson_def(m[:,col], m[:,row])

def get_top5users(idx, corr):
    top5users = [i[0] for i in sorted(enumerate(list(corr[:, idx])), key=lambda x:x[1], reverse=True)][1:6]
    return top5users


def get_rec_movies(user, top5users, corr, ratings):
    tc = corr[user, top5users]
    r = ratings[:, top5users]
    res = r.dot(tc)

    for i in range(res.shape[0]):
        s = sum([tc[j] for j in range(len(tc)) if r[i, j] > 0.0])
        res[i] = res[i] / s if s > 0 else 0
    return [i[0] for i in sorted(enumerate(list(res)), key=lambda x:x[1], reverse=True)][0:4],res



def get_rec_movies_w(user, top5users, corr, ratings):
    tc = corr[user, top5users]
    r = ratings[:, top5users]

    u_avg = average(filter(bool, ratings[:, user]))
    r_avg = [average(filter(bool, r[:, i])) for i in range(r.shape[1])]

    r_res = r - r_avg
    r_res = np.where(r, r_res, r)

    res = r_res.dot(tc)

    for i in range(res.shape[0]):
        s = sum([tc[j] for j in range(len(tc)) if r[i, j] > 0.0])
        res[i] = (u_avg + res[i] / s) if s > 0 else 0
    return [i[0] for i in sorted(enumerate(list(res)), key=lambda x:x[1], reverse=True)][0:4], res


for u in [4, 5]:
    print '%s:' % u

    top5users = get_top5users(u, corr)

    idx1,res1 = get_rec_movies(u, top5users, corr, m)
    idx2,res2 = get_rec_movies_w(u, top5users, corr, m)


    for i in idx1:
        print movies[i].split(':')[0], round(res1[i], 3)

    print '---'

    for i in idx2:
        print movies[i].split(':')[0], round(res2[i], 3)


    print '---'