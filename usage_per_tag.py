# -*- coding: utf-8 -*-
from mrjob.job import MRJob

class UsagePerTag(MRJob):
    def mapper(self, _, line):
        try:
            parts = line.split(',')
            # On ignore la première ligne (l'en-tête)
            if parts[0] != 'userId':
                # Le tag est dans la 3ème colonne (index 2)
                tag = parts[2].lower().strip() 
                if tag: # On vérifie que le tag n'est pas vide
                    yield tag, 1
        except Exception:
            pass

    def reducer(self, tag, counts):
        yield tag, sum(counts)

if __name__ == '__main__':
    UsagePerTag.run()