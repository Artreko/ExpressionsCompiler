from sys import maxsize

OPERATORS = ['=', '/', '*', '+', '-', '^']
FUNCS = ["sin", "cos", "abs", "sqrt"]
ALLOWED_TYPE = ["operator", "function"]


class LexNode:
    def __init__(self, value="", left=None, right=None,  lex_type=""):
        self.left = left
        self.right = right
        self.value = value
        self.lex_type = lex_type
        if not self.lex_type:
            if self.value in OPERATORS:
                self.lex_type = "operator"
            elif self.value in FUNCS:
                self.lex_type = "function"
            else:
                self.lex_type = "value"

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        return self.value == other.value


class LexTree:
    def __init__(self, tree=None) -> None:
        self.root = tree.root if tree else None

    def __del__(self) -> None:
        self._remove_values(self.root)
        self.root = None

    def _remove_values(self, node: LexNode) -> None:
        if node:
            node.value = 0
            if node.left:
                self._remove_values(node.left)
            if node.right:
                self._remove_values(node.right)

    def add(self, value):
        if self.root is None:
            self.root = LexNode(value)
        else:
            self.add_tree_node(LexNode(value), self.root)

    def add_tree_node(self, node, this):
        if this is None:
            this = node
            return True
        if this.lex_type in ALLOWED_TYPE:
            if this.lex_type == "function":
                if this.left is None:
                    this.left = node
                    return True
                if this.left.lex_type == "operator":
                    return self.add_tree_node(node, this.left)
                else:
                    return False
            if this.left is None:
                this.left = node
                return True
            else:
                if self.add_tree_node(node, this.left):
                    return True
            if this.right is None:
                this.right = node
                return True
            else:
                return self.add_tree_node(node, this.right)
        else:
            return False

    def print_tree(self, node: LexNode, level: int = 0):
        if node is not None and node.value is not None:
            self.print_tree(node.right, level + 1)
            print(' ' * 4 * level + '->', node.value)
            self.print_tree(node.left, level + 1)

    def print_(self, node: LexNode = None):
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

    def post_traverse(self, node: LexNode):
        if node:
            self.post_traverse(node.left)
            self.post_traverse(node.right)
            print(node.value, end=' ')

    @staticmethod
    def get_all_lexemes_list(expr):
        symbols = [s for s in expr]
        words = [""]
        current_word_idx = 0
        for el in symbols:
            if el in ' ':
                if words[current_word_idx]:
                    words.append("")
                    current_word_idx += 1
            elif el in OPERATORS + ['(', ')']:
                if words[current_word_idx]:
                    current_word_idx += 1
                    words.append("")
                words[current_word_idx] += el
                words.append("")
                current_word_idx += 1
            else:
                words[current_word_idx] += el
        if not words[-1]:
            words.pop()
        return words

    @staticmethod
    def get_expression_levels(words):
        levels = [0]
        j = 1
        for el in words:
            levels.append(0)
            if el == '(' or el in OPERATORS + FUNCS:
                levels[j] = levels[j - 1] + 1
            else:
                levels[j] = levels[j - 1] - 1
            j += 1
        return levels[:-1]

    @staticmethod
    def validate(words):
        return any([True if x not in '()' else False for x in words])

    @staticmethod
    def tree_order(words, levels):
        min_level = maxsize
        min_level_idx = -1
        order = []
        for idx, level in enumerate(levels):
            if words[idx] not in '()' and level < min_level:
                min_level = level
                min_level_idx = idx
        # print(min_level, words[min_level_idx])
        order.append(words[min_level_idx])
        # left
        # print("before:", order)
        # print("l:", words[:min_level_idx])

        if LexTree.validate(words[:min_level_idx]):
            order += LexTree.tree_order(words[:min_level_idx], levels[:min_level_idx])
        # right
        # print("r:", words[min_level_idx + 1:])
        if LexTree.validate(words[min_level_idx + 1:]):
            order += LexTree.tree_order(words[min_level_idx + 1:], levels[min_level_idx + 1:])
        # print("after:", order)
        return order

