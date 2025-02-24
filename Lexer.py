import sys

def process_file(file_name, as_string=False):
    #all lines into a string from text file
    if not as_string:
        with open(file_name) as f:
            text = f.read()
    else:
        text = file_name
    #single-char words
    separators = ['\'', '(', ')', '{', '}', '[', ']', ',', '.', ':', ';']

    # single-line comments
    single_line_comments = ['#', '//', '!', '%%']

    # Break into lines
    text = text.split('\n')

    # Remove single-line comments
    no_comment_text = []
    for line in text:
        valid = True
        for token in single_line_comments:
            if line.startswith(token):
                valid = False
        if valid:
            no_comment_text.append(line)
    text = ' '.join(no_comment_text)

    # Remove multi-lines
    text = " ".join(text.split())

    # Split separators from other words
    new_text = ''
    identifier = False
    for idx, char in enumerate(text):
        if char.isalpha():
            identifier = True
            new_text += char
        elif char == '$' and identifier:
            new_text += char
            identifier = False
        elif char.isnumeric() and identifier:
            new_text += char
        else:
            new_text += ' ' + char + ' '

    text = new_text.split()

    double_ops = ['!', '=', '>', '<', '^', '*', '+', '-', '/', '%']
    # Merge double operators

    for idx in range(1, len(text)):
        if text[idx] == '=' and text[idx -1] in double_ops:
            text[idx - 1] = text[idx - 1] + '='
            text[idx] = '@@'
    # Remove @@ tokens
    text = ' '.join(text)
    text = text.replace('@@', '')
    text = text.split()
    
    return text


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
    token = str(token)
    separators = "'(){}[],.:;!$"
    if token in separators or token == ' ':
        return "SEPARATOR"

    operators = ["*", "+", "-", "=", "/", "<", ">", "<=", ">=", "%", "=="]
    if token in operators:
        return "OPERATOR"

    keywords = ["int", "float", "bool", "boolean", "if", "else", "then", "endif", "while", "whileend", "do", "doend", "for", "forend", "input", "output", "and", "or", "function"]
    if token in keywords:
        return "KEYWORD"
    
    booleans = ['true', 'false']
    if token in booleans:
        return "BOOLEAN"

    is_identifier = identifier_fsm(token)

    if is_identifier:
        return "IDENTIFIER"

    is_real = reals_fsm(token)

    if is_real:
        return "REAL"

    is_int = int_fsm(token)

    if is_int:
        return "INTEGER"
    
    print("Error: {} is not recognized".format(token))
    raise Exception

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\nPlease input file name as argument. Usage example: \"python Lexer.py SampleInputFile.txt\" \n")
        raise Exception

    text = process_file(sys.argv[1])
    output_string = ''
    print("TOKEN          Lexemes\n")
    output_string += "TOKEN          Lexemes\n"
    for word in text:
        if not word:
            continue
        token = lexer(word).ljust(15, ' ')
        output_string += token + ' ' + word + '\n'
        print (token, word)

    with open("output.txt", 'w') as f:
        f.write(output_string)
        #
