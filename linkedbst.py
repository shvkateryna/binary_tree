"""
File: linkedbst.py
Author: Ken Lambert
"""
from time import time
import random
from math import log
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
import sys
sys.setrecursionlimit(20000)


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            stone = ""
            if node is not None:
                stone += recurse(node.right, level + 1)
                stone += "| " * level
                stone += str(node.data) + "\n"
                stone += recurse(node.left, level + 1)
            return stone

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentnode = top.left
            while not currentnode.right is None:
                parent = currentnode
                currentnode = currentnode.right
            top.data = currentnode.data
            if parent == top:
                top.left = currentnode.left
            else:
                parent.right = currentnode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemremoved = None
        preroot = BSTNode(None)
        preroot.left = self._root
        parent = preroot
        direction = 'L'
        currentnode = self._root
        while not currentnode is None:
            if currentnode.data == item:
                itemremoved = currentnode.data
                break
            parent = currentnode
            if currentnode.data > item:
                direction = 'L'
                currentnode = currentnode.left
            else:
                direction = 'R'
                currentnode = currentnode.right

        # Return None if the item is absent
        if itemremoved is None: return

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentnode.left is None \
                and not currentnode.right is None:
            liftMaxInLeftSubtreeToTop(currentnode)
        else:

            # Case 2: The node has no left child
            if currentnode.left is None:
                newchild = currentnode.right

                # Case 3: The node has no right child
            else:
                newchild = currentnode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newchild
            else:
                parent.right = newchild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preroot.left
        return itemremoved

    def replace(self, item, newitem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                olddata = probe.data
                probe.data = newitem
                return olddata
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def children(self, top: BSTNode):
        """Generate an iteration of Positions representing p's children."""
        if top.left is not None:
            yield top.left
        if top.right is not None:
            yield top.right

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top: BSTNode):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.left is None and top.right is None:
                return 0
            return 1 + max(height1(c) for c in self.children(top))

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        counter = 0
        for _ in self.inorder():
            counter += 1
        formula = 2 * log(counter + 1, 2) - 1
        return formula > self.height()

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        new_list = []
        for i in self.inorder():
            if low <= i <= high:
                new_list.append(i)
        return new_list


    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        new_abstract = LinkedStack()
        for i in self.inorder():
            new_abstract.push(i)
        self.clear()
        def recurse(new_abstract):
            if len(new_abstract) == 1:
                self.add(new_abstract.pop())
            elif len(new_abstract) == 2:
                self.add(new_abstract.pop())
                self.add(new_abstract.pop())
            else:
                middle = len(new_abstract) // 2
                new_left = LinkedStack()
                new_right = LinkedStack()
                for i, j in enumerate(new_abstract):
                    if i < middle:
                        new_left.push(j)
                    elif i == middle:
                        self.add(j)
                    else:
                        new_right.push(j)
                recurse(new_left)
                recurse(new_right)
        recurse(new_abstract)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        min_item = float('inf')
        for i in self.inorder():
            if i < min_item and i > item:
                min_item = i
        if min_item == float('inf'):
            return None
        return min_item



    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        max_item = float('-inf')
        for i in self.inorder():
            if i > max_item and i < item:
                max_item = i
        if max_item == float('-inf'):
            return None
        return max_item

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        final = []
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                final.append(line.strip())
        sorted_final = sorted(final)
        random_10000 = random.sample(final, 10000)
        final_1 = []
        start_time1 = time()
        for i in sorted_final:
            if i in random_10000:
                final_1.append(i)
        end_time1 = time()
        start_end_1 = end_time1 - start_time1

        tree = LinkedBST()
        for i in sorted_final:
            tree.add_alpha(i)

        start_time2 = time()
        for j in random_10000:
            tree.find_word(j)
        end_time2 = time()
        start_end_2 = end_time2 - start_time2

        tree2 = LinkedBST()
        random2 = random.sample(final, 10000)
        for j in final:
            tree2.add(j)

        start_time3 = time()
        final3 = []
        for i in tree2:
            if i in random2:
                final3.append(i)
        end_time3 = time()
        start_end_3 = end_time3 - start_time3

        tree2.another_rebalance()
        final4 = []
        start_time4 = time()
        for i in tree2:
            if i in random2:
                final4.append(i)
        end_time4 = time()
        start_end_4 = end_time4 - start_time4
        return f'Час пошуку у впорядкованому списку: {start_end_1}\n\
Час пошуку у вигляді бінарного дерева (впорядкований): {start_end_2}\n\
Час пошуку у вигляді бінарного дерева (невпорядкований): {start_end_3}\n\
Час пошуку у вигляді бінарного збалансованого дерева: {start_end_4}'

    def add_alpha(self, item):
        if self._root is None:
            self._root = BSTNode(item)
            node = self._root
        else:
            node = self._root
            while node.right is not None:
                node = node.right
            node.right = BSTNode(item)

    def find_word(self, item):
        node = self._root
        while item != node.data:
            node = node.right
        return node

    def another_rebalance(self):
        """Rebalance without recurse"""
        inorder_list = []
        for i in self.inorder():
            inorder_list.append(i)
        self.clear()
        final = []
        final.append(inorder_list)
        while len(final) != 0:
            temporary = final[0]
            middle = len(temporary) // 2
            if temporary != []:
                self.add(temporary[middle])
            final.pop(0)
            if middle != 0:
                if temporary[:middle] != []:
                    final.append(temporary[:middle])
                if temporary[middle:] != []:
                    final.append(temporary[middle + 1:])





a = LinkedBST()
print(a.demo_bst('words.txt'))