#!/usr/bin/env python3
""" 4-mru_cache.py - MRUCache module """

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache class that inherits from BaseCaching and implements MRU caching
    policy.
    """

    def __init__(self):
        """
        Initialize the class instance, setting up a dictionary to track item
        usage by order.
        """
        super().__init__()
        self.access_order = []

    def put(self, key, item):
        """
        Add or update an item in the cache.
        - key: Key of the item to add or update.
        - item: Item to add or update.
        If key or item is None, this method does nothing.
        If the cache exceeds `MAX_ITEMS`, the most recently used item is
        discarded.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.access_order.remove(key)
        elif len(self.cache_data) >= self.MAX_ITEMS:
            # Remove the most recently used item
            mru = self.access_order.pop(-1)
            self.cache_data.pop(mru)
            print("DISCARD: {}".format(mru))

        self.cache_data[key] = item
        self.access_order.append(key)

    def get(self, key):
        """
        Retrieve an item from the cache.
        - key: Key of the item to retrieve.
        Returns the value linked to key, or None if the key is not found or is
        None.
        """
        if key is None or key not in self.cache_data:
            return None

        # Refresh the access order since the item has been accessed
        self.access_order.remove(key)
        self.access_order.append(key)
        return self.cache_data[key]
