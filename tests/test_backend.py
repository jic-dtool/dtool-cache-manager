"""Test the backend that will deal with persistence."""
import os
import uuid

from . import tmp_dir_fixture  # NOQA


def test_import():
    from dtool_cache_manager.backend import (
        BackendManager
    )


def test_functional(tmp_dir_fixture):  # NOQA
    from dtool_cache_manager.backend import BackendManager
    bm = BackendManager(":memory:")
    

    # Create info for a dummy item in a dataset.
    dataset_uuid = str(uuid.uuid4())
    full_item_uri = "path/to/file.txt"
    item_id = dtoolcore.utils.generate_identifier("path/to/file.txt")
    size = 13

    bm.add_new_entry(dataset_uuid=dataset_uuid, item_id=item_id, size_in_bytes=size)

    assert bm.total_size_in_bytes() == 13
    assert bm.total_number_of_entires() == 1

    bm.delete_entry(dataset_uuid=dataset_uuid, item_id=item_id)

    
    assert bm.total_size_in_bytes() == 0
    assert bm.total_number_of_entires() == 0