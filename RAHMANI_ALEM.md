# Compte Rendu Examen CC2 : Big Data - Hadoop
**Étudiants :** RAHMANI & ALEM

## Liens GitHub
*Tous les fichiers de résultats massifs générés par nos jobs Hadoop sont disponibles publiquement sur notre dépôt GitHub :*
 **[lien direct vers le dossier GitHub ici](https://github.com/SKTWIR/RAHMANI_ALEM_CC2_Big_Data)**

---

## 1. Avec la configuration par défaut de Hadoop

### Q1. Combien de tags chaque film possède-t-il ?
* **Script Python utilisé :** `tags_per_movie.py` (La clé est le `movieId`, la valeur est `1`).

* **Explication de la démarche :**
Pour cette question, la fonction Mapper a été conçue pour lire chaque ligne du fichier CSV et extraire l'identifiant du film (movieId situé à l'index 1). La clé émise est donc le movieId, associée à la valeur 1. La fonction Reducer se charge ensuite d'agréger ces valeurs en faisant la somme totale pour chaque film unique.

* **Commande d'exécution :**
```bash
  python tags_per_movie.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar hdfs:///user/raj_ops/examen/tags.csv -o hdfs:///user/raj_ops/examen/resultat_q1
```

### Q2. Combien de tags chaque utilisateur a-t-il ajoutés ?
* **Script Python utilisé :** `tags_per_user.py`

* **Explication de la démarche :**
La logique est identique à la question précédente, mais nous avons modifié la clé d'extraction. Le Mapper cible cette fois-ci l'identifiant de l'utilisateur (userId situé à l'index 0). Le Reducer regroupe l'ensemble des requêtes pour calculer le volume d'activité (nombre de tags) propre à chaque utilisateur.

* **Commande d'exécution :**
```bash
  python tags_per_user.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar hdfs:///user/raj_ops/examen/tags.csv -o hdfs:///user/raj_ops/examen/resultat_q2
```

### Q3. Combien de blocs le fichier occupe-t-il dans HDFS dans chacune des configurations ?
* **Commande d'exécution :**

```bash
  # 1. Vérification avec la configuration par défaut
  hdfs fsck /user/raj_ops/examen/tags.csv -files -blocks
  # Résultat : Total blocks (validated): 1 (avg. block size 38810332 B)

  # 2. Envoi du fichier en forçant la taille maximale des blocs à 64 Mo
  hdfs dfs -D dfs.blocksize=67108864 -put ml-25m/tags.csv /user/raj_ops/examen/tags_64.csv

  # 3. Vérification de la nouvelle configuration
  hdfs fsck /user/raj_ops/examen/tags_64.csv -files -blocks
  # Résultat : Total blocks (validated): 1 (avg. block size 38810332 B)
```

* **Analyse et Explication :** 

Dans les deux cas, le fichier occupe 1 seul bloc sur HDFS.
Cela s'explique logiquement par la taille totale du fichier brut tags.csv. Comme indiqué dans le diagnostic fsck, le fichier pèse environ 38,8 Mo (38810332 B). Puisque 38,8 Mo est inférieur à la taille par défaut d'HDFS (souvent 128 Mo) ET inférieur à notre limite forcée de 64 Mo, Hadoop n'a mathématiquement pas besoin de fractionner le fichier. Il tient intégralement dans un seul bloc, quelle que soit la configuration choisie ici.

### Q4. Combien de fois chaque tag a-t-il été utilisé pour taguer un film ?

* **Script Python utilisé :** `usage_per_tag.py`

* **Explication de la démarche :**
La clé identifiée par le Mapper est le texte du tag lui-même (index 2 du CSV). Afin de garantir un comptage précis et d'éviter les doublons liés à la casse (ex: traiter "Action" et "action" comme deux tags différents), nous avons appliqué la fonction .lower() en Python pour standardiser les chaînes de caractères. Le traitement a bien été orienté vers le nouveau fichier tags_64.csv.

* **Commande d'exécution :**
```bash
  python usage_per_tag.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar hdfs:///user/raj_ops/examen/tags_64.csv -o hdfs:///user/raj_ops/examen/resultat_q4
```

### Q5. Pour chaque film, combien de tags le même utilisateur a-t-il introduits ?

* **Script Python utilisé :** `tags_per_movie_user.py`

* **Explication de la démarche :**
Cette question croisée requiert l'utilisation d'une clé composite (Tuple). Notre fonction Mapper a été programmée pour extraire simultanément l'ID du film et l'ID de l'utilisateur, puis émettre la paire combinée (movieId, userId) comme clé unique. Le Reducer calcule ainsi la somme des tags pour chaque combinaison spécifique d'un utilisateur sur un film donné.

* **Commande d'exécution :**
```bash
  python tags_per_movie_user.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar hdfs:///user/raj_ops/examen/tags_64.csv -o hdfs:///user/raj_ops/examen/resultat_q5
```