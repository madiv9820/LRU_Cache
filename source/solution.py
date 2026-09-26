from typing import List, Any
from .LRU_Cache import LRUCache

class Solution:
    def execute(self, operations: List[str], values: List[List[int]]) -> List[Any]:
        # 🧠 Create the cache using the first operation's capacity.
        cache = LRUCache(values[0][0])

        results: List[Any] = [None]

        # ⚙️ Execute each cache operation in sequence.
        for operation, arguments in zip(operations[1:], values[1:]):
            if operation == 'put':
                cache.put(arguments[0], arguments[1])
                results.append(None)
            
            elif operation == 'get':
                results.append(cache.get(arguments[0]))

        return results
