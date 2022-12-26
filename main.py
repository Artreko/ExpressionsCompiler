from math import *
import lexemes_tree as lt

my_expression = "S = ((1 / 2) * (a * b)) * sin(al)"


def print_dict(my_dict):
    for key, value in my_dict.items():
        print(f'{key}: {value}')


def valid_parentheses(lexemes):
    open_counter = 0
    close_counter = 0
    for sym in lexemes:
        if sym == '(':
            open_counter += 1
        if sym == ')':
            close_counter += 1
        if close_counter > open_counter:
            return False
    return open_counter == close_counter


def get_tetrads(corder):
    tetr_dict = {}
    t_idx = 1
    last_op = 0
    while len(corder) > 1:
        for i in range(len(corder)):
            if corder[i] in lt.OPERATORS + lt.FUNCS:
                last_op = i
        tetr_dict[f'T{t_idx}'] = []
        if corder[last_op] in lt.FUNCS:
            tetr_counter = 2
        else:
            tetr_counter = 3
        for _ in range(tetr_counter):
            tetr_dict[f'T{t_idx}'].append(corder.pop(last_op))
        corder.insert(last_op, f'T{t_idx}')
        t_idx += 1
    return tetr_dict


def get_value(var, tetr_dict, var_dict):
    if var in tetr_dict:
        return tetr_dict[var]
    if var in var_dict:
        var = var_dict[var]
    if var.isdecimal():
        return int(var)
    return float(var)


def calculate_tetrad_valuers(tetr_dict, var_dict):
    for t_name in tetr_dict:
        op = tetr_dict[t_name][0]
        params = tetr_dict[t_name][1:]
        match op:
            case 'sin':
                tetr_dict[t_name] = sin(get_value(params[0], tetr_dict, var_dict))
            case 'abs':
                tetr_dict[t_name] = abs(get_value(params[0], tetr_dict, var_dict))
            case 'cos':
                tetr_dict[t_name] = cos(get_value(params[0], tetr_dict, var_dict))
            case 'sqrt':
                tetr_dict[t_name] = sqrt(get_value(params[0], tetr_dict, var_dict))
            case '+':
                tetr_dict[t_name] = \
                    get_value(params[0], tetr_dict, var_dict) + get_value(params[1], tetr_dict, var_dict)
            case '-':
                tetr_dict[t_name] = \
                    get_value(params[0], tetr_dict, var_dict) - get_value(params[1], tetr_dict, var_dict)
            case '/':
                tetr_dict[t_name] = \
                    get_value(params[0], tetr_dict, var_dict) / get_value(params[1], tetr_dict, var_dict)
            case '*':
                tetr_dict[t_name] = \
                    get_value(params[0], tetr_dict, var_dict) * get_value(params[1], tetr_dict, var_dict)
            case '^':
                tetr_dict[t_name] = \
                    get_value(params[0], tetr_dict, var_dict) ** get_value(params[1], tetr_dict, var_dict)
            case '=':
                tetr_dict[t_name] = get_value(params[1], tetr_dict, var_dict)
            case _:
                pass


if __name__ == "__main__":
    words = lt.LexTree.get_all_lexemes_list(my_expression)
    if not valid_parentheses(words):
        raise RuntimeError("Не верно расставлены скобки!")
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
    order_copy = order.copy()
    tetrads_dict = get_tetrads(order_copy[2:])

    tetrads_values = tetrads_dict.copy()
    calculate_tetrad_valuers(tetrads_values, lex_tree.variables_dict)

    print()
    print("Операторы")
    for word in words:
        if word in lt.OPERATORS:
            print(word)
    print("Функции")
    for word in words:
        if word in lt.FUNCS:
            print(word)
    result_value = list(tetrads_values.values())[-1]
    print("Литералы")
    for var, value in lex_tree.variables_dict.items():
        print(f'{var}: {"int" if "." not in value else "float"}')
    for word in words:
        if word not in lt.FUNCS + lt.OPERATORS + lt.BRACKETS and not word.isalnum():
            print(f'{word}: {"int" if "." not in word else "float"}')
    print("Тетрады")
    print_dict(tetrads_dict)
    print("Значение тетрад")
    print_dict(tetrads_values)
    print("Результат")
    print(f'{words[0]} = {result_value}')

