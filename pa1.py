import csv
import time
import mmap

#4327
#280
#194


def fastFileOpen():
    start = time.time()
    users = set()
    all_movies = dict()
    movies = set()
    movie_count = dict()

    with open("recsys-data-ratings.csv", "r+b") as f:
        # memory-mapInput the file, size 0 means whole file
        mapInput = mmap.mmap(f.fileno(), 0)
        # read content via standard file methods
        for s in iter(mapInput.readline, ""):
            user, movie, rate = s.split(',')
            if user not in users:
                users.add(user)
                all_movies[user] = set()
            all_movies[user].add(movie)
            if movie not in movies:
                movies.add(movie)
                movie_count[movie] = 1
            else:
                movie_count[movie] += 1

        mapInput.close()
        end = time.time()
        print "Time for completion", end - start
        return all_movies, users, movies, movie_count


def readFile():
    with open('recsys-data-ratings.csv', 'rU') as csvfile:
        r = csv.reader(csvfile, delimiter=',')
        all_movies = dict()
        for user, movie, rate in r:
            if user not in all_movies.keys():
                all_movies[user] = list()
            all_movies[user].append(movie)
    return all_movies


def writeFile(filename, data_list):
    with open(filename, 'w') as my_file:
        for item in data_list:
            my_file.write("%s" % item)
            for k, v in data_list[item]:
                my_file.write(",%s,%.2f" % (k, v))
            my_file.write("\n")


my_movies = set(['194', '280', '4327'])
all_movies, users, movies, movie_count = fastFileOpen()

result = {'194': {}, '280': {}, '4327': {}}

for movie in movies:
    if movie in my_movies:
        continue
    for user in users:
        for my in my_movies:
            if movie in all_movies[user] and my in all_movies[user]:
                if movie not in result[my]:
                    result[my][movie] = 1
                else:
                    result[my][movie] += 1

for my in result:
    for movie in result[my]:
        result[my][movie] = result[my][movie] / float(movie_count[my])

for my in result:
    result[my] = sorted(result[my].items(), key=lambda x: x[1], reverse=True)[0:5]

print result

writeFile('simple.txt', result)
exit()


adv_formula = {'194': {}, '280': {}, '4327': {}}
movie_count = {'194': 0, '280': 0, '4327': 0}

for movie in movies:
    for user in users:
        if movie in my_movies:
            if movie not in all_movies[user]:
                movie_count[movie] += 1
        else:
            for my in my_movies:
                if movie in all_movies[user] and my not in all_movies[user]:
                    if movie not in adv_formula[my]:
                        adv_formula[my][movie] = 1
                    else:
                        adv_formula[my][movie] += 1

for my in adv_formula:
    for movie in adv_formula[my]:
        adv_formula[my][movie] = result[my][movie] / (adv_formula[my][movie] / float(movie_count[my]))

for my in adv_formula:
    adv_formula[my] = sorted(adv_formula[my].items(), key=lambda x: x[1], reverse=True)[0:5]
    #sorted(result[my], reverse=True, key=result[my].get)[0:5]

print adv_formula

writeFile('adv.txt', adv_formula)