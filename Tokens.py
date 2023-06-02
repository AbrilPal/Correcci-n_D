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

def get_tokens():
    return tokens

