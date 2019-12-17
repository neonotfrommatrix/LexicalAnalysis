import sys
from Lexer import lexer, process_file

TOKEN = ''
BASE_MEMLOC = 2000
ADDR = 0
STACK = []
JUMPSTACK = []
SYMBOL_TABLE = []
INSTRUCTIONS_TABLE = []
LABEL_QUEUE = []
DATATYPES = ['int', 'float', 'bool', 'boolean']
OPERATORS = ['*', '+', '-', '/']
COMPARATORS = ['<', '>', '==', '>=', '<=', '^=', '!=']
BOOLEANS = ['true', 'false']



class Symbol():
    def __init__(self, ID, MEM, TYPE, VAL=None):
        self.ID = ID
        self.MEM = MEM
        self.TYPE = TYPE
        self.VAL = VAL

class Instruction():
    def __init__(self, IDX, INST, VAL=None):
        self.IDX = IDX
        self.INST = INST
        self.VAL = VAL

def next_token():
    global ADDR
    global TOKEN

    ADDR += 1
    try:
        TOKEN = tokens[ADDR]
    except IndexError:
        return

def get_mem_loc(ID):
    for symbol in SYMBOL_TABLE:
        if symbol.ID == ID:
            return symbol.MEM
    return -1

def get_ID(MEM):
    for symbol in SYMBOL_TABLE:
        if symbol.MEM == MEM:
            return symbol.ID
    return -1

def get_type(ID):
    for symbol in SYMBOL_TABLE:
        if symbol.ID == ID:
            return symbol.TYPE
    raise Exception("Identifier '{}' not found.".format(ID))

def set_mem_loc(MEM, VAL):
    SYMBOL_TABLE[MEM - BASE_MEMLOC].VAL = VAL

def print_instructions():
    # print(*INSTRUCTIONS_TABLE, sep='\n')
    for row in INSTRUCTIONS_TABLE:
        idx = str(row.IDX).ljust(4, ' ')
        inst = str(row.INST).ljust(8, ' ')
        val = '' if row.VAL is None else str(row.VAL).ljust(6, ' ')
        print(idx, inst, val)

def print_symbol_table():
    print('Symbol Table')
    print('Identifier   MemoryLocation  Type')
    for symbol in SYMBOL_TABLE:
        ID = str(symbol.ID).ljust(12, ' ')
        MEM = str(symbol.MEM).ljust(15, ' ')
        TYPE = symbol.TYPE
        print(ID, MEM, TYPE) 

def transform_value(value):
    if value == 'true':
        return 1
    if value == 'false':
        return 0
    if lexer(value) == 'IDENTIFIER':
        MEM = get_mem_loc(value)
        if MEM == -1:
            raise Exception("Identifier '{}' referenced before assignment!".format(value))
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
        VAL = SYMBOL_TABLE[value - BASE_MEMLOC].VAL
        if VAL is None:
            raise Exception("Error: Identifier '{}' was never initialized!".format(get_ID(value)))
        STACK.append(VAL)

    elif instruction == 'POPM': # Pops the value from the top of the stack and stores it at {ML}
        if lexer(value) == 'IDENTIFIER':
            mem = get_mem_loc(value)
            if mem == -1:
                raise Exception("Identifier '{}' referenced before assignment!".format(value))
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

    elif instruction == 'GRT': #Pops two items from the stack and pushes 1 onto TOS if second item is larger otherwise push 0
        first = STACK.pop(-1)
        second = STACK.pop(-1)
        result = 1 if second > first else 0
        STACK.append(result)

    elif instruction == 'LES': # Pops two items from the stack and pushes 1 onto TOS if the second item is smaller than first item otherwise push 0
        first = STACK.pop(-1)
        second = STACK.pop(-1)
        result = 1 if second < first else 0
        STACK.append(result)

    elif instruction == 'EQU': # Pops two items from the stack and pushes 1 onto TOS if they are equal otherwise push 0
        first = STACK.pop(-1)
        second = STACK.pop(-1)
        result = 1 if first == second else 0
        STACK.append(result)

    elif instruction == 'NEQ': # Pops two items from the stack and pushes 1 onto TOS if they are not equal otherwise push 0
        first = STACK.pop(-1)
        second = STACK.pop(-1)
        result = 0 if first == second else 1
        STACK.append(result)

    elif instruction == 'GEQ': # Pops two items from the stack and pushes 1 onto TOS if second item is larger or equal, otherwise push 0
        first = STACK.pop(-1)
        second = STACK.pop(-1)
        result = 1 if second >= first else 0
        STACK.append(result)

    elif instruction == 'LEQ': #Pops two items from the stack and pushes 1 onto TOS if second item is less or equal, otherwise push 0
        first = STACK.pop(-1)
        second = STACK.pop(-1)
        result = 1 if second <= first else 0
        STACK.append(result)


    elif instruction == 'JUMPZ': #{IL - Instruction Location} Pop the stack and if the value is 0 then jump to {IL}
        # TOS = STACK.pop(-1)
        # if not TOS == 0:
        #     return
        JUMPSTACK.append(len(INSTRUCTIONS_TABLE))

    elif instruction == 'LABEL':
        LABEL_QUEUE.append(len(INSTRUCTIONS_TABLE) + 1)
        value = ''
    
    elif instruction == 'JUMP':
        JUMPSTACK.append(len(INSTRUCTIONS_TABLE))
        value = ''

    else:
        raise Exception("Instruction '{}' not recognized!".format(instruction))

    num = str(len(INSTRUCTIONS_TABLE) + 1).ljust(4, ' ')
    instruction = str(instruction).ljust(8, ' ')
    instruction_row = Instruction(num, instruction, value)
    INSTRUCTIONS_TABLE.append(instruction_row)

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
        MEM = get_mem_loc(TOKEN)
        if MEM == -1:
            raise Exception("Identifier '{}' referenced before assignment!".format(TOKEN))
        create_instruction('PUSHM', MEM)
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
            create_instruction('LES')
            # JUMPSTACK.append(len(INSTRUCTIONS_TABLE))
            create_instruction('JUMPZ')
        elif operator == '>':
            create_instruction('GRT')
            # JUMPSTACK.append(len(INSTRUCTIONS_TABLE))
            create_instruction('JUMPZ')
        elif operator == '==':
            create_instruction('EQU')
            # JUMPSTACK.append(len(INSTRUCTIONS_TABLE))
            create_instruction('JUMPZ')
        elif operator == '>=':
            create_instruction('GEQ')
            # JUMPSTACK.append(len(INSTRUCTIONS_TABLE))
            create_instruction('JUMPZ')
        elif operator == '<=':
            create_instruction('LEQ')
            # JUMPSTACK.append(len(INSTRUCTIONS_TABLE))
            create_instruction('JUMPZ')
        elif operator == '^=' or operator == '!=':
            create_instruction('NEQ')
            # JUMPSTACK.append(len(INSTRUCTIONS_TABLE))
            create_instruction('JUMPZ')

def Statement():
    expect_brace = False
    if TOKEN == '{':
        expect_brace = True
        next_token()

    if TOKEN == 'if':
        If()
    elif TOKEN == 'while':
        While()
    elif TOKEN in DATATYPES:
        Declaration()
    elif not TOKEN == ';':
            Assignment()

    if expect_brace:
        next_token()
        if not TOKEN == '}':
            raise Exception("Expected '{}' after TOKEN #{} ({})".format('}', ADDR, TOKEN))
    next_token()

def Back_Patch():
    global INSTRUCTIONS_TABLE
    # if len(LABEL_QUEUE) == len(JUMPSTACK):
    for label in LABEL_QUEUE:
        INSTRUCTIONS_TABLE[JUMPSTACK.pop(-1)].VAL = label
    
def If():
    global ADDR
    global TOKEN
    if TOKEN == 'if':
        next_token()
        if TOKEN == '(':
            next_token()
            Condition(TOKEN)
            if TOKEN == ')':
                next_token()
                Statement()
                if TOKEN == 'ifend':
                    next_token()
                elif TOKEN == 'else':
                    next_token()
                    LABEL_QUEUE.append(len(INSTRUCTIONS_TABLE) + 1)
                    Statement()
                else:
                    raise Exception("Expected 'ifend' or 'else' keyword.")
            else:
                raise Exception("Expected ')' symbol on TOKEN #{} ({})".format(ADDR, TOKEN))
        else:
            raise Exception("Expected '(' symbol on TOKEN #{} ({})".format(ADDR, TOKEN))
    else:
        raise Exception("Expected 'if' statement on TOKEN #{} ({})".format(ADDR, TOKEN))

def While():
    if TOKEN == 'while':
        address = len(INSTRUCTIONS_TABLE) + 1
        create_instruction("LABEL")
        next_token()
        if TOKEN == '(':
            next_token()
            Condition(TOKEN)
            if TOKEN == ')':
                next_token()
                Statement()
                create_instruction("JUMP", address)
                if TOKEN == 'whileend':
                    LABEL_QUEUE.append(len(INSTRUCTIONS_TABLE) + 1)
                    next_token()
                else: 
                    raise Exception("Expected 'whileend' statement on TOKEN #{} ({})".format(ADDR, TOKEN))
            else:
                raise Exception("Expected ')' token on TOKEN #{} ({})".format(ADDR, TOKEN))
        else:
            raise Exception("Expected '(' token on TOKEN #{} ({})".format(ADDR, TOKEN))
    else:
        raise Exception("Expected 'while' statement on TOKEN #{} ({})".format(ADDR, TOKEN))

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
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = 'SampleInput3.txt'
    tokens = process_file(file)
    TOKEN = tokens[ADDR]
    try:
        while ADDR < len(tokens):
            Statement()
        final_instruction = Instruction(len(INSTRUCTIONS_TABLE) + 1, 'END   ')
        INSTRUCTIONS_TABLE.append(final_instruction)
    finally:
        Back_Patch()
        print_instructions()
        print_symbol_table()