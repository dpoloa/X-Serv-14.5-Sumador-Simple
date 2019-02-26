#!/bin/usr/python3

# Python Calculator Program

import sys


def suma(sum1, sum2):
    """Suma dos argumentos"""

    return sum1 + sum2


def resta(res1, res2):
    """Resta dos argumentos"""

    return res1 - res2


def multiplicacion(mul1, mul2):
    """Multiplica dos argumentos"""

    return mul1 * mul2


def division(div1, div2):
    """Divide dos argumentos"""

    try:
        return div1 / div2
    except ZeroDivisionError:
        return "infinito"


operators = {
    "sumar": suma,
    "restar": resta,
    "multiplicar": multiplicacion,
    "dividir": division
}


def main(operacion, op1, op2):
    """Cuerpo principal del programa"""

    try:
        return operators[operacion](op1, op2)
    except KeyError:
        print("Operandos disponibles: sumar, restar, multiplicar, dividir")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: ./calculadora.py <operando> <argumento1> <argumento2>")
    else:
        try:
            operation = sys.argv[1]
            arg1 = float(sys.argv[2])
            arg2 = float(sys.argv[3])
        except ValueError:
            print("Argumentos no validos: deben ser numeros ")
            sys.exit(1)

        resultado = main(operation, arg1, arg2)
        print("Resultado:", resultado)


    sys.exit(0)
