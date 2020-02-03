dtool cache manager specification
=================================

Overview
--------

When data is retrieved from datasets stored in object storage (iRODS, ECS, S3,
Azure) whole files are copied back to disk to a location known as the "dtool
cache". By default the dtool cache is in the user's home directory
(~/.cache/dtool). However, it is possible to customize this location using the
DTOOL_CACHE_DIRECTORY setting.

The disk usage of the dtool cache can become very large and from time to time
one will need to clean up the dtool cache to free up disk space. At the
moment this is something that the user would need to do by themselves.

The purpose of this "dtool-cache-manager" plugin is to make it easier to clean
up dtool cache directory. It allows users to quickly find out how much disk the
dtool cache is using and provides commands to clean up files that have not been
used for a set period of time. Below is a list of user stories illustrating the
intended usage of the dtool cache manager:

- As a consumer of dtool I want to find out how much space the dtool cache
  is using so that I know if I need to clean it up or not.

- As a consumer of dtool I want to be able to free up disk space from the
  dtool cache by removing any files that have not been used in the past month.

- As a data manager in a group with a shared dtool cache directory I want to be
  able to delete all the files in the dtool cache that are not actively being
  used by any other user.

- As a data manager I want to be able to view how often files in the
  dtool cache have been used so that I can work out how much time has been
  saved by keeping them in the cache

CLI usage
---------

To view the current state of the dtool cache one can use the command::

    dtool cache summary

To safely clean the entire dtool cache one can use the command::

    dtool cache clean --all 

To remove files until only 1TB is used::

    dtool cache clean --retain-size=1TB

To remove files that have been accessed less than ten times::

    dtool cache clean --exclude-frequently-accessed=10

Technical details
-----------------

In the dtoolcore the content of items are accessed using the call::

    dtoolcore.DataSet.item_content_abspath

This call includes a calls to pre- and a post-hook methods. These
can be accessed by adding the code block below to the setup.py file::

    entry_points={
        "dtool.pre_item_content_abspath": [
            "dtool_cache_manager_pre_item_content_abspath=dtool_cache_manager:pre_item_content_abspath",
        ],
        "dtool.post_item_content_abspath": [
            "dtool_cache_manager_post_item_content_abspath=dtool_cache_manager:post_item_content_abspath",
        ],
    },

The ``dtool-cache-manager`` package then needs to implement these functions::

    def pre_item_content_abspath(uri, uuid):
        increment_cache_item_lock_counter(uri, uuid)
    
    def post_item_content_abspath(uri, uuid):
        register_cache_item_access(uri, uuid)
        decrement_cache_item_lock_counter(uri, uuid)

The ``dtool-cache-manager`` will also implement a helper function for safely
removing items from the cache::

    def remove_cache_item_safely(uri, uuid):
        if cache_item_lock_counter(uri, uuid) == 0:
            _remove_cache_item(uri, uuid)

As well as helper functions for finding stats about a cache item::

    def num_times_accessed(uri, uuid):
        # Return the number of times an item has been accessed.

    def last_time_accessed(uri, uuid):
        # Return the datetime when the item was last accessed.
