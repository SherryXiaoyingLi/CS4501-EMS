from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

# 1. Read data in as pairs of (user_id, item_id clicked on by the user)
data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file

pages = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition

output = pages.collect()
for user_id, page_id in output:
    print ("user_id %s page_id %s" % (user_id, page_id))
print ("1. Read data in as pairs of (user_id, item_id clicked on by the user)")


# 2. Group data into (user_id, list of item ids they clicked on)
clicks = pages.groupByKey().mapValues(list)

output = clicks.collect()
for user_id, item_list in output:
    print ("user_id %s list %s" % (user_id, str(item_list)))
print ("2. Group data into (user_id, list of item ids they clicked on)")


#3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
user_click_pairs = clicks.flatMapValues(lambda xs: [(xs[x], xs[x+1]) for x in range(0, len(xs)-1)])

output = user_click_pairs.collect()
for user_id, pair in output:
    print ("user_id %s pair %s" % (user_id, str(pair)))
print ("3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on")


#4. Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
item_pairs = user_click_pairs.map(lambda pair: (pair[1], pair[0]))
item_pairs_list = item_pairs.groupByKey().mapValues(list)

output = item_pairs_list.collect()
for item_pair, user_list in output:
    print ("item_pair %s user_list %s" % (str(item_pair), str(user_list)))
print ("4. Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)")


#5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
item_pair_map = item_pairs_list.flatMapValues(lambda x: x).map(lambda pair: (pair[0], 1))

'''
output = item_pair_map.collect()
for item_pair, one in output:
    print ("item_pair %s one %s" % (str(item_pair), one))
'''

count = item_pair_map.reduceByKey(lambda x,y: int(x)+int(y))

# Do the filtering here

output = count.collect()
for item_pair, count in output:
    print ("item_pair %s count %d" % (str(item_pair), count))
print ("5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)")


#6. Filter out any results where less than 3 users co-clicked the same pair of items

sc.stop()
