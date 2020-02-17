import datetime
import time
import uuid

import pytest

import dtoolcore.utils

def test_functional():
    from dtool_cache_manager import (
        log_item_accessed,
        item_last_accessed,
    )

    # Create info for a dummy item in a dataset.
    dataset_uuid = str(uuid.uuid4())
    item_id = dtoolcore.utils.generate_identifier("path/to/file.txt")

    # Log that that item was accessed.
    log_item_accessed(dataset_uuid=dataset_uuid, item_id=item_id)

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
    
    # Ensure that access to the second item is more recent than the first.
    last_accessed_item2 = item_last_accessed(dataset_uuid=dataset_uuid, item_id=second_item_id)
    assert last_accessed_item2 > last_accessed