import lexemes_tree as lt
import sys

my_expression = "S = ((1 / (2 * a * b)) * sin(alpha * 4)"
# my_expression = "круг = ( пи * ( рад * рад ) ) + ( 8 + 1 ) - ( 6 * 4 )"
# my_expression = "S = c + a * b"
# my_expression = "S = (((1 + 2) * 2) / 6) + 8"

OPERATORS = ['=', '/', '*', '+', '-', '^']
FUNCS = ["sin", "cos", "abs", "sqrt"]


if __name__ == "__main__":
    words = lt.LexTree.get_all_lexemes_list(my_expression)
    print(*words, sep="\t")
    levels = lt.LexTree.get_expression_levels(words)
    print(*levels, sep="\t")
    order = lt.LexTree.tree_order(words, levels)
    """
    удалить скобки и их уровни 
    минимальный уровень в верху дереваs
    """
    #lex = [el for el in words if el not in '()']
    # print(lex)
    lex_tree = lt.LexTree()
    for el in order:
        lex_tree.add(el)

    lex_tree.print_tree(lex_tree.root)
    lex_tree.post_traverse(lex_tree.root)
    print()
