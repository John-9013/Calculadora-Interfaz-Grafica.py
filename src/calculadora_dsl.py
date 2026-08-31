# Simple DSL para la calculadora usando PLY (lex + yacc)
# Provee:
#   - tokens y lexer
#   - parser con precedencia
#   - soporte para operador de potencia `**`
#   - llamadas a funciones matemáticas seguras (sin, cos, tan, sqrt, pow, log, exp, abs)
#   - comentarios de línea que empiezan con `#` y son ignorados
#   - variables (tabla de símbolos) accesible desde la GUI: variables.clear() funciona
#   - exporta `parser` (objeto yacc) y `parse(text)` para evaluar expresiones

import math
import ply.lex as lex
import ply.yacc as yacc

# Diccionario de variables (exportado)
variables = {}

# Tokens
tokens = (
    'NUMBER',
    'ID',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN', 'COMMA',
    'EQUALS',
)

# Token regexes
t_PLUS    = r'\+'
t_MINUS   = r'-'
# TIMES must be single '*' (POWER is '**')
t_TIMES   = r'\*'
# DIVIDE
t_DIVIDE  = r'/'
# POWER (two stars)
t_POWER   = r'\*\*'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA   = r','
t_EQUALS  = r'='

# Ignorar espacios y tabs
t_ignore = ' \t'

# Comentarios de línea con '#', se ignoran
def t_COMMENT(t):
    r'\#.*'
    pass

# Números (enteros y flotantes)
def t_NUMBER(t):
    r"\d+(\.\d+)?"
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Identificadores (variables y nombres de funciones)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'ID'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    raise SyntaxError(f"Caracter inválido '{t.value[0]}' en la posición {t.lexpos}")

# Construir el lexer
lexer = lex.lex()

# Precedencia (para operaciones aritméticas)
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'POWER'),  # potencia, asociativa a la derecha
    ('right', 'UMINUS'),
)

# Funciones matemáticas permitidas (mapeo seguro)
_allowed_funcs = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'pow': math.pow,
    'log': math.log,
    'exp': math.exp,
    'abs': abs,
}

# Gramática

def p_statement_assign(p):
    'statement : ID EQUALS expression'
    varname = p[1]
    value = p[3]
    variables[varname] = value
    p[0] = value


def p_statement_expr(p):
    'statement : expression'
    p[0] = p[1]


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    left = p[1]
    right = p[3]
    op = p[2]
    if op == '+':
        p[0] = left + right
    elif op == '-':
        p[0] = left - right
    elif op == '*':
        p[0] = left * right
    elif op == '/':
        if right == 0:
            raise ZeroDivisionError("División por cero")
        p[0] = left / right


def p_expression_power(p):
    'expression : expression POWER expression'
    # Exponenciación: asociatividad a la derecha se controla con precedence
    p[0] = p[1] ** p[3]


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_id(p):
    'expression : ID'
    varname = p[1]
    if varname in variables:
        p[0] = variables[varname]
    else:
        raise NameError(f"Variable no definida: {varname}")


def p_expression_func_call(p):
    'expression : ID LPAREN arg_list RPAREN'
    fname = p[1]
    args = p[3] if p[3] is not None else []
    if fname in _allowed_funcs:
        func = _allowed_funcs[fname]
        try:
            p[0] = func(*args)
        except TypeError as e:
            raise TypeError(f"Error en llamada a función '{fname}': {e}")
    else:
        raise NameError(f"Función no permitida o inexistente: {fname}")


def p_arg_list_multiple(p):
    'arg_list : arg_list COMMA expression'
    p[0] = p[1] + [p[3]]


def p_arg_list_single(p):
    'arg_list : expression'
    p[0] = [p[1]]


def p_arg_list_empty(p):
    'arg_list : '
    p[0] = []


def p_error(p):
    if p is None:
        raise SyntaxError("Fin de entrada inesperado")
    else:
        raise SyntaxError(f"Token inesperado '{p.value}' en la línea {p.lineno}")

# Construir el parser (exportamos un objeto llamado `parser` compatible con parser.parse(text))
parser = yacc.yacc()


def parse(text):
    """Parsea y evalúa la expresión/statement. Lanza excepciones en errores."""
    if text is None:
        raise ValueError("Expresión vacía")
    text = text.strip()
    if text == "":
        return 0
    # reset lexer state entre parseos
    lexer.input(text)
    result = parser.parse(text, lexer=lexer)
    # normalizar números: si es float entero, devolver int
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result
