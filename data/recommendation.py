from pyspark import SparkContext
import MySQLdb

# Open database connection
db = MySQLdb.connect("db","www","$3cureUS","cs4501" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

'''
cursor.execute("SHOW columns FROM webapp_recommendation")
data = cursor.fetchall()

for d in data:
    print ("TABLES : %s " % d[0])
'''

# execute SQL query using execute() method.

'''
sql = "INSERT INTO webapp_recommendation(item_id_id, recommended_items) \
       VALUES ('%d', '%s' )" % \
       (1, '2, 3')
cursor.execute(sql)
db.commit()

sql = "SELECT * FROM webapp_recommendation"
cursor.execute(sql)

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print ("Recommendation : %s " % str(data))

'''

# initially delete all from recommendation
sql = "DELETE FROM webapp_recommendation WHERE 1"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()



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

def f (xs):
    retList = []
    for x in range(0, len(xs)-1):
        pairL = [xs[x], xs[x+1]].sort()
        retList.append(tuple(pairL))
    return retList

#3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
user_click_pairs = clicks.flatMapValues(lambda xs: [(xs[x], xs[x+1]) for x in range(0, len(xs)-1)])
#user_click_pairs = clicks.flatMapValues(f)

#To Do: Find way to sort the values inside the tuple to allow double-sided

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
    item1 = int(item_pair[0])
    item2 = int(item_pair[1])

    # check for first item
    sql = "SELECT * FROM webapp_recommendation WHERE item_id_id='%d'" % (item1)
    cursor.execute(sql)

    row_count = cursor.rowcount
    #print("number of affected rows: {}".format(row_count))
    if row_count == 0:
       #No record so insert
       sql = "INSERT INTO webapp_recommendation(item_id_id, recommended_items) \
              VALUES ('%d', '%s' )" % \
             (item1, str(item2))
       cursor.execute(sql)
       db.commit()

    else:
        # There is record so update the row if the item isn't in it
        data = cursor.fetchone()
        #print("Recommendation : %s " % str(data))
        recommended_items = data[1].split(',')
        recommended_items = list(map(int, recommended_items))

        # Only update if item not already in list
        if (item2 not in recommended_items):
            recommended_items.append(item2)
            recommended_items = ', '.join(str(x) for x in recommended_items)
            sql = "UPDATE webapp_recommendation SET recommended_items = '%s' WHERE item_id_id='%d'" % (recommended_items, item1)
            cursor.execute(sql)
            db.commit()

    #Repeat for item2 once we get the double-sided to work

print ("5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)")


#6. Filter out any results where less than 3 users co-clicked the same pair of items

# disconnect from server
db.close()
sc.stop()
