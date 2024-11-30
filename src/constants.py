from typing import Dict, Union
from src.utils.die import Die
import re


def tokenize(expression):
    tokens = re.findall(r'\d+|\+|\-|\*|\/', expression)
    return tokens


def infix_to_postfix(tokens):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operators = []

    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token in precedence:
            while (operators and operators[-1] in precedence and
                   precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)

    while operators:
        output.append(operators.pop())

    return output


def evaluate_postfix(postfix):
    stack = []

    for token in postfix:
        if token.isdigit():
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a // b)  # Integer (floor) division

    return stack[0]


def evaluate_expression(expression):
    tokens = tokenize(expression)
    postfix = infix_to_postfix(tokens)
    result = evaluate_postfix(postfix)
    return result


def roll_stats():
    die = Die(6)
    stats = []
    for _ in range(7):
        stats.append(sum(sorted(die.roll(rolls=4, summed=False))[1:]))

    stats.sort()
    stats = stats[1:]

    return stats

def print_distribution(distribution: Dict[Union[int, float], Union[int, float]], step_size: Union[float, int] = 1):
    min_val = min(distribution.keys())
    max_val = max(distribution.keys())

    for val in range(min_val, max_val + 1):
        print(val, end='|')
        if val in distribution.keys():
            i = step_size
            while i < distribution[val]:
                print('-', end='')
                i += step_size

        print()

proficiency_bonus = [None,
                     2, 2, 2, 2,  # 1st-4th
                     3, 3, 3, 3,  # 5th-8th
                     4, 4, 4, 4,  # 9th-12th
                     5, 5, 5, 5,  # 13th-16th
                     6, 6, 6, 6]  # 17th-20th

ability_modifier = [None, -5,  # 1
                    -4, -4,    # 2-3
                    -3, -3,    # 4-5
                    -2, -2,    # 6-7
                    -1, -1,    # 8-9
                     0,  0,    # 10-11
                     1,  1,    # 12-13
                     2,  2,    # 14-15
                     3,  3,    # 16-17
                     4,  4,    # 18-19
                     5,  5,    # 20-21
                     6,  6,    # 22-23
                     7,  7,    # 24-25
                     8,  8,    # 26-27
                     9,  9,    # 28-29
                     10]       # 30

