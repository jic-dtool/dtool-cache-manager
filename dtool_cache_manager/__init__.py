"""Module for managing the dtool cache."""

import datetime

MY_AMAZING_DB = {}

def log_item_accessed(dataset_uuid, item_id):
    MY_AMAZING_DB[dataset_uuid] = {item_id: datetime.datetime.utcnow()}

def item_last_accessed(dataset_uuid, item_id):
    return MY_AMAZING_DB[dataset_uuid][item_id]