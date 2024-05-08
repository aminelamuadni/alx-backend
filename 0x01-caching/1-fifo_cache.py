#!/usr/bin/env python3
""" 1-fifo_cache.py - FIFOCache module """

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache class that inherits from BaseCaching and implements FIFO caching
    policy.
    """

    def __init__(self):
        """
        Initialize the class instance, setting up any necessary variables
        (e.g., for tracking the order of items).
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Add an item to the cache.
        - key: Key of the item to add.
        - item: Item to add.
        If key or item is None, this method does nothing.
        If the cache exceeds `MAX_ITEMS`, the oldest item is discarded.
        """
        if key is not None and item is not None:
            if key not in self.cache_data:
                if len(self.cache_data) >= self.MAX_ITEMS:
                    oldest_key = self.order.pop(0)
                    self.cache_data.pop(oldest_key)
                    print("DISCARD: {}".format(oldest_key))
                self.order.append(key)
            else:
                self.order.remove(key)
                self.order.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """
        Get an item by key.
        - key: Key of the item to retrieve.
        Returns the value in self.cache_data linked to key.
        If key is None or if the key doesn’t exist in self.cache_data, returns
        None.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
