#!/usr/bin/env python3
""" 100-lfu_cache.py - LFUCache module """

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache class that inherits from BaseCaching and implements the LFU
    caching policy.
    This class tracks both frequency and recency of accesses.
    """

    def __init__(self):
        """
        Initialize the class instance along with two helper dictionaries for
        managing frequency and the order of access.
        """
        super().__init__()
        self.frequency = {}
        self.access_time = {}
        self.time = 0

    def put(self, key, item):
        """
        Add or update an item in the cache.
        - key: Key of the item to add or update.
        - item: Item to add or update.
        If key or item is None, this method does nothing.
        If the cache exceeds `MAX_ITEMS`, the least frequently used item, and
        among them the least recently used, is discarded.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency[key] += 1
            self.access_time[key] = self.time
            self.time += 1
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            # Find the least frequently used key
            lfu_key = min(self.frequency, key=lambda k: (self.frequency[k],
                                                         self.access_time[k]))
            print("DISCARD: {}".format(lfu_key))
            self.cache_data.pop(lfu_key)
            self.frequency.pop(lfu_key)
            self.access_time.pop(lfu_key)

        self.cache_data[key] = item
        self.frequency[key] = 1
        self.access_time[key] = self.time
        self.time += 1

    def get(self, key):
        """
        Retrieve an item from the cache.
        - key: Key of the item to retrieve.
        Returns the value linked to key, or None if the key is not found or is
        None.
        """
        if key is None or key not in self.cache_data:
            return None

        self.frequency[key] += 1
        self.access_time[key] = self.time
        self.time += 1
        return self.cache_data[key]
