from leaves import NodeList, NodeMixin


class N(NodeMixin):
    def __init__(self, name=None):
        self.name = name
        super(N, self).__init__()

    def __repr__(self):
        return 'N(%s)' % self.name


def test_nodelist_sets_parent_on_values():
    parent = N()

    n1 = N(1)
    assert n1.parent is None
    parent.children.append(n1)
    assert n1.parent == parent

    n2 = N(2)
    parent.children[0] = n2
    assert n2.parent == parent

    n3 = N(3)
    parent.children.insert(1, n3)
    assert n3.parent == parent

    n4 = N(4)
    parent.children.extend([n4])
    assert n4.parent == parent

    n5 = N(5)
    parent.children[1:1] = [n5]
    assert n5.parent == parent

    parent.children = (n1, n2, n3)
    assert isinstance(parent.children, NodeList)
    assert n1.parent == n2.parent == n3.parent == parent


def test_leaf_list():

    root = N('root')

    def assert_leaves(*expected_leaves):
        assert root.leaves == expected_leaves

    assert_leaves(root)

    n1, n2, n3 = N(1), N(2), N(3)
    root.children.extend((n1, n2, n3))
    assert_leaves(n1, n2, n3)

    n21, n22 = N(21), N(22)
    n2.children = (n21, n22)
    assert_leaves(n1, n21, n22, n3)

    n31 = N(31)
    n3.children.append(n31)
    assert_leaves(n1, n21, n22, n31)

    n311 = N(311)
    n31.children.append(n311)
    assert_leaves(n1, n21, n22, n311)

    n32 = N(32)
    n3.children.append(n32)
    assert_leaves(n1, n21, n22, n311, n32)

    n11, n12, n13 = N(11), N(12), N(13)
    n1.children.extend((n11, n12, n13))
    assert_leaves(n11, n12, n13, n21, n22, n311, n32)

    n2.children = []
    assert_leaves(n11, n12, n13, n2, n311, n32)
