'''
This file implements the Heap data structure as a subclass of the BinaryTree.
The book implements Heaps using an *implicit* tree with an *explicit* vector implementation,
so the code in the book is likely to be less helpful than the code for the other data structures.
The book's implementation is the traditional implementation because it has a faster constant factor
(but the same asymptotics).
This homework is using an explicit tree implementation to help you get more practice with OOP-style programming and classes.
'''

from containers.BinaryTree import BinaryTree, Node


class Heap(BinaryTree):
    '''
    FIXME:
    Heap is currently not a subclass of BinaryTree.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the Heap.
        '''
        super().__init__()
        if xs is not None:
            self.insert_list(xs)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string that can be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command Heap([1,2,3])
        it's __repr__ will return "Heap([1,2,3])"

        For the Heap, type(self).__name__ will be the string "Heap",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of Heap will have a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def is_heap_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether insert/delete functions
        are actually working.
        '''
        if self.root:
            return Heap._is_heap_satisfied(self.root)
        return True

    @staticmethod
    def _is_heap_satisfied(node):
        '''
        FIXME:
        Implement this method.
        '''
        ret_val = True
        if node is None:
            return ret_val
        ret_val &= Heap._is_complete(node)
        if node.left and node.right:
            # check max heap
            if node.value > node.left.value:
                if node.value < node.right.value:
                    return False
            if node.value > node.right.value:
                if node.value < node.left.value:
                    return False
            # check min heap
            if node.value < node.left.value:
                if node.value > node.right.value:
                    return False
            if node.value < node.right.value:
                if node.value > node.left.value:
                    return False
        if node.left:
            if node.left.value < node.value:
                return False
            ret_val &= Heap._is_heap_satisfied(node.left)
        if node.right:
            if node.right.value < node.value:
                return False
            ret_val &= Heap._is_heap_satisfied(node.right)
        return ret_val

    @staticmethod
    def _is_complete(node):
        ret = True
        # check vertical completeness
        if BinaryTree._height(node) > 2:
            if node.left is None or node.right is None:
                return False
            else:
                ret &= Heap._is_complete(node.left)
                ret &= Heap._is_complete(node.right)
            # horizontal grandchild: if 3 exists 2 must
            if node.right.left:
                if node.left.right is None:
                    return False
        # check horizontal left to right
        if BinaryTree._height(node) == 2:
            # if 2 / 4 exists, 1 / 3 must
            if node.right and node.left is None:
                return False
        return ret

    def insert(self, value):
        '''
        Inserts value into the heap.

        FIXME:
        Implement this function.

        HINT:
        The pseudo code is
        1. Find the next position in the tree using the binary representation of the total number of nodes
            1. You will have to explicitly store the size of your heap in a variable (rather than compute it) to maintain the O(log n) runtime
            1. See https://stackoverflow.com/questions/18241192/implement-heap-using-a-binary-tree for hints
        1. Add `value` into the next position
        1. Recursively swap value with its parent until the heap property is satisfied

        HINT:
        Create a @staticmethod helper function,
        following the same pattern used in the BST and AVLTree insert functions.
        '''
        if self.root:
            next_po = Heap._count_node(self.root)
            next_po_bi = bin(next_po)[3:]
            return Heap._insert(self.root, value, next_po_bi)
        else:
            self.root = Node(value)

    @staticmethod
    def _insert(node, value, bi_path):
        # insert value to the new node position
        while len(bi_path) > 0:
            if bi_path[0] == "0":
                if node.left is None:
                    node.left = Node(value)
                    # swap after insert
                    if node.left.value < node.value:
                        return Heap._swap(node, "left")
                    else:
                        return node
                else:
                    node.left = Heap._insert(node.left, value, bi_path[1:])
            if bi_path[0] == "1":
                if node.right is None:
                    node.right = Node(value)
                    # swap after insert
                    if node.right.value < node.value:
                        return Heap._swap(node, "right")
                    else:
                        return node
                else:
                    node.right = Heap._insert(node.right, value, bi_path[1:])

    @staticmethod
    def _swap(node, swap_direction):
        # swap value with left child when direction is left
        if swap_direction == "left":
            placeholder = node.value
            node.value = node.left.value
            node.left.value = placeholder
            return node
        if swap_direction == "right":
            placeholder = node.value
            node.value = node.right.value
            node.right.value = placeholder

    @staticmethod
    def _count_node(node):
        node_counter = 0
        if node:
            node_counter += 1
            Heap._count_node(node.left)
            Heap._count_node(node.right)
        if node is None:
            return
        return node_counter + 1

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.
        '''
        for x in xs:
            self.insert(x)

    def find_smallest(self):
        '''
        Returns the smallest value in the tree.

        FIXME:
        Implement this function.
        '''
        if self.root:
            return Heap._find_smallest(self.root)
        else:
            return None

    @staticmethod
    def _find_smallest(node):
        assert node is not None
        return node.value

    def remove_min(self):
        '''
        Removes the minimum value from the Heap.
        If the heap is empty, it does nothing.

        FIXME:
        Implement this function.

        HINT:
        The pseudocode is
        1. remove the bottom right node from the tree
        2. replace the root node with what was formerly the bottom right
        3. "trickle down" the root node: recursively swap it with its largest child until the heap property is satisfied

        HINT:
        I created two @staticmethod helper functions: _remove_bottom_right and _trickle.
        It's possible to do it with only a single helper (or no helper at all),
        but I personally found dividing up the code into two made the most sense.
        '''
        if not self.root:
            return
        if self.root.right is None and self.root.left is None:
            return None
        else:
            next_po = Heap._count_node(self.root)
            next_po_bi = bin(next_po)[3:]
            remove_node = Heap._remove(self.root, next_po_bi)
            self.root.value = remove_node.value
            Heap._trickle(self.root)

    @staticmethod
    def _remove(node, bi_path):
        remove_node = node
        while len(bi_path) > 1:
            if bi_path[0] == "0":
                remove_node = Heap._remove(remove_node.left, bi_path[1:])
            if bi_path[1] == "1":
                remove_node = Heap._remove(remove_node.right, bi_path[1:])
        if len(bi_path) == 1:
            if bi_path[0] == "0":
                remove_node = remove_node.left
                placeholder = remove_node
                remove_node = None
            if bi_path[0] == "1":
                remove_node = remove_node.right
                placeholder = remove_node
                remove_node = None
        return placeholder

    @staticmethod
    def _trickle(node):
        if node.left is None:
            return None
        elif node.right is None or node.left.value < node.right.value:
            swap_dir = "left"
            nx_node = node.left
        else:
            swap_dir = "right"
            nx_node = node.right
        if nx_node.value < node.value:
            Heap._swap(node, swap_dir)
            Heap._trickle(nx_node)
