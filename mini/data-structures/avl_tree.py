"""AVL self-balancing binary search tree. Usage: python avl_tree.py"""


class Node:
    def __init__(self, key):
        self.key, self.left, self.right, self.h = key, None, None, 1


def h(n): return n.h if n else 0
def upd(n): n.h = 1 + max(h(n.left), h(n.right))
def bal(n): return h(n.left) - h(n.right)


def rot_right(y):
    x = y.left
    y.left, x.right = x.right, y
    upd(y); upd(x)
    return x


def rot_left(x):
    y = x.right
    x.right, y.left = y.left, x
    upd(x); upd(y)
    return y


def insert(n, key):
    if n is None:
        return Node(key)
    if key < n.key:
        n.left = insert(n.left, key)
    elif key > n.key:
        n.right = insert(n.right, key)
    else:
        return n
    upd(n)
    b = bal(n)
    if b > 1:
        if key > n.left.key:
            n.left = rot_left(n.left)
        return rot_right(n)
    if b < -1:
        if key < n.right.key:
            n.right = rot_right(n.right)
        return rot_left(n)
    return n


def inorder(n):
    if n:
        yield from inorder(n.left)
        yield n.key
        yield from inorder(n.right)


if __name__ == "__main__":
    root = None
    for k in range(1, 1024):  # sorted input: worst case for a plain BST
        root = insert(root, k)
    assert list(inorder(root)) == list(range(1, 1024))
    assert root.h <= 11
    print("avl ok, height", root.h)
