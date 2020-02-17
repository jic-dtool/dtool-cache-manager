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
used for a set period of time. Below are the two most important user stories
illustrating the intended usage of the dtool cache manager:

- As a consumer of dtool I want to find out how much space the dtool cache
  is using so that I know if I need to clean it up or not.

- As a consumer of dtool I want to be able to free up disk space from the
  dtool cache by removing any files that have not been used in the past month.

Below are two less important user stories from the perspective of a data
manager.

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

To safely clean the cache one can use the command::

    dtool cache clean

The command above removes any files that have not been touched in the
past month. To clean the cache more or less aggressively one can use
the ``--older-than`` option. The command below removes any files older
than seven days.

To ::

    dtool cache clean --older-than 7


Technical details
-----------------

In the dtoolcore the content of items are accessed using the call:

.. code-block:: python

    dtoolcore.DataSet.item_content_abspath

This call includes a calls to pre- and a post-hook methods. These
can be accessed by adding the code block below to the setup.py file:

.. code-block:: python

    entry_points={
        "dtool.pre_item_content_abspath": [
            "dtool_cache_manager_pre_item_content_abspath=dtool_cache_manager:pre_item_content_abspath",
        ],
        "dtool.post_item_content_abspath": [
            "dtool_cache_manager_post_item_content_abspath=dtool_cache_manager:post_item_content_abspath",
        ],
    },

The ``dtool-cache-manager`` package then needs to implement:

.. code-block:: python

    def pre_item_content_abspath(uri, uuid):
        pass

    def pre_item_content_abspath(uri, uuid):
        pass

The ``dtool-cache-manager`` will also implement a helper function for safely
removing items from the cache:

.. code-block:: python

    def remove_cache_item(dataset_uuid, item_id):
        pass

As well as helper functions for finding stats about a cache item:

.. code-block:: python

    def item_num_times_accessed(dataset_uuid, item_id):
        """Return the number of times an item has been accessed."""

    def item_last_time_accessed(dataset_uuid, item_id):
        """Return the datetime when the item was last accessed."""

    def item_num_days_since_last_accessed(dataset_uuid, item_id):
        """Return the number of days since the item was last accessed."""

There will also be helper functions for finding out summary statistics about
the cache::

.. code-block:: python

    def cache_size():
        pass

    def cache_num_items():
        pass
