"""Splay tree: self-adjusting BST; accessed keys move to the root. Usage: python splay_tree.py"""


class Node:
    def __init__(self, key):
        self.key, self.left, self.right = key, None, None


class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        """Top-down splay: bring key (or last node on its search path) to the root."""
        if root is None:
            return None
        header = Node(None)
        left = right = header
        t = root
        while True:
            if key < t.key:
                if t.left is None:
                    break
                if key < t.left.key:
                    y = t.left
                    t.left, y.right = y.right, t
                    t = y
                    if t.left is None:
                        break
                right.left = t
                right, t = t, t.left
            elif key > t.key:
                if t.right is None:
                    break
                if key > t.right.key:
                    y = t.right
                    t.right, y.left = y.left, t
                    t = y
                    if t.right is None:
                        break
                left.right = t
                left, t = t, t.right
            else:
                break
        left.right, right.left = t.left, t.right
        t.left, t.right = header.right, header.left
        return t

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return
        n = Node(key)
        if key < self.root.key:
            n.right, n.left = self.root, self.root.left
            self.root.left = None
        else:
            n.left, n.right = self.root, self.root.right
            self.root.right = None
        self.root = n

    def find(self, key) -> bool:
        self.root = self._splay(self.root, key)
        return self.root is not None and self.root.key == key

    def delete(self, key) -> bool:
        if not self.find(key):
            return False
        l, r = self.root.left, self.root.right
        if l is None:
            self.root = r
        else:
            self.root = self._splay(l, key)  # max of left subtree surfaces
            self.root.right = r
        return True

    def inorder(self):
        out, stack, n = [], [], self.root
        while stack or n:
            while n:
                stack.append(n)
                n = n.left
            n = stack.pop()
            out.append(n.key)
            n = n.right
        return out


if __name__ == "__main__":
    t = SplayTree()
    for k in [5, 3, 8, 1, 4, 7, 9, 2, 6]:
        t.insert(k)
    print("sorted:", t.inorder())
    print("find 4:", t.find(4), "-> root is", t.root.key)
    print("delete 8:", t.delete(8), "delete 100:", t.delete(100))
    print("sorted:", t.inorder())
    assert t.inorder() == [1, 2, 3, 4, 5, 6, 7, 9]
