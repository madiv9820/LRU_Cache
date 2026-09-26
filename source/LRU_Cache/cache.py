from typing import Dict, Optional

class Node:
    def __init__(
        self,
        key: int,
        value: int,
        prev: Optional[Node] = None,
        next: Optional[Node] = None
    ) -> None:
        self.key: int = key
        self.value: int = value
        self.prev: Optional[Node] = prev
        self.next: Optional[Node] = next


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.size: int = 0

        # 👑 Head = Most Recently Used
        # 💤 Tail = Least Recently Used
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None

        # 🔑 key → Node
        self.cache: Dict[int, Node] = {}

    def get(self, key: int) -> int:
        if key not in self.cache: return -1

        node: Node = self.cache[key]

        # 🔄 Accessing a node makes it most recently used.
        self._moveToHead(node=node)

        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node: Node = self.cache[key]
            node.value = value

            # 🔄 Updated entries become most recently used.
            self._moveToHead(node=node)
            return

        node: Node = Node(
            key=key,
            value=value
        )

        # 👑 New entries are most recently used.
        self._addToHead(node=node)

        self.cache[key] = node
        self.size += 1

        # 🗑️ Evict the least recently used entry.
        if self.size > self.capacity:
            lruNode: Optional[Node] = self.tail

            if lruNode is not None:
                self._removeNode(node=lruNode)
                self.cache.pop(lruNode.key)
                self.size -= 1

    def _addToHead(self, node: Node) -> None:
        node.prev = None
        node.next = self.head

        if self.head is not None: self.head.prev = node
        else: self.tail = node

        self.head = node

    def _removeNode(self, node: Node) -> None:
        if node.prev is not None: node.prev.next = node.next
        else: self.head = node.next

        if node.next is not None: node.next.prev = node.prev
        else: self.tail = node.prev

        node.prev = None
        node.next = None

    def _moveToHead(self, node: Node) -> None:
        if node is self.head: return

        self._removeNode(node=node)
        self._addToHead(node=node)
