import datetime
import time
import uuid

import pytest

import dtoolcore.utils

def test_functional():
    from dtool_cache_manager import (
        log_item_accessed,
        item_last_accessed,
        log_item_size_in_bytes,
        cache_size_in_bytes, 
        remove_cache_item,
        item_num_times_accessed,
    )

    # Create info for a dummy item in a dataset.
    dataset_uuid = str(uuid.uuid4())
    item_id = dtoolcore.utils.generate_identifier("path/to/file.txt")

    # Log that that item was accessed.
    log_item_accessed(dataset_uuid=dataset_uuid, item_id=item_id)
    log_item_size_in_bytes(dataset_uuid=dataset_uuid, item_id=item_id, size_in_bytes=13)

    # Create a timestamp to compare it to.
    time.sleep(0.1)    
    last_accessed_before = datetime.datetime.utcnow()
    time.sleep(0.1)
    
    # Find out when the item was last accessed.
    last_accessed = item_last_accessed(dataset_uuid=dataset_uuid, item_id=item_id)

    # Ensure that the item was accessed beofre the timestamp we are comparing it to.
    assert isinstance(last_accessed, datetime.datetime)
    assert last_accessed < last_accessed_before

    # Create an identifier for a second item. This has never been accessed before.
    second_item_id = dtoolcore.utils.generate_identifier("another/file.txt")
    with pytest.raises(KeyError):
        item_last_accessed(dataset_uuid=dataset_uuid, item_id=second_item_id)

    # Now we access the second item.
    log_item_accessed(dataset_uuid=dataset_uuid, item_id=second_item_id)
    log_item_size_in_bytes(dataset_uuid=dataset_uuid, item_id=second_item_id, size_in_bytes=20)
    
    # Ensure that access to the second item is more recent than the first.
    last_accessed_item2 = item_last_accessed(dataset_uuid=dataset_uuid, item_id=second_item_id)
    assert last_accessed_item2 > last_accessed

    # Check the total size of the cache.
    assert 33 == cache_size_in_bytes()

    # Delete an item from the cache.
    remove_cache_item(dataset_uuid=dataset_uuid, item_id=second_item_id)

    # Check that the size of the cache has been updated.
    assert 13 == cache_size_in_bytes()

    # Make sure that remove_cache_item raises KeyError if uuid/item_id doesn't exist.
    with pytest.raises(KeyError):
        remove_cache_item(dataset_uuid="dont_exit", item_id=second_item_id)
    with pytest.raises(KeyError):
        remove_cache_item(dataset_uuid=dataset_uuid, item_id="dont_exist")

    # Test the num_time_accessed functionality.
    item_num_times_accessed(dataset_uuid, item_id) == 1
    log_item_accessed(dataset_uuid=dataset_uuid, item_id=item_id)
    log_item_accessed(dataset_uuid=dataset_uuid, item_id=item_id)
    item_num_times_accessed(dataset_uuid, item_id) == 3