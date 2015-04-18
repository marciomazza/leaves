

class NodeList(list):

    def __init__(self, node):
        self.node = node
        super(NodeList, self).__init__()

    def _with_parent(self, value):
        value.parent = self.node
        return value

    def _all_with_parent(self, iterable):
        for value in iterable:
            yield self._with_parent(value)

    def __setitem__(self, index, value):
        list.__setitem__(self, index, self._with_parent(value))

    def __setslice__(self, i, j, iterable):
        list.__setslice__(self, i, j, self._all_with_parent(iterable))

    def append(self, value):
        list.append(self, self._with_parent(value))

    def insert(self, index, value):
        list.insert(self, index, self._with_parent(value))

    def extend(self, iterable):
        list.extend(self, self._all_with_parent(iterable))


class NodeMixin(object):

    def __init__(self):
        self.parent = None
        self._children = NodeList(self)

    @property
    def is_root(self):
        return not self.parent

    @property
    def root(self):
        if self.parent:
            return self.parent.root
        else:
            return self

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = NodeList(self)
        self._children.extend(value)

    def _leaves(self):
        if not self.children:
            yield self
        else:
            for child in self.children:
                for leaf in child._leaves():
                    yield leaf

    @property
    def leaves(self):
        return tuple(self._leaves())
