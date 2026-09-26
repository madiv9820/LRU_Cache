"""
🧩 Solution wrapper for the LRU Cache implementation.

This file translates the operation-based test input into actual
LRUCache method calls.

📦 The first operation creates the cache with its given capacity.
⚙️ Subsequent operations execute get() and put() in sequence.
📋 Results are collected in the same order as the operations.

The actual LRU logic is implemented inside LRUCache.
"""

from typing import Any, List
from .LRU_Cache import LRUCache

class Solution:
    def execute(
        self,
        operations: List[str],
        values: List[List[int]]
    ) -> List[Any]:
        
        # 📦 Create the cache using the capacity from the first input.
        cache = LRUCache(capacity=values[0][0])

        # 📋 The constructor operation does not produce a result.
        results: List[Any] = [None]

        # ⚙️ Execute every cache operation in its given order.
        for operation, arguments in zip(
            operations[1:],
            values[1:]
        ):
            if operation == 'put':
                # ✏️ Add or update a key-value pair.
                cache.put(
                    key=arguments[0],
                    value=arguments[1]
                )

                # 📋 put() does not return a value.
                results.append(None)

            elif operation == 'get':
                # 🔎 Retrieve the value and record the result.
                results.append(
                    cache.get(key=arguments[0])
                )

        return results
