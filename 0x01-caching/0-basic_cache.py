#!/usr/bin/env python3
""" 0-basic_cache.py - BasicCache module """

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache class that inherits from BaseCaching and is a caching system.
    - This caching system doesn’t have a limit.
    """

    def put(self, key, item):
        """
        Add an item to the cache.
        - key: Key of the item to add.
        - item: Item to add.
        If key or item is None, this method does nothing.
        """
        if key is not None and item is not None:
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
