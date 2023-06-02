import re
tokens_d = {
    'WHITESPACE': r'\s+',
    'ID': r'[A-Za-z][A-Za-z0-9]*',
    'NUMBER': r'\d+(\.\d+)?([Ee][+-]?\d+)?',
    'PLUS': r'\+',
    'MINUS': r'-',
    'TIMES': r'\*',
    'DIV': r'/',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'ASSIGNOP': r':=',
    'EQUALS': r'=',
    'SEMICOLON': r';',
    'LT': r'<',
    'GT': r'>',
}

def merge_tokens(tokens, additional_tokens):
    """
    Función que combina dos diccionarios de tokens y elimina los tokens repetidos según su token_rule y token_name.

    Args:
        tokens (dict): Diccionario original de tokens.
        additional_tokens (dict): Diccionario de tokens adicionales a agregar.

    Returns:
        dict: Diccionario combinado de tokens sin tokens repetidos según su token_rule y token_name.
    """
    merged_tokens = tokens.copy()
    for token_name, token_rule in additional_tokens.items():
        if token_name not in merged_tokens.keys() and token_rule not in merged_tokens.values():
            merged_tokens[token_name] = token_rule
    return merged_tokens

def filter_tokens(tokens, tokens_d):
    """
    Función que filtra los tokens de un diccionario de tokens generados por la función
    extract_tokens_from_yalex_file, 
    Args:
        tokens (dict): Diccionario con los tokens y sus reglas.
        tokens_d (dict): Diccionario con los nombres de los tokens permitidos y sus reglas.
    Returns:
        dict: Diccionario con los tokens procesados.
    """
    filtered_tokens = {}
    for token_name, token_rule in tokens.items():
        if token_name == "id" and "ID" in tokens_d:
            filtered_tokens["ID"] = tokens_d["ID"]
        elif token_name == "number" and "NUMBER" in tokens_d:
            filtered_tokens["NUMBER"] = tokens_d["NUMBER"]
        elif token_name == "ws":
            filtered_tokens["WHITESPACE"] = tokens_d["WHITESPACE"]
        elif token_name in tokens_d and token_rule == tokens_d[token_name]:
            filtered_tokens[token_name] = token_rule
    return filtered_tokens


def extract_tokens_from_yalex_file(file_path, tokens_d):
    """
    Función que extrae los tokens de una gramática en formato yalex desde un archivo
    Args:
        file_path (str): Ruta del archivo yalex.
        tokens_d (dict): Diccionario con los tokens y sus reglas a reemplazar.
    Returns:
        dict: Diccionario con los tokens y sus reglas.
    """
    tokens = {}

    with open(file_path, 'r') as file:
        contenido = file.read()

    contenido_sin_comentarios = re.sub(r'\(\*.*?\*\)', '', contenido, flags=re.DOTALL)

    with open(file_path, 'w') as file:
        file.write(contenido_sin_comentarios)

    with open(file_path, 'r') as file:
        yalex_text = file.read()

    tokens_def = re.findall(r"let\s+(\w+)\s+=\s+(.+)", yalex_text)

    for token_name, token_rule in tokens_def:
        if "return" in token_rule:
            token_rule = token_rule.replace("'", "").replace("return", "").strip()
            if token_rule in tokens_d:
                tokens[token_name] = tokens_d[token_rule]
                tokens[token_rule] = tokens_d[token_rule] 
            else:
                if token_name in tokens_d:
                    tokens[token_name] = tokens_d[token_name]
                else:
                    tokens[token_name] = token_rule
        else:
            token_rule = token_rule.replace("'", "")
            if token_rule in tokens_d:
                tokens[token_name] = tokens_d[token_rule]
                tokens[token_rule] = tokens_d[token_rule]
            else:
                if token_name in tokens_d:
                    tokens[token_name] = tokens_d[token_name]
                else:
                    tokens[token_name] = token_rule

    rules = re.findall(r"rule\s+tokens\s+=\s+([\s\S]+?)(?=\nrule|\Z)", yalex_text)

    for rule in rules:
        rule_lines = rule.split("\n")
        for line in rule_lines:
            line = line.strip()
            if line:
                tokens_and_rules = line.split("{")
                token_names = tokens_and_rules[0].split("|")
                for token_name in token_names:
                    token_name = token_name.strip()
                    if token_name and token_name not in tokens.keys():
                        if len(tokens_and_rules) > 1:
                            token_rule = tokens_and_rules[1].split("}")[0].strip()
                            if "return" in token_rule:
                                token_rule = token_rule.replace("'", "").replace("return", "").strip()
                                if token_rule in tokens_d:
                                    tokens[token_name] = tokens_d[token_rule]
                                    tokens[token_rule] = tokens_d[token_rule] 
                                else:
                                    if token_name in tokens_d:
                                        tokens[token_name] = tokens_d[token_name]
                                    else:
                                        tokens[token_name] = token_rule
                            else:
                                if token_rule in tokens_d:
                                    tokens[token_name] = tokens_d[token_rule]
                                    tokens[token_rule] = tokens_d[token_rule] 

    return tokens

file_path = input('Ingrese la ruta del archivo de entrada: ')
tokens = extract_tokens_from_yalex_file(file_path, tokens_d)
tokens = filter_tokens(tokens, tokens_d)

# Imprimir los tokens y sus reglas
for token_name, token_rule in tokens.items():
    print("Token: %s " % (token_name))

def get_tokens():
    return tokens

def generar_scanner(tokens):
    with open('scanner.py', 'w') as archivo:
        archivo.write("import re\n\n")
        archivo.write("tokens = {\n")
        for token_name, token_regex in tokens.items():
            archivo.write(f"    '{token_name}': '{token_regex}',\n")
        archivo.write("}\n\n")

        archivo.write("def lexer(input_str):\n")
        archivo.write("    tokens_list = []\n")
        archivo.write("    while input_str:\n")
        archivo.write("        match = None\n")
        archivo.write("        for token_name, token_rule in tokens.items():\n")
        archivo.write("            regex = re.compile(r'^' + token_rule)\n")
        archivo.write("            match = regex.search(input_str)\n")
        archivo.write("            if match:\n")
        archivo.write("                token_value = match.group(0)\n")
        archivo.write("                tokens_list.append((token_name, token_value))\n")
        archivo.write("                input_str = input_str[len(token_value):]\n")
        archivo.write("                break\n")
        archivo.write("        if not match:\n")
        archivo.write("            raise ValueError('Error: No se pudo analizar el siguiente token en la entrada: {}'.format(input_str))\n")
        archivo.write("    return tokens_list\n\n")

        archivo.write("file_path = input('Ingrese la ruta del archivo de entrada: ')\n")
        archivo.write("print()\n")
        archivo.write("with open(file_path, 'r') as file:\n")
        archivo.write("    input_str = file.read()\n\n")

        archivo.write("tokens_list = lexer(input_str)\n")
        archivo.write("for token_name, token_value in tokens_list:\n")
        archivo.write("    if token_name == 'ID':\n")
        archivo.write("        print('ID: {}'.format(token_value))\n")
        archivo.write("    else:\n")
        archivo.write("        print('{} : {}'.format(token_name, token_value))\n")

def generar_tokens(tokens):
    with open('Tokens.py', 'w') as archivo:
        archivo.write("import re\n\n")
        archivo.write("tokens = {\n")
        for token_name, token_regex in tokens.items():
            archivo.write(f"    '{token_name}': '{token_regex}',\n")
        archivo.write("}\n\n")

        archivo.write("def get_tokens():\n")
        archivo.write("    return tokens\n\n")

generar_scanner(tokens)
generar_tokens(tokens)

