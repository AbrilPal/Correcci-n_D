class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.transitions = {}

    def is_leaf(self):
        return self.left is None and self.right is None
