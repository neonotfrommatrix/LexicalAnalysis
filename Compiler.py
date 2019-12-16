from Lexer import lexer, process_file

BASE_MEMLOC = 2000
symbol_table = []
instructions = []
STACK = []
DATATYPES = ['int', 'float', 'bool', 'boolean']
OPERATORS = ['*', '+', '-', '/']
ADDR = 0

class Symbol():
    def __init__(self, ID, MEM, TYPE, VAL=None):
        self.ID = ID
        self.MEM = MEM
        self.TYPE = TYPE
        self.VAL = VAL

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

def resolve_expresion(statement):
    tokens = statement.split()
    left = tokens[0]
    operator = tokens[1]
    right = tokens[2]
    if operator == '+':
        return left + right
    if operator == '-':
        return left - right
    if operator == '*':
        return left * right
    if operator == '/':
        return left / right

def is_expression(statement):
    tokens = statement.split()
    if not tokens[-1] == ';':
        return False

    left = tokens[0]
    if not lexer(left) =='IDENTIFIER' and not lexer(left) == 'INTEGER':
        return False

    operator = tokens[1] 
    if operator not in OPERATORS:
        return False

    right = tokens[2:]
    if len(right) > 2:
        return is_expression(' '.join(right))
    else:
        return lexer(right[0]) == 'INTEGER' or lexer(right[0]) == 'IDENTIFIER'

def is_condition(statement):
    tokens = statement.split()



def table_add(statement):
    tokens = statement.split()
    tuple_type = tokens[0]
    for ID in [token for token in tokens if lexer(token) == 'IDENTIFIER']:
        symbol = Symbol(ID, BASE_MEMLOC + len(symbol_table), tuple_type)
        symbol_table.append(symbol)

def get_mem_loc(ID):
    for symbol in symbol_table:
        if symbol.ID == ID:
            return symbol.MEM
    return -1

def set_mem_loc(MEM, VAL):
    symbol_table[MEM - BASE_MEMLOC].VAL = VAL

def transform_value(value):
    if value == 'true':
        return 1
    if value == 'false':
        return 0
    if lexer(value) == 'IDENTIFIER':
        MEM = get_mem_loc(value)
        if MEM == -1:
            raise Exception('Identifier {} referenced before assignment!'.format(value))
        else:
            return symbol_table[MEM - BASE_MEMLOC].VAL
    try:
        return int(value)
    except:
        raise Exception('Invalid value {}. Expected integer, boolean, or previously assigned identifier!'.format(value))

def create_instruction(instruction, value=''):
    if instruction == 'PUSHI': #Pushes the {Integer Value} onto the Top of the Stack (TOS)
        value = transform_value(value)
        STACK.append(value)

    elif instruction == 'PUSHM': # Pushes the value stored at {ML} onto TOS
        value = symbol_table[get_mem_loc(value) - BASE_MEMLOC].VAL
        STACK.append(value)

    elif instruction == 'POPM': # Pops the value from the top of the stack and stores it at {ML}
        ID = value
        mem = get_mem_loc(ID)
        set_mem_loc(mem, STACK.pop(-1))
        value = mem

    elif instruction == 'STDOUT':
        STACK.pop(-1)
        value = ''

    elif instruction == 'STDIN':
        STACK.append(value)
        value = ''

    elif instruction == 'ADD':
        first = STACK.pop(-1)
        second = STACK.pop(-1)
        STACK.append(transform_value(first) + transform_value(second))
        value = ''

    elif instruction == 'SUB':
        first = STACK.pop(-1)
        second = STACK.pop(-1)
        STACK.append(transform_value(second) - transform_value(first))


    num = str(len(instructions) + 1).ljust(4, ' ')
    instruction = str(instruction).ljust(8, ' ')
    return('{} {} {}'.format(num, instruction, value))

def instruction_assignment(statement):
    tokens = statement.split()
    VAL = tokens[2]
    ID = tokens[0]
    inst_type = 'PUSHM' if lexer(VAL) == 'IDENTIFIER' else 'PUSHI'
    instructions.append(create_instruction(instruction=inst_type, value=VAL))
    instructions.append(create_instruction(instruction='POPM', value=ID))


def print_instructions():
    print(*instructions, sep='\n')

def print_symbol_table():
    print('Symbol Table')
    print('Identifier   MemoryLocation  Type')
    for symbol in symbol_table:
        ID = str(symbol.ID).ljust(12, ' ')
        MEM = str(symbol.MEM).ljust(15, ' ')
        TYPE = symbol.TYPE
        print('{} {} {}'.format(ID, MEM, TYPE))

def create_statements(text):
    statements = []
    statement = []
    idx = 0
    open_paren = False
    open_curly = False
    while idx < len(text):



sample = [
    'int num , nu2m , large$ ;',
    'num = 0 ;',
    'nu2m = 15 ;',
    'boolean hey ;',
    'hey = true ;',
    'hey = false ;'
    ]

while ADDR < len(sample):
    statement = sample[ADDR]
    if is_declaration(statement):
        table_add(statement)
    elif is_assignment(statement):
        instruction_assignment(statement)
    ADDR += 1

print_instructions()
print_symbol_table()
# If
all_stms = ''
for statement in sample:
    all_stms += statement
print(process_file(all_stms, as_string=True))
print(process_file('SampleInput3.txt'))
# While