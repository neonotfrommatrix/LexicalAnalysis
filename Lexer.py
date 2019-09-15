
def identifier_fsm(token):
    """
    state machine
    state/input     alpha   num     $      other
        0           1       2       2       2
        (1)         1       1       1       2
        2           2       2       2       2

    """
    transition_function = [
        [1, 2, 2, 2],
        [1, 1, 1, 2],
        [2, 2, 2, 2]
    ]

    current_state = 0
    for character in token:
        if character.isalpha():
            column = 0
        elif character.isdigit():
            column = 1
        elif character == '$':
            column = 2
        else:
            column = 3

        current_state = transition_function[current_state][column]

    return current_state == 1

    
def reals_fsm(token):
    """
    state machine
    state/input     num    dec      other
        0           1       2       4
        1           1       2       4
        2           3       4       4
        (3)         3       4       4
        4           4       4       4

    """
    transition_function = [
        [1, 2, 4],
        [1, 2, 4],
        [3, 4, 4],
        [3, 4, 4],
        [4, 4, 4]
    ]

    current_state = 0
    for character in token:
        if character.isdigit():
            column = 0
        elif character == '.':
            column = 1
        else:
            column = 2

        current_state = transition_function[current_state][column]

    return current_state == 3

def int_fsm(token):
    """
    state machine
    state/input     num       other
        0           1         2
        (1)         1         2
        2           2         2
    """
    transition_function = [
        [1, 2],
        [1, 2],
        [2, 2],
    ]

    current_state = 0
    for character in token:
        if character.isdigit():
            column = 0
        else:
            column = 1

        current_state = transition_function[current_state][column]

    return current_state == 1

def lexer(token):           #defines a function
    separators = "'(){}[],.:;!"
    if token in separators or token == ' ':
        return "SEPARATOR"

    operators = ["*", "+", "-", "=", "/", "<", ">", "<=", ">=", "%"]
    if token in operators:
        return "OPERATOR"

    keywords = ["int", "float", "bool", "if", "else", "then", "endif", "while", "whileend", "do", "doend", "for", "forend", "input", "output", "and", "or", "function"]
    if token in keywords:
        return "KEYWORD"
    
    is_identifier = identifier_fsm(token)

    if is_identifier:
        return "IDENTIFIER"

    is_real = reals_fsm(token)

    if is_real:
        return "REAL     "

    is_int = int_fsm(token)

    if is_int:
        return "INTEGER "

test = "while ( fahr < upper ) a = 23.00 whileend while ( cr < lower ) b = 14 whileend"
for word in test.split():
    print (lexer(word), "\t", word)