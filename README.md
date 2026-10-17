# persistent_linked_list

An immutable singly linked list where every `cons` produces a new head node sharing its tail with the predecessor, so old versions stay valid and unchanged.

```python
from persistent_linked_list import Cons, Nil

base = Cons(1, Nil()).cons(2).cons(3)   # [3, 2, 1]
extended = base.cons(4)                 # [4, 3, 2, 1]; base unchanged
list(base)      # [3, 2, 1]
list(extended)  # [4, 3, 2, 1]
base.head       # 3
extended.head   # 4
```

## Why this exists

When you need cheap snapshots of a list-like structure — undo stacks, backtracking
search, functional pipelines where each step should not destroy its input — a
persistent linked list gives O(1) prepend and O(1) structure sharing. The
trade-off is that random access is O(n), there is no in-place mutation, and
long iteration walks a chain of heap nodes rather than a contiguous array.

The head value and tail reference are set once at construction and the node
objects refuse attribute assignment, so any reference held to a previous
version remains a stable view of the list at that point in time.

## Edge to know about

Equality and hashing recurse into elements. A list containing an unhashable
head (for example another mutable list) will raise `TypeError` when hashed.
This is intentional: a persistent container's hash is derived from its
contents, so it can only be as hashable as those contents allow.

Accessing `.head` or `.tail` on `Nil` raises `EmptyListError`, which is a
subclass of `IndexError` so it integrates with ordinary sequence-error
handling. Negative indexing and slices work and return tuple-backed results.
