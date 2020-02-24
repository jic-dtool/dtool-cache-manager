"""Module for managing the dtool cache."""

import datetime
from collections import defaultdict


MY_AMAZING_DB = defaultdict(dict)

def log_item_accessed(dataset_uuid, item_id):
    MY_AMAZING_DB[dataset_uuid][item_id] = defaultdict(dict)
    MY_AMAZING_DB[dataset_uuid][item_id]["last_access_time"] = datetime.datetime.utcnow()


def log_item_size_in_bytes(dataset_uuid, item_id, size_in_bytes):
    MY_AMAZING_DB[dataset_uuid][item_id]["size_in_bytest"] = size_in_bytes
    

def item_last_accessed(dataset_uuid, item_id):
    return MY_AMAZING_DB[dataset_uuid][item_id]["last_access_time"]


def cache_size_in_bytes():
    "Return the total size of the dtool cache."
    tot_size_in_bytes = 0

    for _uuid in MY_AMAZING_DB:
       for ids  in  MY_AMAZING_DB[_uuid]:
            tot_size_in_bytes += MY_AMAZING_DB[_uuid][ids]["size_in_bytest"]

    return tot_size_in_bytes

 

def remove_cache_item(dataset_uuid, item_id):
    "Remove cache item"
    del MY_AMAZING_DB[dataset_uuid][item_id]

    
