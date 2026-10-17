"""Core implementation of a persistent (immutable) singly linked list.

Persistence is achieved by never mutating any node after construction.
Every cons operation allocates a fresh head node that references the previous
tail, so all prior versions remain valid and independent.
"""


class EmptyListError(IndexError):
    """Raised on head/tail access of an empty persistent list.

    Subclassing IndexError lets callers treat it as a sequence-index failure
    when that is meaningful.
    """


class Nil:
    """Sentinel representing the empty persistent list.

    A single class (rather than a per-call object) is used so that 'is' identity
    comparisons on Nil are cheap and canonical.
    """

    __slots__ = ()
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @property
    def is_empty(self):
        return True

    @property
    def head(self):
        raise EmptyListError("head of empty persistent list")

    @property
    def tail(self):
        raise EmptyListError("tail of empty persistent list")

    @property
    def length(self):
        return 0

    def cons(self, value):
        return Cons(value, self)

    def __iter__(self):
        return iter(())

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(())

    def __len__(self):
        return 0

    def __getitem__(self, index):
        raise IndexError("index out of range")

    def __repr__(self):
        return "Nil"

    def __bool__(self):
        return False


class Cons:
    """A non-empty persistent singly linked list node.

    Holds an immutable head value and an immutable reference to the tail node.
    The same tail can be referenced by any number of cons cells, which is how
    structure sharing keeps each new list O(1) to construct.
    """

    __slots__ = ("_head", "_tail", "_length", "_hash")

    def __init__(self, head, tail):
        object.__setattr__(self, "_head", head)
        if isinstance(tail, (Cons, Nil)):
            object.__setattr__(self, "_tail", tail)
        else:
            raise TypeError("tail must be a Cons or Nil instance")
        object.__setattr__(self, "_length", tail.length + 1)
        object.__setattr__(self, "_hash", None)

    def __setattr__(self, name, value):
        raise AttributeError("persistent list nodes are immutable")

    def __delattr__(self, name):
        raise AttributeError("persistent list nodes are immutable")

    @property
    def is_empty(self):
        return False

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail

    @property
    def length(self):
        return self._length

    def cons(self, value):
        return Cons(value, self)

    def __iter__(self):
        node = self
        while isinstance(node, Cons):
            yield node._head
            node = node._tail

    def __eq__(self, other):
        if self is other:
            return True
        if isinstance(other, Cons) and self._length == other._length:
            a, b = self, other
            while isinstance(a, Cons) and isinstance(b, Cons):
                if a._head != b._head:
                    return False
                a = a._tail
                b = b._tail
            return a is b
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        cached = self._hash
        if cached is None:
            cached = hash(tuple(iter(self)))
            object.__setattr__(self, "_hash", cached)
        return cached

    def __len__(self):
        return self._length

    def __getitem__(self, index):
        if isinstance(index, slice):
            return tuple(self)[index]
        if index < 0:
            index += self._length
            if index < 0:
                raise IndexError("index out of range")
        node = self
        pos = 0
        while isinstance(node, Cons):
            if pos == index:
                return node._head
            node = node._tail
            pos += 1
        raise IndexError("index out of range")

    def __repr__(self):
        return "Cons(" + repr(self._head) + ", " + repr(self._tail) + ")"

    def __bool__(self):
        return True
