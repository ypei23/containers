'''
The file implements the AVL Tree data structure.
The functions in this file are considerably harder than the functions in the BinaryTree and BST files,
but there are fewer of them.
'''

from containers.BinaryTree import BinaryTree, Node
from containers.BST import BST


class AVLTree(BST):
    '''
    FIXME:
    AVLTree is currently not a subclass of BST.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        Implement this function.
        '''
        super().__init__()
        if xs is not None:
            self.insert_list(xs)

    def balance_factor(self):
        '''
        Returns the balance factor of a tree.
        '''
        return AVLTree._balance_factor(self.root)

    @staticmethod
    def _balance_factor(node):
        '''
        Returns the balance factor of a node.
        '''
        if node is None:
            return 0
        return BinaryTree._height(node.left) - BinaryTree._height(node.right)

    def is_avl_satisfied(self):
        '''
        Returns True if the avl tree satisfies that all nodes have a balance factor in [-1,0,1].
        '''
        return AVLTree._is_avl_satisfied(self.root)

    @staticmethod
    def _is_avl_satisfied(node):
        '''
        FIXME:
        Implement this function.
        '''
        if node is None:
            return True
        ret = True
        if AVLTree._balance_factor(node) > -2 and AVLTree._balance_factor(node) < 2:
            ret = True
        else:
            return False
        if node.right:
            ret &= AVLTree._is_avl_satisfied(node.right)
        if node.left:
            ret &= AVLTree._is_avl_satisfied(node.left)
        return ret

    @staticmethod
    def _left_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        if node.right:
            node_smallest_f_right = node.right.left
            post_rt_root = Node(node.right.value)
            post_rt_root.left = Node(node.value)
            post_rt_root.left.right = node_smallest_f_right
            post_rt_root.right = node.right.right
            post_rt_root.left.left = node.left
        else:
            return node
        return post_rt_root

    @staticmethod
    def _right_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        if node.left:
            node_largest_f_left = node.left.right
            post_rt_root = Node(node.left.value)
            post_rt_root.right = Node(node.value)
            post_rt_root.right.left = node_largest_f_left
            post_rt_root.left = node.left.left
            post_rt_root.right.right = node.right
        else:
            return node
        return post_rt_root

    def insert(self, value):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of how to insert into an AVL tree,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.

        HINT:
        It is okay to add @staticmethod helper functions for this code.
        The code should look very similar to the code for your insert function for the BST,
        but it will also call the left and right rebalancing functions.
        '''
        if self.root:
            self._insert(self.root, value)
            while not self.is_avl_satisfied():
                self.root = self.rebalance(self.root)
            return
        else:
            self.root = Node(value)
            return

    @staticmethod
    def _insert(node, value):
        if node.value > value:
            if node.left:
                return AVLTree._insert(node.left, value)
            else:
                node.left = Node(value)
                return node
        if node.value < value:
            if node.right:
                return AVLTree._insert(node.right, value)
            else:
                node.right = Node(value)
                return node

    def rebalance(self, node):
        if node is None:
            return
        if self._balance_factor(node) < -1 or self._balance_factor(node) > 1:
            node = self._rebalance(node)
        else:
            node.left = self.rebalance(node.left)
            node.right = self.rebalance(node.right)
        return node

    @staticmethod
    def _rebalance(node):
        '''
        There are no test cases for the rebalance function,
        so you do not technically have to implement it.
        But both the insert function needs the rebalancing code,
        so I recommend including that code here.
        '''
        if node is None:
            return
        if AVLTree._balance_factor(node) < 0:
            if AVLTree._balance_factor(node.right) > 0:
                node.right = AVLTree._right_rotate(node.right)
                return AVLTree._left_rotate(node)
            else:
                return AVLTree._left_rotate(node)
        elif AVLTree._balance_factor(node) > 0:
            if AVLTree._balance_factor(node.left) < 0:
                node.left = AVLTree._left_rotate(node.left)
                return AVLTree._right_rotate(node)
            else:
                return AVLTree._right_rotate(node)
