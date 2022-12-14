import lexemes_tree as lt
import sys

my_expression = "S = ((1 / (2 * a * b)) * sin(al * 1)"
# my_expression = "круг = ( пи * ( рад * рад ) ) + ( 8 + 1 ) - ( 6 * 4 )"
# my_expression = "S = c + a * b"
# my_expression = "S = (((1 + 2) * 2) / 6) + 8"

if __name__ == "__main__":
    words = lt.LexTree.get_all_lexemes_list(my_expression)
    only = [el for el in words if el not in lt.FUNCS + lt.OPERATORS + lt.BRACKETS]
    print("Все лексемы без скобок: ")
    print(*only, sep='\t')
    print("Споставление уровней лексем:")
    print(*words, sep="\t")
    levels = lt.LexTree.get_expression_levels(words)
    print(*levels, sep="\t")
    print("Порядок заполнения дерева")
    order = lt.LexTree.tree_order(words, levels)
    print(*order)
    print("Дерево:")
    lex_tree = lt.LexTree()
    lex_tree.build_tree(order)
    lex_tree.print_tree(lex_tree.root)
    print("Постфиксная форма записи выражения:")
    lex_tree.post_traverse(lex_tree.root)
    print()
    print("Введите значения преременной(ых)")
    lex_tree.get_variables_values(lex_tree.root)
    print()
