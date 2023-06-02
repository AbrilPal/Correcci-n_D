"""
    Andrea Abril Palencia Gutierrez, 18198
    Diseño de Lenguajes de Programacion
    23 de febrero del 2023

    Convertir de INFIX a POSTFIX: usa como parametro una cadena ya
    formateada y devolver una cadena POSTFIX para luego contruir el
    arbol.
"""
from Lab_A.Stack import *
from Lab_A.Formatear_Expresion import Formatear

def getPrecedence(caracter):
    if(caracter == '(' or caracter == ')'):
        return 1
    elif(caracter == '|'):
        return 2
    elif(caracter == '.'):
        return 3
    elif(caracter == '?' or caracter == '*' or caracter == '+'):
        return 4
    elif(caracter == '^'):
        return 5
    else:
        return 6

def Infix_Postfix(expresion_re):
    postfix = []
    stack = Stack()
    expresion_form = Formatear(expresion_re)

    for c in expresion_form:
        if c == '(':
            stack.push(c)
        elif c == ')':
            while stack.peek() != '(':
                postfix.append(stack.pop())
            stack.pop()
        else:
            while not stack.is_empty():
                peekedChar = stack.peek()
                peekedCharPrece = getPrecedence(peekedChar)
                currentCharPrece = getPrecedence(c)

                if peekedCharPrece >= currentCharPrece:
                    postfix.append(stack.pop())
                else:
                    break
            
            stack.push(c)
    
    while not stack.is_empty():
        postfix.append(stack.pop())

    postfixFinal = ''.join(postfix)
    print("La expresion POSTFIX es: ", postfixFinal, "\n")
    return postfixFinal

