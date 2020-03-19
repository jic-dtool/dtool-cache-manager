"""Module for managing the dtool cache."""

import datetime
from collections import defaultdict
import sqlite3

import sqlite3 as lite

#con = lite.connect('dtool_cache_sqlite3.db') # global connection
con = lite.connect(":memory:")
with con:
    cur = con.cursor()
    cur.execute('''CREATE TABLE dtcache
              ( item_id TEXT PRIMARY KEY     NOT NULL,
                dataset_uuid TEXT   NOT NULL,
                size_in_byte INT     NOT NULL,
                last_access_time  TEXT  NOT NULL );''')

print("Table created successfully")
'''
# Many  inserts many
records = [
             ('2020-02-24', 'ABC', 'XYZ', 1000, 45.00),
             ('2020-02-24', 'BUY', 'IBM', 1000, 45.00),
             ('2020-02-24', 'BUY', 'IBM', 1000, 45.00),
]
c.executemany('INSERT INTO dtcache VALUES (?,?,?,?,?)', records)

'''

# We will replace this with a rich mans database such as sqlite3, mysql, posgres
nested = lambda: defaultdict(nested) # nested dict of dicts  {{{...}}} wont raise keyError if lvalue appears

MY_AMAZING_DB = nested()


def log_item_accessed(dataset_uuid, item_id):

    MY_AMAZING_DB[dataset_uuid][item_id]["last_access_time"] = datetime.datetime.utcnow()

    # set counter here
    if not "times_item_accessed" in MY_AMAZING_DB[dataset_uuid][item_id]: # initialise its not already
       MY_AMAZING_DB[dataset_uuid][item_id]["times_item_accessed"] = 1
    else:
       MY_AMAZING_DB[dataset_uuid][item_id]["times_item_accessed"] += 1     # update the counter

def log_item_size_in_bytes(dataset_uuid, item_id, size_in_bytes):
    MY_AMAZING_DB[dataset_uuid][item_id]["size_in_bytes"] = size_in_bytes

def item_last_accessed(dataset_uuid, item_id):
    "Get time stamp for last time an item wass accessed "

    if dataset_uuid not in MY_AMAZING_DB:
       raise KeyError('Dataset doesnt exists: {}'.format(dataset_uuid))
    if item_id not in MY_AMAZING_DB[dataset_uuid]:
       raise KeyError('Items doesnt exists: {}'.format(item_id))
    if "last_access_time" not in MY_AMAZING_DB[dataset_uuid][item_id]:
       raise KeyError('No time recored for item: {} in dataset {}'.format( item_id, dataset_uuid))

    return MY_AMAZING_DB[dataset_uuid][item_id]["last_access_time"]


def cache_size_in_bytes():
    "Return the total size of the dtool cache."
    tot_size_in_bytes = 0

    for _uuid in MY_AMAZING_DB:
       for ids  in  MY_AMAZING_DB[_uuid]:
            tot_size_in_bytes += MY_AMAZING_DB[_uuid][ids]["size_in_bytes"]

    return tot_size_in_bytes

def remove_cache_item(dataset_uuid, item_id):
    "Remove cache item"
    del MY_AMAZING_DB[dataset_uuid][item_id]


def item_num_times_accessed(dataset_uuid, item_id):
    "Return the number of times this item acccesed "

    if not "times_item_accessed" in MY_AMAZING_DB[dataset_uuid][item_id]:
       raise KeyError

    return  MY_AMAZING_DB[dataset_uuid][item_id]["times_item_accessed"]

