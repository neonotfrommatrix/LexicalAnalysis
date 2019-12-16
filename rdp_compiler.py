from Lexer import lexer, process_file
TOKEN = ''
BASE_MEMLOC = 2000
ADDR = 0
STACK = []
SYMBOL_TABLE = []
INSTRUCTIONS_TABLE = []
DATATYPES = ['int', 'float', 'bool', 'boolean']
OPERATORS = ['*', '+', '-', '/']
COMPARATORS = ['<', '>']
BOOLEANS = ['true', 'false']


class Symbol():
    def __init__(self, ID, MEM, TYPE, VAL=None):
        self.ID = ID
        self.MEM = MEM
        self.TYPE = TYPE
        self.VAL = VAL

def next_token():
    global ADDR
    global TOKEN

    ADDR += 1
    TOKEN = tokens[ADDR]

def get_mem_loc(ID):
    for symbol in SYMBOL_TABLE:
        if symbol.ID == ID:
            return symbol.MEM
    return -1
def get_type(ID):
    for symbol in SYMBOL_TABLE:
        if symbol.ID == ID:
            return symbol.TYPE
    raise Exception("Identifier '{}' not found.".format(ID))

def set_mem_loc(MEM, VAL):
    SYMBOL_TABLE[MEM - BASE_MEMLOC].VAL = VAL

def print_instructions():
    print(*INSTRUCTIONS_TABLE, sep='\n')

def print_symbol_table():
    print('Symbol Table')
    print('Identifier   MemoryLocation  Type')
    for symbol in SYMBOL_TABLE:
        ID = str(symbol.ID).ljust(12, ' ')
        MEM = str(symbol.MEM).ljust(15, ' ')
        TYPE = symbol.TYPE
        print('{} {} {}'.format(ID, MEM, TYPE))  

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
            return SYMBOL_TABLE[MEM - BASE_MEMLOC].VAL
    try:
        return int(value)
    except:
        raise Exception('Invalid value {}. Expected integer, boolean, or previously assigned identifier!'.format(value))

def create_instruction(instruction, value=None):
    if instruction == 'PUSHI': #Pushes the {Integer Value} onto the Top of the Stack (TOS)
        value = transform_value(value)
        STACK.append(value)

    elif instruction == 'PUSHM': # Pushes the value stored at {ML} onto TOS
        if lexer(value) == 'IDENTIFIER':
            value = get_mem_loc(value)
        value = SYMBOL_TABLE[value - BASE_MEMLOC].VAL
        STACK.append(value)

    elif instruction == 'POPM': # Pops the value from the top of the stack and stores it at {ML}
        if lexer(value) == 'IDENTIFIER':
            mem = get_mem_loc(value)
        else:
            mem = value
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
        value = ''

    elif instruction == 'MUL':
        first = STACK.pop(-1)
        second = STACK.pop(-1)
        STACK.append(transform_value(second) * transform_value(first))
        value = ''

    elif instruction == 'DIV':
        first = STACK.pop(-1)
        second = STACK.pop(-1)
        STACK.append(transform_value(second) / transform_value(first))
        value = ''


    num = str(len(INSTRUCTIONS_TABLE) + 1).ljust(4, ' ')
    instruction = str(instruction).ljust(8, ' ')
    INSTRUCTIONS_TABLE.append('{} {} {}'.format(num, instruction, value))

def add_symbol(TYPE):
    # Check if valid ID
    if not lexer(TOKEN) == 'IDENTIFIER':
        raise Exception("Invalid Identifier on TOKEN #{} ({})".format(ADDR, TOKEN))
    # Check if already exists
    for symbol in SYMBOL_TABLE:
        if symbol.ID == TOKEN:
            raise Exception("Identifier {} already previously declared.".format(TOKEN))
    
    SYMBOL_TABLE.append(Symbol(TOKEN, BASE_MEMLOC + len(SYMBOL_TABLE), TYPE))

def Expression(ID):
    Term(ID)
    ExpressionPrime(ID)

def ExpressionPrime(ID):
    if TOKEN == '+':
        next_token()
        Term(ID)
        create_instruction('ADD')
        ExpressionPrime(ID)
    elif TOKEN == '-':
        next_token()
        Term(ID)
        create_instruction('SUB')
        ExpressionPrime(ID)

def Term(ID):
    Factor(ID)
    TermPrime(ID)

def TermPrime(ID):
    if TOKEN == '*':
        next_token()
        Factor(ID)
        create_instruction('MUL')
        TermPrime(ID)
    elif TOKEN == '/':
        next_token()
        Factor(ID)
        create_instruction('DIV')
        TermPrime(ID)

def Factor(ID):
    if lexer(TOKEN) == 'IDENTIFIER':
        create_instruction('PUSHM', get_mem_loc(TOKEN))
    else:
        value = transform_value(TOKEN)
        create_instruction('PUSHI', value)
    next_token() 

def Condition(ID):
    Expression(ID)
    if TOKEN in COMPARATORS:
        operator = TOKEN
        next_token()
        Expression(ID)
        if operator == '<':
            return
def Statement():
    pass
    
def If():
    global ADDR
    global TOKEN
    if TOKEN == 'if':
        address = ADDR
        next_token()
        if TOKEN == '(':
            next_token()
            Condition(TOKEN)
            if TOKEN == ')':
                next_token()
                Statement()
            else:
                raise Exception("Expected ')' symbol on TOKEN #{} ({})".format(ADDR, TOKEN))
        else:
            raise Exception("Expected '(' symbol on TOKEN #{} ({})".format(ADDR, TOKEN))
    else:
        raise Exception("Expected 'if' statement on TOKEN #{} ({})".format(ADDR, TOKEN))

def Assignment():
    global ADDR
    global TOKEN

    if lexer(TOKEN) == 'IDENTIFIER':
        ID = TOKEN
        next_token()
        if TOKEN == '=':
            next_token()
            Expression(ID)
            create_instruction('POPM', ID)
    else:
        raise Exception("Expected IDENTIFIER on TOKEN #{} ({})".format(ADDR, TOKEN))

def Declaration():
    global ADDR
    global TOKEN

    if TOKEN in DATATYPES:
        TYPE = TOKEN
        next_token()
        add_symbol(TYPE)
        next_token()
        if TOKEN == ',':
            TOKEN = TYPE
            Declaration()
        elif TOKEN == ';':
            return
        else:
            raise Exception("Expected ending ';' or a ',' followed by additional declarations.")

    else:
        raise Exception("Expected a datatype on TOKEN #{} ({})".format(ADDR, TOKEN)) 




if __name__ == '__main__':
    tokens = process_file('SampleInput3.txt')
    TOKEN = tokens[ADDR]
    print(tokens)
    try:
        while ADDR < len(tokens):
            if TOKEN == 'if':
                If()
            elif TOKEN == 'while':
                pass
            elif TOKEN in DATATYPES:
                Declaration()
            elif not TOKEN == ';':
                    Assignment()
            next_token()
    finally:
        print_instructions()
        print_symbol_table()