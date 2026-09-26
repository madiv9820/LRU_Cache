"""
🧠 LRU Cache using HashMap and Doubly Linked List.

🔑 The HashMap provides O(1) average access to a node by key.
🔗 The Doubly Linked List maintains the usage order of cache entries.

👑 Head → Most Recently Used
💤 Tail → Least Recently Used

🔄 Accessed or updated entries move to the head.
🗑️ When capacity is exceeded, the tail node is evicted.

⚡ Together, both data structures allow get() and put()
   to run in O(1) average time.
"""

from typing import Dict, Optional

class Node:
    def __init__(
        self,
        key: int,
        value: int,
        prev: Optional[Node] = None,
        next: Optional[Node] = None
    ) -> None:
        # 🔑 Keep the key so the node can be removed from the HashMap.
        self.key: int = key

        # 💾 Store the value associated with the key.
        self.value: int = value

        # ◀️ Previous node in the doubly linked list.
        self.prev: Optional[Node] = prev

        # ▶️ Next node in the doubly linked list.
        self.next: Optional[Node] = next

class LRUCache:
    def __init__(self, capacity: int) -> None:
        # 📦 Maximum number of entries the cache can store.
        self.capacity: int = capacity

        # 🔢 Current number of entries in the cache.
        self.size: int = 0

        # 👑 Head = Most Recently Used.
        # 💤 Tail = Least Recently Used.
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None

        # ⚡ Map each key directly to its linked-list node.
        self.cache: Dict[int, Node] = {}

    def get(self, key: int) -> int:
        # ❌ Return -1 when the key is not present.
        if key not in self.cache:
            return -1

        # 🔎 Find the node directly through the HashMap.
        node: Node = self.cache[key]

        # 🔄 Access makes this node Most Recently Used.
        self._moveToHead(node=node)

        return node.value

    def put(self, key: int, value: int) -> None:
        # ♻️ Update the existing node instead of creating a duplicate.
        if key in self.cache:
            node: Node = self.cache[key]
            node.value = value

            # 👑 Updated entry becomes Most Recently Used.
            self._moveToHead(node=node)
            return

        # 🆕 Create a node for the new cache entry.
        node: Node = Node(
            key=key,
            value=value
        )

        # 👑 New entries are always placed at the head.
        self._addToHead(node=node)

        # 🔗 Store the same node in the HashMap.
        self.cache[key] = node
        self.size += 1

        # 🗑️ Remove the Least Recently Used entry if full.
        if self.size > self.capacity:
            lruNode: Optional[Node] = self.tail

            if lruNode is not None:
                # ✂️ Remove the LRU node from the linked list.
                self._removeNode(node=lruNode)

                # 🧹 Remove the evicted key from the HashMap.
                self.cache.pop(lruNode.key)

                self.size -= 1

    def _addToHead(self, node: Node) -> None:
        # 👑 Insert the node at the Most Recently Used position.
        node.prev = None
        node.next = self.head

        if self.head is not None:
            # 🔗 Link the old head back to the new head.
            self.head.prev = node
        else:
            # 🏁 First node becomes both head and tail.
            self.tail = node

        self.head = node

    def _removeNode(self, node: Node) -> None:
        # ✂️ Connect the previous node to the next node.
        if node.prev is not None:
            node.prev.next = node.next
        else:
            # ⬅️ Removing the head moves head forward.
            self.head = node.next

        # 🔗 Connect the next node back to the previous node.
        if node.next is not None:
            node.next.prev = node.prev
        else:
            # 💤 Removing the tail moves tail backward.
            self.tail = node.prev

        # 🧹 Fully detach the node from the linked list.
        node.prev = None
        node.next = None

    def _moveToHead(self, node: Node) -> None:
        # 👑 Already Most Recently Used.
        if node is self.head:
            return

        # ✂️ Remove the node from its current position.
        self._removeNode(node=node)

        # 👑 Reinsert it at the head as Most Recently Used.
        self._addToHead(node=node)
