# Versión 2: distribuido con coreSpark

from pyspark import SparkConf, SparkContext
import sys
import csv # Necessary to handle commas inside actor / director names.

input_file = sys.argv[1]

conf = SparkConf().setAppName("actorDirector")
sc = SparkContext(conf=conf)

#header: tconst,actor,actorName,director,directorName,averageRating,numVotes

infoActor = sc.textFile(input_file)

header = infoActor.first()

bestPairs=infoActor.filter(lambda row: row != header
).map(lambda row: next(csv.reader([row]))
).map(lambda row: (
    (row[1], row[3]),               # actor, director
    (
        row[2],                     # actorName
        row[4],                     # directorName
        1,
        rating := float(row[5]),    # averageRating
        rating,
        rating
    )
)).reduceByKey(lambda a, b: (
    a[0],               # actorName
    a[1],               # directorName
    a[2] + b[2],        # count
    a[3] + b[3],        # sum of ratigs
    min(a[4], b[4]),    # min rating
    max(a[5], b[5])     # max rating
)).map(lambda a: (
    a[1][0],            # actorName
    a[1][1],            # directorName
    a[1][2],            # count
    a[1][3] / a[1][2],  # average rating
    a[1][4],            # min rating
    a[1][5]             # max rating
)).takeOrdered(20, key=lambda a: -a[2]) # type: ignore

print(bestPairs)