#!/usr/bin/env python3
""" 2-lifo_cache.py - LIFOCache module """

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache class that inherits from BaseCaching and implements LIFO caching
    policy.
    """

    def __init__(self):
        """
        Initialize the class instance, maintaining a stack to track the last
        item added.
        """
        super().__init__()
        self.stack = []  # Stack to keep track of the keys' order

    def put(self, key, item):
        """
        Add an item to the cache.
        - key: Key of the item to add.
        - item: Item to add.
        If key or item is None, this method does nothing.
        If the cache exceeds `MAX_ITEMS`, the last item added before the new
        one is discarded.
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.stack.remove(key)
            elif len(self.cache_data) >= self.MAX_ITEMS:
                last_in = self.stack.pop()
                self.cache_data.pop(last_in)
                print("DISCARD: {}".format(last_in))

            self.cache_data[key] = item
            self.stack.append(key)

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
