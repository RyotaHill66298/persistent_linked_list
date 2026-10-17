import unittest

from persistent_linked_list import Cons, Nil, EmptyListError


class TestNil(unittest.TestCase):
    def test_is_singleton(self):
        self.assertIs(Nil(), Nil())

    def test_is_empty(self):
        self.assertTrue(Nil().is_empty)

    def test_length_zero(self):
        self.assertEqual(Nil().length, 0)
        self.assertEqual(len(Nil()), 0)

    def test_head_raises(self):
        with self.assertRaises(EmptyListError):
            Nil().head

    def test_tail_raises(self):
        with self.assertRaises(EmptyListError):
            Nil().tail

    def test_iter_empty(self):
        self.assertEqual(list(Nil()), [])

    def test_bool_false(self):
        self.assertFalse(bool(Nil()))

    def test_getitem_raises_index_error(self):
        with self.assertRaises(IndexError):
            Nil()[0]

    def test_repr(self):
        self.assertEqual(repr(Nil()), "Nil")

    def test_eq_identity(self):
        self.assertEqual(Nil(), Nil())
        self.assertFalse(Nil() != Nil())


class TestCons(unittest.TestCase):
    def test_single_cons(self):
        lst = Cons(1, Nil())
        self.assertFalse(lst.is_empty)
        self.assertEqual(lst.head, 1)
        self.assertEqual(lst.tail, Nil())
        self.assertEqual(lst.length, 1)
        self.assertEqual(len(lst), 1)

    def test_cons_chains_values(self):
        lst = Cons(1, Nil()).cons(2).cons(3)
        self.assertEqual(list(lst), [3, 2, 1])
        self.assertEqual(lst.length, 3)

    def test_cons_via_constructor_and_method_are_equivalent(self):
        a = Cons(5, Cons(4, Cons(3, Nil())))
        b = Nil().cons(3).cons(4).cons(5)
        self.assertEqual(list(a), list(b))
        self.assertEqual(a, b)

    def test_bool_true(self):
        self.assertTrue(bool(Cons(0, Nil())))

    def test_iter_yields_in_order(self):
        lst = Cons(10, Cons(20, Cons(30, Nil())))
        self.assertEqual(list(lst), [10, 20, 30])

    def test_getitem_positive(self):
        lst = Cons(10, Cons(20, Cons(30, Nil())))
        self.assertEqual(lst[0], 10)
        self.assertEqual(lst[1], 20)
        self.assertEqual(lst[2], 30)

    def test_getitem_negative(self):
        lst = Cons(10, Cons(20, Cons(30, Nil())))
        self.assertEqual(lst[-1], 30)
        self.assertEqual(lst[-2], 20)
        self.assertEqual(lst[-3], 10)

    def test_getitem_out_of_range(self):
        lst = Cons(10, Cons(20, Nil()))
        with self.assertRaises(IndexError):
            lst[2]
        with self.assertRaises(IndexError):
            lst[-3]

    def test_getitem_slice(self):
        lst = Cons(10, Cons(20, Cons(30, Nil())))
        self.assertEqual(lst[1:], (20, 30))
        self.assertEqual(lst[0:2], (10, 20))

    def test_repr_roundtrips(self):
        lst = Cons(1, Cons(2, Nil()))
        self.assertEqual(repr(lst), "Cons(1, Cons(2, Nil))")

    def test_equality_same_values(self):
        a = Cons(1, Cons(2, Nil()))
        b = Cons(1, Cons(2, Nil()))
        self.assertEqual(a, b)
        self.assertFalse(a != b)

    def test_inequality_different_values(self):
        a = Cons(1, Cons(2, Nil()))
        b = Cons(1, Cons(3, Nil()))
        self.assertNotEqual(a, b)

    def test_inequality_different_length(self):
        a = Cons(1, Cons(2, Nil()))
        b = Cons(1, Nil())
        self.assertNotEqual(a, b)

    def test_hash_equal_lists_match(self):
        a = Cons(1, Cons(2, Nil()))
        b = Cons(1, Cons(2, Nil()))
        self.assertEqual(hash(a), hash(b))

    def test_head_is_immutable(self):
        lst = Cons(1, Nil())
        with self.assertRaises(AttributeError):
            lst._head = 99

    def test_tail_is_immutable(self):
        lst = Cons(1, Nil())
        with self.assertRaises(AttributeError):
            lst._tail = Nil()

    def test_tail_type_check(self):
        with self.assertRaises(TypeError):
            Cons(1, [2, 3])


class TestPersistence(unittest.TestCase):
    def test_cons_preserves_predecessor(self):
        base = Cons(2, Cons(1, Nil()))
        extended = base.cons(3)
        self.assertEqual(list(base), [2, 1])
        self.assertEqual(list(extended), [3, 2, 1])

    def test_predecessor_head_unchanged_after_cons(self):
        base = Cons(2, Cons(1, Nil()))
        extended = base.cons(3)
        self.assertEqual(base.head, 2)
        self.assertEqual(extended.head, 3)

    def test_structure_shared_same_tail_object(self):
        base = Cons(2, Cons(1, Nil()))
        extended = base.cons(3)
        self.assertIs(extended.tail, base)

    def test_nil_cons_preserves_nil(self):
        single = Nil().cons(42)
        self.assertIs(single.tail, Nil())


class TestEdgeCases(unittest.TestCase):
    def test_none_values_allowed(self):
        lst = Cons(None, Cons(None, Nil()))
        self.assertEqual(list(lst), [None, None])

    def test_mixed_types_allowed(self):
        lst = Cons(1, Cons("two", Cons(3.0, Nil())))
        self.assertEqual(list(lst), [1, "two", 3.0])

    def test_nested_lists_allowed(self):
        inner = Cons(1, Nil())
        outer = Cons(inner, Cons("x", Nil()))
        self.assertEqual(outer.head, inner)
        self.assertEqual(outer.head.head, 1)

    def test_unhashable_head_breaks_hash(self):
        lst = Cons([1, 2], Nil())
        with self.assertRaises(TypeError):
            hash(lst)


if __name__ == "__main__":
    unittest.main()
