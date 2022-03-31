import ply.lex as lexico

salidas = []
error = False

tokens = [
    "PUNTOCOMA","COMA","PARENTECISAPERTURA","PARENTESISCIERRE",
    "LLAVEAPERTURA","LLAVECIERRE","DIGITO",
    "MODIFICADORACCESO",'ID','TIPODATO','CLASE', 'PUBLIC','NOMBRECLASE'
]

t_ignore = ' \t'
t_PUNTOCOMA = r';'
t_COMA = r','
t_PARENTECISAPERTURA = r'\('
t_PARENTESISCIERRE = r'\)'
t_LLAVEAPERTURA = r'\{'
t_LLAVECIERRE = r'\}'

def t_NOMBRECLASE(t):
    r'([A-Z])([a-z]+)'
    return t

def t_PUBLIC(t):
    r'^(public)'
    return t

def t_MODIFICADORACCESO(t):
    # r'public | private | protected | default'
    r'public | private | protected | default'
    return t

def t_CLASE(t):
    r'class'
    return t

def t_DIGITO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_TIPODATO(t):
    r'string | float | int'
    return t


def t_ID(t):
    # ### r'^([a-z])([0-9]+)$'
    # r'([a-z][a-z]*)([0-9]+)'
    r'([a-z]+)'
    # r'\w+'
    return t

def t_error(t):
    global error
    # if t.value[0]:
    if t:
        print('Caracter '+ str(t.value[0])+ ' no válido')
        t.lexer.skip(1)
        num_ascii = ord(str(t.value[0]))
        print(num_ascii)
        # simbolo = chr(ascci_)
        print(f'Este es un numero ascii {num_ascii} --> Simbolo: {chr(num_ascii)}')
        # salidas.append('Error Caracter No Válido: '+ str(t.value[0]))
        # salidas.append('Error Caracter No Válido:--> '+ str(ascci_))
        salidas.append(str(num_ascii))
        error = True
    


def t_newLine(t):
    r'\n'
    t.lexer.lineno += len(t.value)

cadena = ''
# analizador = lexico.lex()
def analizar(cadena):
    global salidas
    analizador = lexico.lex()
    analizador.input(cadena)

    while True:
        tok = analizador.token()
        if not tok: break
        salidas.append(str(tok))