"""
A class for our tree.
"""


class Node:
    def __init__(self, parent, level, data=None):
        self.data = data
        self.parent = parent
        self.kids = dict()
        self.level = level
        return


class Tree:
    def __init__(self):
        self.Head = Node(None, 0)
        self.Active = self.Head
        return

    def add(self, key, data):
        self.Active.kids[key] = Node(self.Active, self.Active.level+1, data)
        return

    def delete(self, key):
        self.Active.kids.pop(key)
        return

    def back_to_head(self):
        self.Active = self.Head
        return
