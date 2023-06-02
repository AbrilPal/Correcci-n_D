import re

tokens = {
    'WHITESPACE': '\s+',
    'ID': '[A-Za-z][A-Za-z0-9]*',
    'NUMBER': '\d+(\.\d+)?([Ee][+-]?\d+)?',
    'PLUS': '\+',
    'MINUS': '-',
    'TIMES': '\*',
    'DIV': '/',
    'LPAREN': '\(',
    'RPAREN': '\)',
}

def lexer(input_str):
    tokens_list = []
    while input_str:
        match = None
        for token_name, token_rule in tokens.items():
            regex = re.compile(r'^' + token_rule)
            match = regex.search(input_str)
            if match:
                token_value = match.group(0)
                tokens_list.append((token_name, token_value))
                input_str = input_str[len(token_value):]
                break
        if not match:
            raise ValueError('Error: No se pudo analizar el siguiente token en la entrada: {}'.format(input_str))
    return tokens_list

file_path = input('Ingrese la ruta del archivo de entrada: ')
print()
with open(file_path, 'r') as file:
    input_str = file.read()

tokens_list = lexer(input_str)
for token_name, token_value in tokens_list:
    if token_name == 'ID':
        print('ID: {}'.format(token_value))
    else:
        print('{} : {}'.format(token_name, token_value))
