# Versión 3: distribuido con sparkSQL

from pyspark import SparkContext
from pyspark.sql import SparkSession
import sys

input_file = sys.argv[1]

sc = SparkContext(appName='actorDirector')
spark=SparkSession(sc)

#header: tconst,actor,actorName,director,directorName,averageRating,numVotes
df = spark.read.load(input_file, format='csv', inferSchema='true', header='true')

df=df.repartition(32, 'actorName')

df.createOrReplaceTempView('actorDirector')
sqlDF = spark.sql('''
    SELECT
        ANY_VALUE(actorName) as actorName,
        ANY_VALUE(directorName) as directorName,
        COUNT(*) as count,
        AVG(averageRating),
        MIN(averageRating),
        MAX(averageRating)
    FROM actorDirector
    GROUP BY actor, director
    ORDER BY count DESC
    ''')
sqlDF.show(20)