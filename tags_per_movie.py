# -*- coding: utf-8 -*-
from mrjob.job import MRJob

class TagsPerMovie(MRJob):
    def mapper(self, _, line):
        try:
            # Séparation par virgule (format CSV classique)
            parts = line.split(',')
            # On ignore la première ligne (l'en-tête)
            if parts[0] != 'userId':
                movieId = parts[1]
                yield movieId, 1
        except Exception:
            pass

    def reducer(self, movieId, counts):
        yield movieId, sum(counts)

if __name__ == '__main__':
    TagsPerMovie.run()