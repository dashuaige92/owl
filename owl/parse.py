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
    """Get all names visible in the current scope."""
    return [var for scope in symbol_stack for var in scope]

def global_names():
    """Get all names visible outside of the local scope, with scope level."""
    return [(level, var) for level, scope in enumerate(symbol_stack[:-1]) for var in scope]

def local_names():
    """Get all names in the local scope."""
    return get_table(scope_stack).keys()

def get_type(var_name):
    """Get an identifier's scope level and type."""
    for i in range(len(scope_stack) + 1):
        subtable = get_table(scope_stack if i is 0 else scope_stack[:-i])
        if var_name in subtable:
            return (len(scope_stack) - i, subtable[var_name]['type'] if type(subtable[var_name]) is dict else subtable[var_name])
    return (0, None)

def add_symbol(var_name, var_type):
    """Add an identifier in the local scope."""
    if var_name in local_names():
        warnings.warn("%s has been declared twice!" % (var_name), ParseError)

    symbol_stack[-1].append(var_name)
    get_table(scope_stack)[var_name] = var_type

def push_scope(scope_name, scope_type=None):
    if scope_name in local_names():
        warnings.warn("%s declared twice" % (scope_name), ParseError)

    #symbol_stack[-1].append(scope_name)
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
                                                             ], keywords=[], starargs=None, kwargs=None, type=str)

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
        if p[2].id not in all_names():
            warnings.warn("%s not declared before for loop!" % (p[2].id,), ParseError)
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
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 3:
        p[0] = ([p[1]] if p[1] is not None else []) + p[2]

def p_statement_list_item(p):
    """statement_list_item : NEWLINE
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

def p_statement_list_item_expression(p):
    """statement_list_item : expression NEWLINE
    """
    p[0] = p[1] if type(p[1]) is ast.Print else ast.Expr(value=p[1])

def p_function_def(p):
    """function_def : type NAME new_scope LPAREN params_def_list RPAREN LBRACE func_statement_list RBRACE
                    | void NAME new_scope LPAREN params_def_list RPAREN LBRACE func_statement_list RBRACE
    """
    p[0] = ast.FunctionDef(name=p[2], args=ast.arguments(args=p[5], vararg=None, kwarg=None, defaults=[]), body=p[8], decorator_list=[], type=p[1], level=0, globals=global_names())
    pop_scope()

def p_func_statement_list(p):
    """func_statement_list : func_statement_list_item
                           | func_statement_list_item func_statement_list
    """
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 3:
        p[0] = ([p[1]] if p[1] is not None else []) + p[2]

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
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 4:
        p[0] = ([p[1]] if p[1] is not None else []) + p[3]

def p_params_def(p):
    """params_def : type NAME
                  |
    """
    if len(p) != 1:
        add_symbol(p[2], p[1])
        p[0] = ast.Name(id=p[2], ctx=ast.Param(), type=p[1], level=len(scope_stack))

def p_function_call(p):
    """function_call : PRINT LPAREN expression RPAREN
                     | TOINT LPAREN expression RPAREN
                     | TOBOOL LPAREN expression RPAREN
                     | TOFLOAT LPAREN expression RPAREN
                     | TOSTRING LPAREN expression RPAREN
                     | variable_load LPAREN parameters RPAREN
                     | variable_load DOT NAME LPAREN parameters RPAREN
                     | variable_load DOT NAME
                     | variable_load LBRACK expression RBRACK
    """
    if p[1] == 'print':
        p[0] = ast.Print(None, [p[3]], True)
    elif p[1] == 'toInt':
        p[0] = ast.Call(func=ast.Name(id='int', ctx=ast.Load()), args=[p[3]], keywords=[], starargs=None, kwargs=None, type=int)
    elif p[1] == 'toBool':
        p[0] = ast.Call(func=ast.Name(id='bool', ctx=ast.Load()), args=[p[3]], keywords=[], starargs=None, kwargs=None, type=bool)
    elif p[1] == 'toFloat':
        p[0] = ast.Call(func=ast.Name(id='float', ctx=ast.Load()), args=[p[3]], keywords=[], starargs=None, kwargs=None, type=float)
    elif p[1] == 'toString':
        p[0] = ast.Call(func=ast.Name(id='str', ctx=ast.Load()), args=[p[3]], keywords=[], starargs=None, kwargs=None, type=str)
    elif len(p) == 4:
        p[0] = ast.Attribute(value=p[1], attr=p[3], ctx=ast.Load())
    elif len(p) == 7:
        p[0] = ast.Call(func=ast.Attribute(value=p[1], \
            attr=p[3], ctx=ast.Load()), args=p[5], keywords=[], starargs=None, kwargs=None)
    elif len(p) == 5:
        # [TODO] Typecheck expression for int
        if p[2] == '[':
            p[0] = ast.Subscript(
                value=p[1],
                slice=ast.Index(value=p[3]),
                ctx=ast.Load(),
                )
        elif p[2] == '(':
            p[0] = ast.Call(func=p[1], \
                args=p[3], keywords=[], starargs=None, kwargs=None)

def p_parameters(p):
    """parameters    : expression
                     | expression COMMA parameters
                     |
    """
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 4:
        p[0] = ([p[1]] if p[1] is not None else []) + p[3]
    elif len(p) == 1:
        p[0] = []

def p_initialization(p):
    """initialization : type variable_init EQUAL expression
                      | type variable_init
    """
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

        #check correctness
        elif p[1] == (list,int):
            #p[1][0] - accesses first element of tuple, use '1' for second elem
            p[0] = ast.Assign([p[2]], ast.List([], ast.Load(), type=p[1]), type=p[1]) #check correctness
        elif p[1] == (list,bool):
            p[0] = ast.Assign([p[2]], ast.List([], ast.Load(), type=p[1]), type=p[1]) #check correctness
        elif p[1] == (list,float):
            p[0] = ast.Assign([p[2]], ast.List([], ast.Load(), type=p[1]), type=p[1]) #check correctness
        elif p[1] == (list,str):
            p[0] = ast.Assign([p[2]], ast.List([], ast.Load(), type=p[1]), type=p[1]) #check correctness

        else:
            warnings.warn("%s Initialization error" % (str(p[1]),), ParseError)
    else:
        p[0] = ast.Assign([p[2]], p[4], type=p[1])

def p_variable_init(p):
    """variable_init : NAME
    """

    add_symbol(p[1], p[-1])
    scope_level, var_type = get_type(p[1])
    p[0] = ast.Name(p[1], ast.Store(), type=var_type, level=scope_level)

def p_assignment(p):
    """assignment : variable_store EQUAL expression
                  | variable_store PEQUAL expression
                  | variable_store MEQUAL expression
                  | variable_store TEQUAL expression
                  | variable_store DEQUAL expression
    """
                  #| variable_store LBRACK expression RBRACK EQUAL expression
    operators = {
        '=' : ast.Eq(),
        '+=': ast.Add(),
        '-=': ast.Sub(),
        '*=': ast.Mult(),
        '/=': ast.Div(),
    }
    if len(p) == 4:
        target = p[1]
        value = p[3]
    elif len(p) == 6:
        target = ast.Subscript(
            value=p[1],
            slice=ast.Index(value=p[3]),
            ctx=ast.Load(),
            )
        value = p[6]

    if p[2] == '=':
        p[0] = ast.Assign(targets=[target], value=value, type=p[1].type)
    else:
        p[0] = ast.AugAssign(target=target, op=operators[p[2]], value=value)

def p_void(p):
    """void : VOID
    """
    p[0] = None

def p_type(p):
    """type : INT
            | BOOL
            | FLOAT
            | STRING
            | INT LBRACK RBRACK
            | BOOL LBRACK RBRACK
            | FLOAT LBRACK RBRACK
            | STRING LBRACK RBRACK
    """
    if len(p) == 2:
        if p[1] == 'int':
            p[0] = int
        elif p[1] == 'bool':
            p[0] = bool
        elif p[1] == 'float':
            p[0] = float
        elif p[1] == 'string':
            p[0] = str

    elif len(p) == 4: #list types
        if p[1] == 'int':
            p[0] = (list,int)
        elif p[1] == 'bool':
            p[0] = (list,bool)
        elif p[1] == 'float':
            p[0] = (list,float)
        elif p[1] == 'string':
            p[0] = (list,str)

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
    p[0] = ast.Str(p[1][1:-1], type=str)

def p_list(p):
    """list : LBRACK parameters RBRACK
            | RANGE LPAREN number RPAREN
            | RANGE LPAREN number COMMA number RPAREN
    """
    if p[1] == '[':
        p[0] = ast.List(p[2], ast.Load(), type=list)

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
        p[0] = ast.Name("True", ast.Load(), type=bool)
    else:
        p[0] = ast.Name("False", ast.Load(), type=bool)

# Use variable_store and variable_load instead of NAME for variables
def p_variable_store(p):
    """variable_store : NAME
    """
    scope_level, var_type = get_type(p[1])
    p[0] = ast.Name(p[1], ast.Store(), type=var_type, level=scope_level)

def p_variable_load(p):
    """variable_load : NAME
    """
    # check if variable has been declared
    scope_level, var_type = get_type(p[1])
    p[0] = ast.Name(p[1], ast.Load(), type=var_type, level=scope_level)

def p_machine(p):
    """machine : MACHINE NAME EQUAL LBRACE machine_body RBRACE
               | MACHINE NAME EQUAL LBRACE RBRACE
    """
    p[0] = nodes.Machine(p[2], p[5], level=0)

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

    """function : three_es LPAREN NAME new_machine_function_scope RPAREN LBRACE func_statement_list RBRACE
    """ 
    p[0] = nodes.Function(e=p[1], name=p[3], body=p[7], level=0, globals=global_names())
    pop_scope()

def p_three_es(p):
    """three_es : ENTER
                | EXIT
                | END
    """

    p[0] = p[1]

def p_transition(p):
    """transition : NAME LPAREN string RPAREN ARROW NAME NEWLINE
                  | NAME LPAREN string RPAREN ARROW NAME new_machine_transition_scope LBRACE func_statement_list RBRACE
                  | NAME LPAREN RPAREN ARROW NAME NEWLINE
                  | NAME LPAREN RPAREN ARROW NAME new_machine_default_transition_scope LBRACE func_statement_list RBRACE
    """
    arg = p[3] if len(p) in [8, 11] else []
    body = p[len(p)-2] if len(p) in [10, 11] else []
    p[0] = nodes.Transition(left=p[1], arg=arg, right=p[6], body=body, level=0, globals=global_names())
    if len(p) >= 10:
        pop_scope()

def p_new_machine_function_scope(p):
    """new_machine_function_scope :
    """
    push_scope('_func_' + p[-3] + '_' + p[-1], 'void')
    p[0] = p[-1]

def p_new_machine_transition_scope(p):
    """new_machine_transition_scope :
    """
    push_scope('_trans_' + p[-6] + '_' + p[-1] + '_' + p[-4].s, 'void')
    p[0] = p[-1]

def p_new_machine_default_transition_scope(p):
    """new_machine_default_transition_scope :
    """
    push_scope('_trans_' + p[-5] + '_' + p[-1], 'void')
    p[0] = p[-1]

def p_new_scope(p):
    """new_scope :
    """
    push_scope(p[-1], p[-2])
    p[0] = p[-1]

def p_error(p):
    warnings.warn("Syntax error on line %d at token %s!" % (getattr(p, 'lineno', 0), str(p)), ParseError)

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
