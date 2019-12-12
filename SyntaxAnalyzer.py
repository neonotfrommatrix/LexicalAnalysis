import Lexer as lx
import sys
Term_Definition = {
    'S': 'Statement', 'E' : 'Expression', 'Q' : 'ExpressionPrime', 'T' : 'Term', 'R' : 'TermPrime', 'F' : 'Factor', 'i' : 'Identifier', '^' : 'epsilon'
}
RULES = [ #Line num - 7
   '<Statement List> -> <Statement> | <Statement> <Statement List>',                                                
   '<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>',
   '<Assign> -> <Identifier> = <Expression>;',
   '<Expression> -> <Term> <ExpressionPrime>',
   '<Term> -> <Factor> <TermPrime>',
   '<Factor> -> - <Primary> | <Primary>',
   '<Primary> -> <Identifier> | <Integer> | <Identifier> ( <IDs> ) | ( <Expression> ) | <Real> | true | false',
   '<Empty> -> Epsilon',
   '<TermPrime> -> * <Factor> <TermPrime> | / <Factor> <TermPrime> | <Empty>',
   '<ExpressionPrime> -> + <Term> <ExpressionPrime> | - <Term> <ExpressionPrime> | <Empty>'
]
def rule(row, col):
    if row == 0 and col == 1:
        print(RULES[1])
        print(RULES[2])
    elif row == 1 and col in [1,6]:
        print(RULES[3])
    elif row == 2:
        print(RULES[7])
        print(RULES[9])
    elif row == 3 and col in [1,6]:
        print(RULES[4])
    elif row == 4:
        print(RULES[7])
        print(RULES[8])
    elif row == 5:
        print(RULES[5])
    else:
        print("none met")

def is_assignment(inp):
    return inp.count('=') > 0

TDPP_Table = [
    #Row    i       +       -       *       /       (       )       $
    ['S',   'i=E',  None,   None,   None,   None,   None,   None,   None],
    ['E',   'TQ',   None,   None,   None,   None,   'TQ',   None,   None],
    ['Q',   None,   '+TQ',  '-TQ',  None,   None,   '^',    '^',    '^'],
    ['T',   'FR',   None,   None,   None,   None,   'FR',   None,   None],
    ['R',   None,   '^',    '^',    '*FR',  '/FR',  '^',    '^',    '^'],
    ['F',   'i',   None,   None,   None,   None,    '(E)',  None,   None]
]
COLS = {
    'row':0, 'i':1, '+':2, '-':3, '*':4, '/':5, '(':6, ')':7, '$':8, ';':8
}
ROWS = {
    'S':0, 'E':1, 'Q':2, 'T':3, 'R':4, 'F':5
}
def process_token(token, STACK):
    # print('stack', STACK)
    if token == '':
        print('Finished!')
        return STACK
    if token == ';':
        # print('\nToken: {}        Lexeme: {}'.format('SEPARATOR', ';' ) )
        return STACK
    if lx.lexer(token) == 'IDENTIFIER':
        compare = 'i'
    else:
        compare = token
    # print('compare',compare)
    print(STACK)
    if STACK[-1] == compare:
        STACK = STACK[:-1]
        if compare == 'i':
            print(RULES[6])
        elif compare == '$':
            print(RULES[7])
        return STACK
    else:
        if compare in COLS.keys():
            col = COLS[compare]
        else:
            col = COLS['i']
        if STACK[-1] == '$':
            print(RULES[7])
            return STACK
        try:
            row = ROWS[STACK[-1]]
        except KeyError:
            print('ERROR on line {} on statement {}. Unexpected character ({}).'.format(statement_no, statement, STACK[-1]))
            sys.exit(1)
        string = TDPP_Table[row][col]
        if string is not None:
            rule(row, col)
            STACK = STACK[:-1]
            if string != '^':
                for letter in reversed(string):
                    STACK.append(letter)
        else:
            print('ERROR on line ({}) on statement ({}). Expected ({})!'.format(statement_no, statement, Term_Definition[TDPP_Table[row][0]]))
            sys.exit(1)

    return process_token(token, STACK)

if __name__ == '__main__':
    global STACK
    if len(sys.argv) < 2:
        print("\nPlease input file name as argument. Usage example: \"python Lexer.py SampleInputFile.txt\" \n")
        # raise Exception

    text = lx.process_file('./SampleInput3.txt')

    text = " ".join(text).replace('$', '').replace(';',';$')

    if text[0:2] == '%%':
        print('\nToken: {}        Lexeme: {}'.format('OPERATOR', '%%' ) )
        print(RULES[0])
        text = text[2:]
    # else:
    #     print('ERROR: \'%%\' Operator not found at beginning of file!')

    STATEMENTS = text.split('$')
    print(STATEMENTS)
    for statement_no, statement in enumerate(STATEMENTS):
        # print('ON STATEMENT', statement)
        # if not statement.endswith(';'):
        #     print('ERROR on line {} on statement ({}). Statemend does not end in \';\'!'.format(statement_no, statement))
        #     sys.exit(1)
        if statement == '':
            print('Finished!')
            continue
        STACK = ['$', 'S']
        for token_no, token in enumerate(statement.split()):
            print('\nToken: {}        Lexeme: {}'.format(lx.lexer(token), token ) )
            STACK = process_token(token, STACK)
        while STACK:
            STACK = process_token('$', STACK)

            
# if __name__ == '__main__':
#     if len(sys.argv) < 2:
#         print("\nPlease input file name as argument. Usage example: \"python Lexer.py SampleInputFile.txt\" \n")
#         raise Exception
#     text = lx.process_file(sys.argv[1])

#     text = "".join(text).replace('$', '').replace(';',';$')

#     if text[0:2] == '%%':
#         print('\nToken: {}        Lexeme: {}'.format('OPERATOR', '%%' ) )
#         print(RULES[0])
#         text = text[2:]
#     # else:
#     #     print('ERROR: \'%%\' Operator not found at beginning of file!')

#     INPUTS = text.split('$')
#     print(INPUTS)
#     for input_no, INPUT in enumerate(INPUTS):
#         input_no += 1
#         if INPUT == '':
#             print('Finished!')
#             break
#         if not INPUT.endswith(';'):
#             print('ERROR on line {} on input ({}). Statemend does not end in \';\'!'.format(input_no, INPUT))
#             sys.exit(1)
#         if INPUT == ';':
#             print('\nToken: {}        Lexeme: {}'.format('SEPARATOR', ';' ) )
#             continue
#         STACK = ['$', 'S']
#         STATEMENT = INPUT
        
#         print('\nToken: {}        Lexeme: {}'.format(lx.lexer(INPUT[0]).split()[0], INPUT[0] ) )
#         while INPUT:
#             if INPUT[0] in '($)' or lx.lexer(INPUT[0]).startswith("OPERATOR"):
#                 compare = INPUT[0]
#             else:
#                 compare = 'i'
#             if STACK[-1] == compare:
#                 STACK = STACK[:-1]
#                 INPUT = INPUT[1:]
#                 if compare == 'i' and not is_assignment():
#                     print(RULES[6])
#                 elif compare == '$':
#                     print(RULES[7])
#                 if len(INPUT):
#                     print('\nToken: {}        Lexeme: {}'.format(lx.lexer(INPUT[0]).split()[0], INPUT[0] ) )
#             else:
#                 char = INPUT[0]
#                 if char in COLS.keys():
#                     col = COLS[char]
#                 else:
#                     col = COLS['i']
#                 if STACK[-1] == '$':
#                     print(RULES[7])
#                     break
#                 try:
#                     row = ROWS[STACK[-1]]
#                 except KeyError:
#                     print('ERROR on line {} on statement {}. Unexpected character ({}).'.format(input_no, STATEMENT, STACK[-1]))
#                     sys.exit(1)
#                 string = TDPP_Table[row][col]
#                 if string:
#                     rule(row, col)
#                     STACK = STACK[:-1]
#                     if string != '^':
#                         for letter in reversed(string):
#                             STACK.append(letter)
#                 else:
#                     print('ERROR on line ({}) on statement ({}). Expected ({})!'.format(input_no, STATEMENT, Term_Definition[TDPP_Table[row][0]]))
#                     sys.exit(1)

