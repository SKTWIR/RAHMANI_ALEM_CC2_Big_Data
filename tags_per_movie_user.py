# -*- coding: utf-8 -*-
from mrjob.job import MRJob

class TagsPerMovieUser(MRJob):
    def mapper(self, _, line):
        try:
            parts = line.split(',')
            # On ignore l'en-tête
            if parts[0] != 'userId':
                userId = parts[0]
                movieId = parts[1]
                
                # La magie opère ici : la clé est un tuple (film, utilisateur)
                yield (movieId, userId), 1
        except Exception:
            pass

    def reducer(self, movie_user_pair, counts):
        # On fait la somme pour chaque couple unique (film, utilisateur)
        yield movie_user_pair, sum(counts)

if __name__ == '__main__':
    TagsPerMovieUser.run()