import re


t = []
exp = []
three = []
operation = ['+', '-', '*', '/', ')']   # значения, при которых уровень уменьшаем
l = 0
c = 0


# inputfile = 'arrr.txt'
# f = open(inputfile, 'r')
#expression = f.read().split()
#f.close()


class Element:
    val = None
    lev = 0

    def __init__(self, el, l):
        self.val = el
        self.level(l)

    def level(self, l):
        if self.val in operation:
            self.lev = l - 1
        else:
            self.lev = l + 1


# вычисляет выражение, содержащееся в тройке
def calc(three, idx):
    global c
    a = float(three[0])
    b = float(three[2])
    c = 0
    exec(f"c = {a}{three[1]}{b}", globals())
    # if three[1] == '+':
    #     c = (a + b) * 1.0
    # elif three[1] == '-':
    #     c = (a - b) * 1.0
    # elif three[1] == '*':
    #     c = (a * b) * 1.0
    # elif three[1] == '/':
    #     c = (a + 0.0) / b
    print(f'T[{idx}] = {three}')


# находим тройку, вычисляем выражение, изменяем массивы t, exp
def find_max(exp, three, idx):
    i = 0
    while i < len(exp):
        maxlev = max(t)
        if t[i] == maxlev:
            j = 0
            three.append(exp[i].val)
            three.append(exp[i+1].val)
            three.append(exp[i+2].val)
            # print(three)
            calc(three, idx)
            print('c =', c)
            # заменяем первый член тройки на ее значение и уменьшаем уровень на 1
            # print('t1 =', t)
            exp[i].val = c
            t[i] = exp[i].lev
            # print('t2 =', t)
            # удаляем скобки, обрамляющие тройку и последние члены тройки
            # del exp[i+3], t[i+3], exp[i+2], t[i+2], exp[i+1], t[i+1], exp[i-1], t[i-1]
            if i == 0:
                del exp[i + 1], exp[i + 1], t[i + 1], t[i + 1]
            else:
                if exp[i + 3].val == ')' and exp[i - 1].val == '(':
                    del exp[i - 1], exp[i], exp[i], exp[i], t[i - 1], t[i], t[i], t[i]
            # print('t3 =', t)
            _exp = []
            for el in exp:
                _exp.append(str(el.val))
            str_exp = ' '.join(_exp)
            # print(str_exp)
            l = 0
            idx = 0
            t_exp = []
            for el in str_exp.split(' '):
                el = Element(el, l)
                l = el.lev
                t[idx] = l
                idx += 1
            # print('t4 =', t)
            i = 0
            break
        else:
            i += 1


def replacing_variables():
    for el in expression.split(" ")[2:]:
        if str.isalnum(el) and not str.isdigit(el):
            if el in dict_variables:
                continue
            dict_variables[el] = input(f'Введите значение переменной {el}: ')


def lexical_analysis():
    print("\nСлужебные символы:")
    for el in expression.split(" "):
        if el in ('=', '+', '-', '*', '/'):
            print(f"{el:<5} : оператор")
        else:
            literals.append(el)

    print("\nЛитералы:")
    for el in literals:
        if not str.isdecimal(el):
            if el in dict_variables and not str.isdecimal(dict_variables[el]):
                print(f"{el:<5} {': Double'}")
            elif el in dict_variables and str.isdecimal(dict_variables[el]):
                print(f"{el:<5} : Int")
            else:
                if el not in ('(', ')'):
                    print(f"{el:<5} {': Double'}")
        else:
            print(f"{el:<5} : Int")


def op_prior(o):
    if o == '*':
        return 4
    elif o == '/':
        return 3
    elif o == '%':
        return 2
    elif o == '+':
        return 1
    elif o == '-':
        return 1


def postfix_form(expr):
    co = []
    op_stack = []
    list_tokens = re.split('[ ]+', expr)
    for i in list_tokens:
        if i.isdigit():
            co.append(int(i))
        elif i in ['*', '/', '%', '+', '-']:
            token_tmp = ''
            if len(op_stack) > 0:
                token_tmp = op_stack[len(op_stack) - 1]
                while (len(op_stack) > 0 and token_tmp != '('):
                    if (op_prior(i) <= op_prior(token_tmp)):
                        co.append(op_stack.pop())
                    else:
                        break
            op_stack.append(i)
        elif i == '(':
            op_stack.append(i)
        elif i == ')':
            token_tmp = op_stack[len(op_stack) - 1]
            while (token_tmp != '('):
                co.append(op_stack.pop())
                token_tmp = op_stack[len(op_stack) - 1]
                if len(op_stack) == 0:
                    raise RuntimeError('В выражении пропущена (')
                if token_tmp == '(':
                    op_stack.pop()
        else:
            co.append(i)

    while (len(op_stack) > 0):
        token_tmp = op_stack[len(op_stack) - 1]
        co.append(op_stack.pop())
        if token_tmp == '(':
            raise RuntimeError('В выражении пропущена )')
    co.pop(1)
    co.append('=')
    return co


if __name__ == '__main__':
    # круг = пи * рад * рад + 8 + 1 - 6 * 4
    expression = "круг = ( пи * ( рад * рад ) ) + ( ( 8 + 1 ) - ( 6 * 4 ) )"
    # f.close()
    service_symbols = []
    literals = []
    dict_variables = {}
    t_idx = 1

    replacing_variables()
    lexical_analysis()
    print("\nПостфискная форма:", *postfix_form(expression), '\n')
    print(*expression.split()[2:], sep='\t')
    # заполняем массивы t, exp
    for el in dict_variables:
        expression = expression.replace(el, str(dict_variables[el]))
    for el in expression.split()[2:]:
        el = Element(el, l)
        l = el.lev
        t.append(l)
        exp.append(el)
    print(*expression.split()[2:], sep='\t')
    print(*t, sep='\t')
    # вычисление выражения
    while len(exp) > 1:
        three = []
        find_max(exp, three, t_idx)
        t_idx += 1
    print(f'{expression.split(" ")[0]} = {exp[0].val}')

