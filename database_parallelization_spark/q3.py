from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
dir = '/global/scratch/paciorek/wikistats_full'
sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)
lines = sc.textFile(dir + '/' + 'dated')

from pyspark.sql import SQLContext, Row
import numpy as np
import pandas as pd
import re
from operator import add
import pyspark.sql.functions as F

# self define filter function
def remove_short_lines(line):
    vals = line.split(' ')
    if len(vals) < 6:
        return(False)
    else:
        return(True)

# self define function to creat more readable rows
def create_Row(line):
    p = line.split(' ')
    return(Row(date = int(p[0]), hour = int(p[1]), lang = p[2],  site = p[3],
               hits = int(p[4]), size = int(p[5])))

#pre-processing
rows = lines.filter(remove_short_lines).map(create_Row)
df = sqlContext.createDataFrame(rows)

# using sql in pyspark
df.registerTempTable("wikiHits")  # name of 'SQL' table is 'wikiHits'
# collect all the rows related to holiday/vacation
subset = sqlContext.sql("SELECT * FROM wikiHits WHERE (UPPER(site) LIKE '%VACATION%' OR UPPER(site) LIKE '%HOLIDAY')")

#
holiday_hits = subset[['lang','hits']].groupBy('lang').sum()
holiday_hits = holiday_hits.withColumnRenamed("sum(hits)", "hits_holiday")

whole_hits = df[['lang','hits']].groupBy('lang').sum()
whole_hits = whole_hits.withColumnRenamed("sum(hits)", "hits")

new_df = holiday_hits.join(whole_hits, on=['lang'], how='left_outer')

# retain three significant digits
result_df = new_df.withColumn("Fraction", (F.col("hits_holiday") / F.col("hits")))

result_df.registerTempTable("HolidayHits")
result = sqlContext.sql("SELECT lang, hits_holiday, Fraction as Holiday_fraction FROM HolidayHits ORDER BY Holiday_fraction desc limit 20")

result.show()

outputDir = '/global/scratch/wejie_yuan/holiday_hits_final'
result.write.format('csv').option("delimiter", "|").save(outputDir)
