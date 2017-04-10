from __future__ import print_function

import sys
from operator import add
from pyspark import SparkContext
import os
from csv import reader

#Count the total violation complaints by season from 2006 - 2016
#output: key = season, value = count


if __name__ == "__main__":
    def filter_date(x):
        try:
            x.split('/')[0]
            return True
        except Exception as e:
            return False

    def filter_violation(x):
        if 'VIOLATION' in x:
            return True
        else:
            return False

    def season(x):
        day = int(x.split('/')[1])
        month = int(x.split('/')[0])
        md = month*100 + day

        if ((md > 320) and (md < 621)):
            s = 'spring'
        elif ((md > 620) and (md < 923)):
            s = 'summer'
        elif ((md > 922) and (md < 1223)):
            s = 'fall'
        else:
            s = 'winter'
        return s


    if len(sys.argv) != 2:
        print("Usage: violation_count_by_season.py <file1> ", file=sys.stderr)
        exit(-1)
    sc = SparkContext()
    data= sc.textFile(sys.argv[1], 1)
    rdd = data.mapPartitions(lambda x: reader(x))
    mapping = rdd.map(lambda line: (line[5], line[11])).filter(lambda x: filter_date(x[0])).filter(lambda x: filter_violation(x[1]))
    mapping = mapping.map(lambda x: (season(x[0]), 1))
    joined = mapping.reduceByKey(lambda x,y: x+y).sortByKey(ascending=True).saveAsTextFile("violation_count_by_season.out")

