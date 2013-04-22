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
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
)

# Symbol Table

symbol_table = {
    # Example entry
    # 'myvar' : None
    # 'myfunc' : { 'x' : None }
}
scope_stack = []
def current_scope():
    """Get the symbol_table of the current scope stack.
    """
    scope = symbol_table
    for name in scope_stack:
        scope = scope[name]
    return scope

def push_scope(name):
    global symbol_table
    symbol_table[name] = {}
    scope_stack.append(name)

def pop_scope():
    scope_stack.pop()


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
                 | iteration
                 | selection_statement
                 | machine
                 | function_def
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

def p_expression(p):
    """expression : function_call
                  | arithmetic_expression
                  | comparison_expression
                  | string
                  | number
                  | bool
                  | variable_load
                  | list
    """
    p[0] = p[1]

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

def p_iteration(p):
    """iteration : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE
                 | FOR variable_store IN variable_load LBRACE statement_list RBRACE
    """

    if p[1] == "while":
        p[0] = ast.While(p[3], p[6], [])
    else:
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
    """statement_list : statement
                      | statement statement_list
    """

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] is not None:
            p[0] = p[1] + ([p[2]] if p[2] is not None else [])
        else:
            p[0] = ([p[2]] if p[2] is not None else [])

def p_function_def(p):
    """function_def : type NAME LPAREN params_def_list RPAREN LBRACE statement_list RBRACE
                    | VOID NAME LPAREN params_def_list RPAREN LBRACE statement_list RBRACE
    """
    p[0] = ast.FunctionDef(name=p[2], args=ast.arguments(args=p[4], vararg=None, kwarg=None, defaults=[]), body=p[7], decorator_list=[], type=p[1])

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

    if len(p) == 3:
        # this is for default initialization


        if p[1] == int:
            p[0] = ast.Assign([p[2]], ast.Num(0), type=int)

                
        elif p[1] == bool:
            p[0] = ast.Assign([p[2]], ast.Name("False", ast.Load()),
                type=bool)
                
        elif p[1] == float:
            p[0] = ast.Assign([p[2]], ast.Num(0), type=float)

        elif p[1] == str:
            p[0] = ast.Assign([p[2]], ast.Str(""), type=str)
                
        elif p[1] == list:
            p[0] = ast.Assign([p[2]], ast.List([], ast.Load()), type=list) #check correctness

        else:
            print("%s err" % (str(p[1])))
        


    else:
          #add type checking here
          p[0] = ast.Assign([p[2]], p[4], type=p[1])


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

def p_trans_string(p):
    """trans_string : LIT_STRING
        """
    p[0] = p[1][1:-1]


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
    p[0] = ast.Name(p[1], ast.Load())

def p_machine(p):
    """machine : MACHINE NAME EQUAL LBRACE machine_body RBRACE
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

    #print p[0]

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

    #print p[0]


def p_function(p):
    """function : three_es LPAREN NAME RPAREN LBRACE statement_list RBRACE
    """ 

    p[0] = []

    p[0].append(ast.FunctionDef('func_'+p[3], ast.arguments([], None, None, []), p[6] if p[6] is not None else [ast.Pass()], []))

    p[0].append(ast.AugAssign(ast.Attribute(ast.Name(p[3], ast.Load()), 'on_'+p[1], ast.Store()), ast.Add(), ast.Name('func_'+p[3], ast.Load())))

def p_three_es(p):
    """three_es : ENTER
                | EXIT
                | END
    """

    p[0] = p[1]


def p_transition(p):
    """transition : NAME LPAREN string RPAREN ARROW NAME NEWLINE
                  | NAME LPAREN string RPAREN ARROW NAME LBRACE statement_list RBRACE
    """
    if len(p) == 8:
        p[0] = nodes.Transition(left=p[1], arg=p[3], right=p[6], body=[])
    elif len(p) == 10:
        p[0] = nodes.Transition(left=p[1], arg=p[3], right=p[6], body=p[8])


    """
    if len(p) == 10:
        machine_trans.append(str(p[1])+str(p[6]))


        p[0] = []

        p[0].append(ast.FunctionDef('trans_'+str(p[1])+str(p[6]), ast.arguments([], None, None, []), p[8] if p[8] is not None else [ast.Pass()], []))

        p[0].append(ast.Assign([ast.Name(str(p[1])+str(p[6]), ast.Store()),], ast.Call(ast.Name('Transition', ast.Load()), [ast.Name(p[1], ast.Load()),
                                                                                                        ast.Name(p[6], ast.Load()),
                                                                                                        ast.Lambda(ast.arguments([ast.Name('x', ast.Param())], None, None, []),
                                                                                                        ast.Compare(ast.Name('x', ast.Load()),[ ast.Eq()], [p[3]])),], [],
                                                                                                        None, None)))
        
        p[0].append(ast.AugAssign(ast.Attribute(ast.Name(str(p[1])+str(p[6]), ast.Load()), 'on_enter', ast.Store()), ast.Add(), ast.Name('trans_'+str(p[1])+str(p[6]), ast.Load())))




    elif len(p) == 8:
        machine_trans.append(str(p[1])+str(p[6]))


        p[0] = []

        p[0].append(ast.FunctionDef('trans_'+str(p[1])+str(p[6]), ast.arguments([], None, None, []), [ast.Pass()], []))


        # p[0].append(ast.Assign([ast.Name(str(p[1])+str(p[6]), ast.Store()),], ast.Call(ast.Name('Transition', ast.Load()), [ast.Name(p[1], ast.Load()),
        #                                                                                    ast.Name(p[6], ast.Load())],[],None, None)))

        p[0].append(ast.Assign([ast.Name(str(p[1])+str(p[6]), ast.Store()),], ast.Call(ast.Name('Transition', ast.Load()), [ast.Name(p[1], ast.Load()),
                                                                                                        ast.Name(p[6], ast.Load()),
                                                                                                        ast.Lambda(ast.arguments([ast.Name('x', ast.Param())], None, None, []),
                                                                                                        ast.Compare(ast.Name('x', ast.Load()),[ ast.Eq()], [p[3]]))], [],
                                                                                                        None, None)))

        p[0].append(ast.AugAssign(ast.Attribute(ast.Name(str(p[1])+str(p[6]), ast.Load()), 'on_enter', ast.Store()), ast.Add(), ast.Name('trans_'+str(p[1])+str(p[6]), ast.Load())))



    else:
        pass
        
    """



def p_error(p):
    warnings.warn("Syntax error on line %d!" % p.lineno, ParseError)

parser = yacc.yacc()

def parse(string):
    """Parse Owl source code and return the AST with symbol_table attached.

    NOTE: Make sure you call this instead of parser.parse() if you need the
          generated symbol table.
    """
    # Reset the symbol_table in the global scope in case we're reusing it.
    global symbol_table
    symbol_table = {}

    tree = parser.parse(string)
    tree.symbol_table = symbol_table
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
