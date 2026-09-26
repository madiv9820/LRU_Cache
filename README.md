# [🕰️ The Cache That Remembers](https://leetcode.com/problems/lru-cache/?envType=study-plan-v2&envId=top-interview-150)

Imagine a small storage shelf 📦 that can hold only a fixed number of items. Whenever an item is accessed, it becomes **recently used** and gets priority to stay on the shelf. When the shelf is full and a new item arrives, the item that has been unused for the longest time must be removed 🗑️.

Design an **`LRUCache`** with a fixed **`capacity`** that supports two operations:

- 🔎 **`get(key)`** — Return the value associated with **`key`** if it exists; otherwise return **`-1`**. A successful access makes the key **most recently used**.
- ✏️ **`put(key, value)`** — Add a new key-value pair or update an existing one. Updating or inserting a key makes it **most recently used**. If the cache exceeds its capacity, remove the **least recently used** key.

#### 📌 Examples

- **📌 Example 1 — Accessing and Evicting Keys**

    For a cache with capacity **`2`**:

    ```
    put(1, 1)  → {1}
    put(2, 2)  → {1, 2}
    get(1)     → returns 1; 1 becomes most recently used
    put(3, 3)  → evicts 2
    get(2)     → returns -1
    ```

    The important detail is that **`get(1)`** changes the usage order, so **`2`** becomes the least recently used key and is removed when **`3`** is inserted.

- **📌 Example 2 — Updating an Existing Key**

    ```
    put(1, 10)
    put(2, 20)
    put(1, 100)
    ```

    The second **`put(1, 100)`** updates the existing value and also makes key **`1`** the **most recently used**. Therefore, if another key is inserted and an eviction is required, key **`2`** will be removed.

#### 📏 Constraints

- **`1 <= capacity <= 3000`**
- **`0 <= key <= 10⁴`**
- **`0 <= value <= 10⁵`**
- At most **`2 × 10⁵`** calls will be made to **`get`** and **`put`**.

#### ⚡ Performance Requirement

Both **`get`** and **`put`** must run **in `O(1)` average time**. Since up to **`2 × 10⁵`** operations can be performed, the cache must efficiently support lookup, updating usage order, insertion, and eviction without scanning all stored keys.

---