import sys
import ast
import warnings

import ply.yacc as yacc

import lex
import nodes
from errors import ParseError

tokens = lex.tokens
precedence = (
    ('left', 'EQ', 'NEQ', 'LT', 'LTEQ', 'GT', 'GTEQ'),
    ('left', 'AND', 'OR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'UMINUS', 'NOT'),
)

# Symbol Table

symbol_table = {
    # Example entries
    # 'myvar' : int
    # 'myfunc' : {
    #   'type' : list
    #   'symbols' : sub_symbol_table
    # }
}
scope_stack = []
symbol_stack = [[]] # Easy way to implement all_names()

def reset_symbol_table():
    global symbol_table, scope_stack, symbol_stack
    symbol_table = {}
    scope_stack = []
    symbol_stack = [[]]

def get_table(scope_stack):
    """Internal function to walk symbol_table with scope_stack."""
    return reduce(lambda d, k: d[k]['symbols'], scope_stack, symbol_table)

def all_names():
    """Get all identifiers visible in the current scope."""
    return [var for scope in symbol_stack for var in scope]

def local_names():
    """Get all identifiers in the local scope."""
    return get_table(scope_stack).keys()

def get_type(var_name):
    """Get an identifier's type."""
    for i in range(len(scope_stack) + 1):
        subtable = get_table(scope_stack if i is 0 else scope_stack[:-i])
        if var_name in subtable:
            return subtable[var_name]['type'] if type(subtable[var_name]) is dict else subtable[var_name]

def add_symbol(var_name, var_type):
    """Add an identifier in the local scope."""
    symbol_stack[-1].append(var_name)
    get_table(scope_stack)[var_name] = var_type

def push_scope(scope_name, scope_type=None):
    get_table(scope_stack)[scope_name] = {
        'type': scope_type, # Return type for function scopes, etc.
        'symbols': {}
    }
    scope_stack.append(scope_name)
    symbol_stack.append([])

def pop_scope():
    scope_stack.pop()
    symbol_stack.pop()

# Parsing Rules

def p_program(p):
    """program : code_block
    """
    p[0] = ast.Module(p[1])

def p_code_block(p):
    """code_block : statement
                  | code_block statement
    """
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 3:
        p[0] = p[1] + ([p[2]] if p[2] is not None else [])

def p_statement(p):
    """statement : NEWLINE
                 | initialization NEWLINE
                 | assignment NEWLINE
                 | iteration
                 | selection_statement
                 | machine
                 | function_def
                 | hoot
    """
    if p[1] == "\n":
        p[0] = None
    else:
        p[0] = p[1]


# Python only wraps an expression with Expr when it is its own statement
def p_statement_expression(p):
    """statement : expression NEWLINE
        """
    p[0] = p[1] if type(p[1]) is ast.Print else ast.Expr(value=p[1])


def p_hoot(p):
    """hoot : HOOT LPAREN RPAREN NEWLINE
    """
    p[0] = ast.Print(dest=None, values=[
                                    ast.Str(s='\x07'),
                                    ], nl=True)


def p_expression(p):
    """expression : function_call
                  | arithmetic_expression
                  | comparison_expression
                  | boolean_expression
                  | unary_expression
                  | string
                  | number
                  | bool
                  | variable_load
                  | list
                  | input
    """
    p[0] = p[1]

def p_input(p):
    """input : INPUT LPAREN string RPAREN
        """
    p[0] = ast.Call(func=ast.Name(id='raw_input', ctx=ast.Load()), args=[
                                                             p[3],
                                                             ], keywords=[], starargs=None, kwargs=None)

def p_arithmetic_expression(p):
    """arithmetic_expression : expression PLUS expression
                             | expression MINUS expression
                             | expression TIMES expression
                             | expression DIVIDE expression
                             | expression MODULO expression
    """
    operators = {
        '+': ast.Add(),
        '-': ast.Sub(),
        '*': ast.Mult(),
        '/': ast.Div(),
        '%': ast.Mod(),
    }
    p[0] = ast.BinOp(
        left=p[1],
        op=operators[p[2]],
        right=p[3])

def p_comparison_expression(p):
    """comparison_expression : expression EQ expression
                             | expression NEQ expression
                             | expression LT expression
                             | expression LTEQ expression
                             | expression GT expression
                             | expression GTEQ expression
    """
    operators = {
        '==': ast.Eq(),
        '!=': ast.NotEq(),
        '<': ast.Lt(),
        '<=': ast.LtE(),
        '>': ast.Gt(),
        '>=': ast.GtE(),
    }
    p[0] = ast.Compare(
        left=p[1],
        ops=[operators[p[2]]],
        comparators=[p[3]])

def p_boolean_expression(p):
    """boolean_expression : expression AND expression
                          | expression OR expression

    """
    if p[2] == 'and':
        p[0] = ast.BoolOp(op=ast.And(), values=[p[1], p[3]])
    else:
        p[0] = ast.BoolOp(op=ast.Or(), values=[p[1], p[3]])

def p_unary_expression(p):
    """unary_expression : MINUS expression %prec UMINUS
                        | NOT expression
    """

    if p[1] == 'not':
        p[0] = ast.UnaryOp(op=ast.Not(), operand=p[2])
    else:
        p[0] = ast.UnaryOp(op=ast.USub(), operand=p[2])


def p_iteration(p):
    """iteration : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE
                 | FOR variable_store IN variable_load LBRACE statement_list RBRACE
    """

    if p[1] == 'while':
        p[0] = ast.While(p[3], p[6], [])
    elif p[1] == 'for':
        if p[2] not in all_names():
            warnings.warn("%s not declared before for loop!" % (p[2].id,), ParseError)
        p[2].type = get_type(p[2].id)
        p[0] = ast.For(p[2], p[4], p[6], [])

def p_selection_statement(p):
    """selection_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE
                           | IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
    """

    if len(p) == 8:
        p[0] = ast.If(p[3], p[6], [])
    else:
        p[0] = ast.If(p[3], p[6], p[10])

def p_statement_list(p):
    """statement_list : statement_list_item
                      | statement_list_item statement_list
    """

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] is not None:
            
            if p[2] is None:
                p[0] = p[1]

            elif type(p[2]) == list and type(p[1]) == list:
                p[0] = p[2] + p[1]

            elif type(p[2]) == list and type(p[1]) != list:
                p[0] = p[2]
                p[0].append(p[1])

            elif type(p[2]) != list and type(p[1]) == list:
                p[0] = p[1]
                p[0].append(p[2])

            else:
                p[0] = [p[2]]
                p[0].append(p[1])


#            if type(p[1]) == list:
#                p[0] = p[1] + ([p[2]] if p[2] is not None else [])
#            else:
#                p[0] = [p[1]] + ([p[2]] if p[2] is not None else [])

        else:
            if p[2] is None:
                p[0] = p[1]

            elif type(p[2]) == list:
                p[0] = p[2]

            else:
                p[0] = [p[2]]



def p_statement_list_item(p):
    """statement_list_item : NEWLINE
                           | initialization NEWLINE
                           | assignment NEWLINE
                           | iteration
                           | selection_statement
                           | hoot
    """
    if p[1] == "\n":
        p[0] = None
    else:
        p[0] = p[1]

def p_statement_list_item_expression(p):
    """statement_list_item : expression NEWLINE
    """
    p[0] = p[1] if type(p[1]) is ast.Print else ast.Expr(value=p[1])

def p_function_def(p):
    """function_def : type NAME new_scope LPAREN params_def_list RPAREN LBRACE func_statement_list RBRACE
                    | void NAME new_scope LPAREN params_def_list RPAREN LBRACE func_statement_list RBRACE
    """
    p[0] = ast.FunctionDef(name=p[2], args=ast.arguments(args=p[5], vararg=None, kwarg=None, defaults=[]), body=p[8], decorator_list=[], type=p[1])
    pop_scope()

def p_func_statement_list(p):
    """func_statement_list : func_statement_list_item
                           | func_statement_list_item func_statement_list
    """

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] is not None:

            if p[2] is None:
                p[0] = p[1]
            
            elif type(p[2]) == list and type(p[1]) == list:
                p[0] = p[2] + p[1]
        
            elif type(p[2]) == list and type(p[1]) != list:
                p[0] = p[2]
                p[0].append(p[1])
                    
            elif type(p[2]) != list and type(p[1]) == list:
                p[0] = p[1]
                p[0].append(p[2])
        
            else:
                p[0] = [p[2]]
                p[0].append(p[1])



#            if type(p[1]) == list:
#                p[0] = p[1] + ([p[2]] if p[2] is not None else [])
#            else:
#                p[0] = [p[1]] + ([p[2]] if p[2] is not None else [])
        else:

            if p[2] is None:
                p[0] = p[1]

            elif type(p[2]) == list:
                p[0] = p[2]

            else:
                p[0] = [p[2]]


def p_func_statement_list_item(p):
    """func_statement_list_item : NEWLINE
                                | initialization NEWLINE
                                | assignment NEWLINE
                                | iteration
                                | selection_statement
                                | hoot
                                | return_stmt
    """
    
    if p[1] == "\n":
        p[0] = None
    else:
        p[0] = p[1]

def p_func_statement_list_item_expression(p):
    """func_statement_list_item : expression NEWLINE
    """
    p[0] = p[1] if type(p[1]) is ast.Print else ast.Expr(value=p[1])

def p_return_statement(p):
    """return_stmt : RETURN NEWLINE
                   | RETURN expression NEWLINE
        
        
    """
    if len(p) == 3:
        p[0] = ast.Return(value=None)
    else:
        p[0] = ast.Return(value=p[2])


def p_params_def_list(p):
    """params_def_list : params_def
                       | params_def COMMA params_def_list

    """
    if len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[0] = list(p[3]).insert(0, p[1])

def p_params_def(p):
    """params_def : type NAME
                  |
    """
    if len(p) != 1:
        p[0] = ast.Name(id=p[2], ctx=ast.Param(), type=p[1])

def p_function_call(p):
    """function_call : PRINT LPAREN expression RPAREN
                     | variable_load LPAREN parameters RPAREN
                     | variable_load DOT NAME LPAREN parameters RPAREN
                     | variable_load DOT NAME
                     | variable_load LBRACK LIT_INT RBRACK

    """
    if p[1] == 'print':
        p[0] = ast.Print(None, [p[3]], True)
    elif len(p) == 4:
        p[0] = ast.Attribute(value=p[1], attr=p[3], ctx=ast.Load())
    elif len(p) == 7:
        p[0] = ast.Call(func=ast.Attribute(value=p[1], \
            attr=p[3], ctx=ast.Load()), args=p[5], keywords=[], starargs=None, kwargs=None)
    elif len(p) == 5:
        if p[2] == '[':
            p[0] = ast.Subscript(value=p[1], \
                slice=ast.Index(value=ast.Num(n=int(p[3]))), ctx=ast.Load())
        elif p[2] == '(':
            p[0] = ast.Call(func=p[1], \
                args=p[3], keywords=[], starargs=None, kwargs=None)
        # Owl doesn't have keyword arguments, *args, or *kwargs


def p_parameters(p):
    """parameters    : expression
                     | expression COMMA parameters
    """
    # How to have one list and add all parameters to it across multiple reductions?
    #i.e. test(1, 2, 3, 4, 5...)
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        tmp = list(p[3])
        tmp.insert(0, p[1])
        p[0] = tmp

def p_initialization(p):
    """initialization : type variable_store EQUAL expression
                      | type variable_store
    """
    # Initialization adds a new variable name to the symbol table
    if p[2].id in local_names():
        warnings.warn("%s has been declared twice!" % (p[2].id,), ParseError)
    add_symbol(p[2].id, p[1])

    if len(p) == 3:
        # this is for default initialization
        if p[1] == int:
            p[0] = ast.Assign([p[2]], ast.Num(0), type=p[1])
        elif p[1] == bool:
            p[0] = ast.Assign([p[2]], ast.Name("False", ast.Load()), type=p[1])
        elif p[1] == float:
            p[0] = ast.Assign([p[2]], ast.Num(0), type=p[1])
        elif p[1] == str:
            p[0] = ast.Assign([p[2]], ast.Str(""), type=p[1])
        elif p[1] == list:
            p[0] = ast.Assign([p[2]], ast.List([], ast.Load()), type=p[1]) #check correctness
        else:
            warnings.warn("%s Initialization error" % (str(p[1]),), ParseError)
    else:
          #add type checking here
          p[0] = ast.Assign([p[2]], p[4], type=p[1])

def p_assignment(p):
    """assignment : NAME EQUAL expression
                  | NAME PEQUAL expression
                  | NAME MEQUAL expression
                  | NAME TEQUAL expression
                  | NAME DEQUAL expression
    """
    operators = {
        '=' : ast.Eq(),
        '+=': ast.Add(),
        '-=': ast.Sub(),
        '*=': ast.Mult(),
        '/=': ast.Div(),
    }

    if p[2] == '=':
        p[0] = ast.Assign(targets=[ast.Name(id=p[1], ctx=ast.Store())], value=p[3])
    else:
        p[0] = ast.AugAssign(target=ast.Name(id=p[1], ctx=ast.Store()),
        op=operators[p[2]], value=p[3])

def p_void(p):
    """void : VOID
    """
    p[0] = None

def p_type(p):
    """type : INT
            | BOOL
            | FLOAT
            | STRING
            | LIST
    """
    if p[1] == 'int':
        p[0] = int
    elif p[1] == 'bool':
        p[0] = bool
    elif p[1] == 'float':
        p[0] = float
    elif p[1] == 'string':
        p[0] = str
    elif p[1] == 'list':
        p[0] = list
  
def p_number_int(p):
    """number : LIT_INT
    """
    p[0] = ast.Num(int(p[1]))

def p_number_float(p):
    """number : LIT_FLOAT
    """
    p[0] = ast.Num(float(p[1]))

def p_string(p):
    """string : LIT_STRING
    """
    p[0] = ast.Str(p[1][1:-1])

#def p_trans_string(p):
#    """trans_string : LIT_STRING
#        """
#    p[0] = p[1][1:-1]

def p_list(p):
    """list : LBRACK parameters RBRACK
            | RANGE LPAREN number RPAREN
            | RANGE LPAREN number COMMA number RPAREN
    """
    if p[1] == '[':
        p[0] = ast.List(p[2], ast.Load())

    elif p[1] == 'range' and p[4] == ',':
        p[0] = value=ast.Call(func=ast.Name(id='range', ctx=ast.Load()), args=[
        p[3],p[5]
      ], keywords=[], starargs=None, kwargs=None)

    else:
        p[0] = value=ast.Call(func=ast.Name(id='range', ctx=ast.Load()), args=[
        p[3],
      ], keywords=[], starargs=None, kwargs=None)

def p_bool(p):
    """bool : TRUE
            | FALSE
    """
    if p[1] == "true":
        p[0] = ast.Name("True", ast.Load())
    else:
        p[0] = ast.Name("False", ast.Load())

# Use variable_store and variable_load instead of NAME for variables
def p_variable_store(p):
    """variable_store : NAME
    """
    p[0] = ast.Name(p[1], ast.Store())

def p_variable_load(p):
    """variable_load : NAME
    """
    p[0] = ast.Name(p[1], ast.Load(), type=get_type(p[1]))

def p_machine(p):
    """machine : MACHINE NAME EQUAL LBRACE machine_body RBRACE
               | MACHINE NAME EQUAL LBRACE RBRACE
    """
    p[0] = nodes.Machine(p[2], p[5])

def p_machine_body(p):
    """machine_body : machine_body_stmt
                    | machine_body machine_body_stmt
    """
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 3:
        if p[2] is None:
            p[0] = p[1]
        elif type(p[2]) is list:
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1] + [p[2]]

def p_machine_body_stmt(p):
    """machine_body_stmt : node
                         | function
                         | transition
                         | NEWLINE
    """

    if p[1] != '\n':
        p[0] = p[1]


def p_node(p):
    """node : NODE NAME NEWLINE
    """
    p[0] = None if len(p) is 2 else nodes.Node(p[2])

def p_function(p):
    """function : three_es LPAREN NAME RPAREN LBRACE func_statement_list RBRACE
    """

    #p[0] = []

    #p[0].append(ast.FunctionDef('func_'+p[3], ast.arguments([], None, None, []), p[6] if p[6] is not None else [ast.Pass()], []))

    #p[0].append(ast.AugAssign(ast.Attribute(ast.Name(p[3], ast.Load()), 'on_'+p[1], ast.Store()), ast.Add(), ast.Name('func_'+p[3], ast.Load())))

    p[0] = nodes.Function(e=p[1], name=p[3], body=p[6])


def p_three_es(p):
    """three_es : ENTER
                | EXIT
                | END
    """

    p[0] = p[1]

def p_transition(p):
    """transition : NAME LPAREN string RPAREN ARROW NAME NEWLINE
                  | NAME LPAREN string RPAREN ARROW NAME LBRACE func_statement_list RBRACE
                  | NAME LPAREN RPAREN ARROW NAME NEWLINE
                  | NAME LPAREN RPAREN ARROW NAME LBRACE func_statement_list RBRACE
    """
    if len(p) == 8:
        p[0] = nodes.Transition(left=p[1], arg=p[3], right=p[6], body=[])
    elif len(p) == 10:
        p[0] = nodes.Transition(left=p[1], arg=p[3], right=p[6], body=p[8])
    elif len(p) == 7:
        p[0] = nodes.Transition(left=p[1], arg=[], right=p[5], body=[])
    else:
        p[0] = nodes.Transition(left=p[1], arg=[], right=p[5], body=p[7])


def p_new_scope(p):
    """new_scope :
    """
    push_scope(p[-1], p[-2])
    p[0] = p[-1]

def p_error(p):
    warnings.warn("Syntax error on line %d!" % p.lineno, ParseError)

parser = yacc.yacc()

def parse(string):
    """Parse Owl source code and return the AST with symbol_table attached.

    NOTE: Make sure you call this instead of parser.parse() if you need the
          generated symbol table.
    """
    reset_symbol_table()
    tree = parser.parse(string)
    if tree is not None:
        global symbol_table, symbol_stack
        tree.symbol_table = symbol_table
        tree.symbol_stack = symbol_stack
    return tree

def build_tree(args):
    """Build an AST tree from expected command line args.

    args[0] = script name
    args[1] = <filename>
    args[1] = None for reading stdin.
    """
    if len(args) > 1:
        tree = parse(open(args[1]).read())
    else:
        tree = parse(sys.stdin.read())
    tree = ast.fix_missing_locations(tree)
    return tree

def main(args):
    tree = build_tree(args)
    exec compile(tree, '<string>', mode='exec')

if __name__ == '__main__':
    main(sys.argv)
