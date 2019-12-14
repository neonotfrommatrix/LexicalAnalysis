from Lexer import lexer

BASE_MEMLOC = 2000
memory_table = []
instructions = []
STACK = []
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

def table_add(statement):
    tokens = statement.split()
    tuple_type = tokens[0]
    for id in [token for token in tokens if lexer(token) == 'IDENTIFIER']:
        tup = (id, BASE_MEMLOC + len(memory_table), tuple_type)
        memory_table.append(tup)

    # print(memory_table)

def instruction_assignment(statement):
    tokens = statement.split()
    val = tokens[2]
    id = tokens[0]
    if lexer(val) == 'BOOLEAN':
        val = 0 if val == 'false' else 1
    ins_type = 'PUSHI'
    instructions.append('{}    {}    {}'.format(len(instructions) + 1, ins_type, val))
    for tup in memory_table:
        if tup[0] == id:
            val = tup[1]
    instructions.append('{}    {}    {}'.format(len(instructions) + 1, 'POPM', val))

sample = ['int num , nu2m , large$ ;',
        'num = 0 ;',
        'nu2 = 15 ;',
        'boolean hey ;',
        'hey = true ;']

table_add(sample[0])
instruction_assignment(sample[1])
instruction_assignment(sample[2])
instruction_assignment(sample[3])
instruction_assignment(sample[4])

print(*instructions, sep='\n')
print('Symbol Table')
print('Identifier   MemoryLocation  Type')
for tup in memory_table:
    print('{}        {}               {}'.format(tup[0], tup[1], tup[2]))
# If

# While