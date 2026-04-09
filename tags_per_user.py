# -*- coding: utf-8 -*-
from mrjob.job import MRJob

class TagsPerUser(MRJob):
    def mapper(self, _, line):
        try:
            # Séparation par virgule (format CSV)
            parts = line.split(',')
            # On ignore la première ligne (l'en-tête)
            if parts[0] != 'userId':
                userId = parts[0] # L'ID de l'utilisateur est dans la première colonne (index 0)
                yield userId, 1
        except Exception:
            pass

    def reducer(self, userId, counts):
        # On fait la somme de tous les 1 pour chaque utilisateur
        yield userId, sum(counts)

if __name__ == '__main__':
    TagsPerUser.run()