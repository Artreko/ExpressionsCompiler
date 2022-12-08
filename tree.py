class Node:
    def __init__(self, value=0, left=None, right=None) -> None:
        self.left = left
        self.right = right
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        return self.value == other.value


class Tree:
    def __init__(self, tree=None) -> None:
        self.root = tree.root if tree else None
        self.list_ = []

    def __del__(self) -> None:
        self._remove_values(self.root)
        self.root = None

    def _remove_values(self, node: Node) -> None:
        if node:
            node.value = 0
            if node.left:
                self._remove_values(node.left)
            if node.right:
                self._remove_values(node.right)

    def add(self, value) -> None:
        self.list_.append(value)
        if self.root is None:
            self.root = Node(value)
        else:
            self.add_node(Node(value), self.root)

    def __eq__(self, other) -> bool:
        return self.check(self.root, other.root)

    def check(self, one: Node, two: Node) -> bool:
        x = True
        if one and two:
            if one == two:
                if one.left and two.left:
                    x = self.check(one.left, two.left)
                elif one.left and not two.left:
                    x = False
                elif not one.left and two.left:
                    x = False

                if one.right and two.right:
                    x = self.check(one.right, two.right)
                elif one.right and not two.right:
                    x = False
                elif not one.right and two.right:
                    x = False
            else:
                x = False

        return x

    def add_node(self, node, this) -> None:
        if this is None:
            this = node
        elif node.value < this.value:
            if this.left is None:
                this.left = node
            else:
                self.add_node(node, this.left)
        else:
            if this.right is None:
                this.right = node
            else:
                self.add_node(node, this.right)

    def del_node(self, root: Node, value):
        if value in self.list_:
            self.list_.remove(value)
        if not root:
            return root
        if value < root.value:
            root.left = self.del_node(root.left, value)
        elif value > root.value:
            root.right = self.del_node(root.right, value)
        elif root.left and root.right:
            root.value = self._find_min(root.right).value
            root.right = self.del_node(root.right, root.value)
        else:
            if root.left:
                root = root.left
            elif root.right:
                root = root.right
            else:
                root = None
        return root

    def find_min(self):
        if self.root is None:
            return None
        else:
            return self._find_min(self.root)

    def _find_min(self, node):
        if node.left:
            return self._find_min(node.left)
        else:
            return node

    def find_max(self):
        if self.root is None:
            return None
        else:
            return self._find_max(self.root)

    def _find_max(self, node):
        if node.right:
            return self._find_max(node.right)
        else:
            return node

    def print_(self, node: Node = None):
        node = node if node else self.root
        print(node, end="")
        if node.left or node.right:

            print("(", end="")

            if node.left:
                self.print_(node.left)
            else:
                print("None", end="")

            print(",", end="")

            if node.right:
                self.print_(node.right)
            else:
                print("None", end="")

            print(")", end="")

    def find(self, key):
        if not self.root:
            return None
        else:
            return self._find(key, self.root)

    def _find(self, key, node):
        if not node:
            return None
        elif key < node.value:

            return self._find(key, node.left)
        elif key > node.value:
            return self._find(key, node.right)
        else:
            return node

    def read_file(self, filename):
        file = open(filename, 'r')
        s = file.read().split(' ')
        nodes = list(map(int, s))
        for node in nodes:
            self.add(node)
            self.list_.append(node)
        file.close()

    def write_in_file(self, filename: str) -> None:
        file = open(filename, 'w')
        self.__write(file)
        file.close()

    def preorder_traverse(self, node: Node) -> None:
        if node:
            print(node.value, end='->')
            self.preorder_traverse(node.left)
            self.preorder_traverse(node.right)

    def inf_traverse(self, node: Node):
        if node:
            self.inf_traverse(node.left)
            print(node.value, end='->')
            self.inf_traverse(node.right)

    def post_traverse(self, node: Node):
        if node:
            self.post_traverse(node.left)
            self.post_traverse(node.right)
            print(node.value, end='->')

    def __write(self, file, node=None):
        node = node if node else self.root
        file.write(str(node))
        if node.left or node.right:

            file.write("(")

            if node.left:
                self.__write(file, node.left)
            else:
                file.write("None")

            file.write(",")

            if node.right:
                self.__write(file, node.right)
            else:
                file.write("None")

            file.write(")")

    def print_simple(self, node, level=0):
        if node:
            if self.is_simple(node.value):
                print(node.value, f'lvl({level})')
            self.print_simple(node.left, level + 1)
            self.print_simple(node.right, level + 1)

    @staticmethod
    def is_simple(num):
        if num <= 1:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, num + 1, 2):
            if num % i == 0:
                return num == i

