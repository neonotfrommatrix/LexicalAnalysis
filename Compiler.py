from Lexer import lexer

memory_table = []
instructions = []
DATATYPES = ['int', 'float', 'bool', 'boolean']

# New declarations
def is_declaration(statement):
    token_tuples = []
    for token in statement.split():
        try:
            tup = token, lexer(token)
        except:
            return False
        token_tuples.append( tup )
    if token_tuples[0][0] not in DATATYPES or not token_tuples[-1][0] == ';' or len(token_tuples) < 3:
        return False
    for idx, token_tuple in enumerate(token_tuples[1:-1]):
        if idx % 2 == 0:
            if not token_tuple[1] == 'IDENTIFIER':
                return False
        else:
            if not token_tuple[0] == ',':
                return False
    return True

# Assignment
def is_assignment(statement):
    tokens = statement.split()
    if not len(tokens) == 4:
        return False
    if not tokens[-1] == ';':
        return False
    if not lexer(tokens[0]) == 'IDENTIFIER':
        return False
    if not tokens[1] == '=':
        return False
    if lexer(tokens[2]) not in ['IDENTIFIER', 'INTEGER', 'BOOLEAN']:
        return False
    return True
# If

# While