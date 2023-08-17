class RBTreeNode:

    def __init__(self, color, key, nil):
        self.color = color
        self.key = key
        self.left = nil
        self.right = nil
        self.fa = nil
        self.size = 1


class RBTree:

    def __init__(self):
        self.nil = RBTreeNode('B', None, None)
        self.nil.size = 0
        self.root = self.nil

    def _left_rotate(self, x):

        y = x.right
        x.right = y.left
        x.right.fa = x
        y.left = x
        y.fa = x.fa
        if x is x.fa.left:
            x.fa.left = y
        elif x is x.fa.right:
            x.fa.right = y
        else:
            assert x.fa is self.nil
            self.root = y
        x.fa = y
        x.size = x.left.size + x.right.size + 1
        y.size = y.left.size + y.right.size + 1

    def _right_rotate(self, x):

        y = x.left
        x.left = y.right
        x.left.fa = x
        y.right = x
        y.fa = x.fa
        if x is x.fa.left:
            x.fa.left = y
        elif x is x.fa.right:
            x.fa.right = y
        else:
            assert x.fa is self.nil
            self.root = y
        x.fa = y
        x.size = x.left.size + x.right.size + 1
        y.size = y.left.size + y.right.size + 1

    def insert(self, key):

        z = RBTreeNode('R', key, self.nil)
        y = self.nil
        x = self.root
        while x is not self.nil:
            y = x
            y.size += 1
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.fa = y
        if y is self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        self._insert_fixup(z)

    def _insert_fixup(self, z):

        while z.fa.color == 'R':
            if z.fa is z.fa.fa.left:
                y = z.fa.fa.right
                if y.color == 'R':
                    z.fa.color = y.color = 'B'
                    z.fa.fa.color = 'R'
                    z = z.fa.fa
                else:
                    if z is z.fa.right:
                        z = z.fa
                        self._left_rotate(z)
                    z.fa.color = 'B'
                    z.fa.fa.color = 'R'
                    self._right_rotate(z.fa.fa)
            else:
                y = z.fa.fa.left
                if y.color == 'R':
                    z.fa.color = y.color = 'B'
                    z.fa.fa.color = 'R'
                    z = z.fa.fa
                else:
                    if z is z.fa.left:
                        z = z.fa
                        self._right_rotate(z)
                    z.fa.color = 'B'
                    z.fa.fa.color = 'R'
                    self._left_rotate(z.fa.fa)
        self.root.color = 'B'

    def _transplant(self, old, new):

        if old.fa is self.nil:
            self.root = new
        elif old is old.fa.left:
            old.fa.left = new
        else:
            old.fa.right = new
        new.fa = old.fa
        x = new.fa
        while x is not self.nil:
            x.size = x.left.size + x.right.size + 1
            x = x.fa

    def find(self, key):

        x = self.root
        while x is not self.nil:
            if key == x.key:
                return x
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        return None

    def find_kth_elem(self, k):

        N = self.root.size
        if not (isinstance(k, int) and -N <= k < N):
            raise IndexError('index k should be within [-%d, %d), but k = %d' % (N, N, k))
        if k < 0:
            k += N
        x = self.root
        offset = 0
        while x is not self.nil:
            mid = x.left.size + offset
            if k == mid:
                return x.key
            if k < mid:
                x = x.left
            else:
                offset += x.left.size + 1
                x = x.right
        raise IndexError('valid index k, but key not found')

    def __getitem__(self, k):

        if isinstance(k, int):
            return self.find_kth_elem(k)
        elif isinstance(k, slice):
            ret = RBTree()
            N = self.root.size
            begin, end, step = k.indices(N)
            for i in range(begin, end, step):
                ret.insert(self.find_kth_elem(i))
            return ret




    def _iter_traverse(self, x, arr):

        if x is self.nil:
            return None
        self._iter_traverse(x.left, arr)
        arr.append(x.key)
        self._iter_traverse(x.right, arr)

    def __iter__(self):

        arr = []
        self._iter_traverse(self.root, arr)
        return iter(arr)

    def _leftmost(self, x):

        y = self.nil
        while x is not self.nil:
            y = x
            x = x.left
        return y

    def remove(self, key):

        z = self.find(key)
        if z is None:
            raise KeyError("Cannot find key '%s' in RBTree" % key)
        y = z
        y_orig_color = y.color
        if z.left is self.nil:
            x = z.right
        elif z.right is self.nil:
            x = z.left
        else:
            y = self._leftmost(z.right)
            y_orig_color = y.color
            z.key = y.key
            x = y.right
        self._transplant(y, x)
        if y_orig_color == 'B':
            self._remove_fixup(x)

    def _remove_fixup(self, x):

        while x is not self.root and x.color == 'B':
            if x is x.fa.left:
                w = x.fa.right
                if w.color == 'R':
                    w.color = 'B'
                    x.fa.color = 'R'
                    self._left_rotate(x.fa)
                    w = w.left.right
                if w.left.color == w.right.color == 'B':
                    w.color = 'R'
                    x = x.fa
                else:
                    if w.right.color == 'B':
                        w.left.color = 'B'
                        w.color = 'R'
                        self._right_rotate(w)
                        w = w.fa
                    w.color = w.fa.color
                    w.fa.color = w.right.color = 'B'
                    self._left_rotate(w.fa)
                    x = self.root
            else:
                w = x.fa.left
                if w.color == 'R':
                    w.color = 'B'
                    x.fa.color = 'R'
                    self._right_rotate(x.fa)
                    w = w.right.left
                if w.left.color == w.right.color == 'B':
                    w.color = 'R'
                    x = x.fa
                else:
                    if w.left.color == 'B':
                        w.right.color = 'B'
                        w.color = 'R'
                        self._left_rotate(w)
                        w = w.fa
                    w.color = w.fa.color
                    w.fa.color = w.left.color = 'B'
                    self._right_rotate(w.fa)
                    x = self.root
        x.color = 'B'



    def __str__(self):
        """Return the string converted from the list(iterator) object"""
        return str(list(self.__iter__()))



tree = RBTree()
for item in range(1, 10):
    tree.insert(item)

print(tree)
tree.remove(6)
print(tree)
