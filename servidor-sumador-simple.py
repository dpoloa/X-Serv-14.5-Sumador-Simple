#!/usr/bin/python3

# Created by:
# Daniel Polo Álvarez
# d.poloa@alumnos.urjc.es

# Based on many programs from:
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
#
# Important: Run with Python 3.6 or higher
#

import socket
import calculadora

myPort = 1234
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind(('localhost', myPort))
mySocket.listen(5)

firstRound = True
firstOperator = 0

PAGE1 = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <h1>Servidor sumador simple</h1>
    <p> El primer operando es: {operando1}</p>
    <p> Esperando segundo argumento</p>
  </body>
</html>
"""

PAGE2 = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <h1>Servidor sumador simple</h1>
    <p> El primer operando es: {operando1}</p>
    <p> El segundo operando es: {operando2}</p>
    <p> Resultado de la operacion: {operando1} {operacion} {operando2} = {resultado}</p>
  </body>
</html>
"""

PAGE_NOT_FOUND = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <h1>Servidor sumador simple</h1>
    <p> Recuso no valido: forma de uso: http://localhost/operacion/operando </p>
  </body>
</html>
"""

PAGE_ERROR = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <h1>Servidor sumador simple</h1>
    <p> Error: {error} </p>
  </body>
</html>
"""


def operatorSymbol(operation):

    if operation == "sumar":
        return "+"
    elif operation == "restar":
        return "-"
    elif operation == "multiplicar":
        return "x"
    elif operation == "dividir":
        return "/"
    else:
        return "?"


try:
    while True:
        print('Waiting for connections')
        (recvSocket, address) = mySocket.accept()
        print('HTTP request received:')
        httpRequest = recvSocket.recv(1024)
        httpRequestStr = str(httpRequest, 'utf-8')
        print("Request: " + httpRequestStr)
        resourceName = httpRequestStr.split(' ', 2)[1]

        if resourceName == "favicon.ico":
            httpCode = b'400 Resource not available'
            httpPage = PAGE_NOT_FOUND
        else:
            try:
                _, function, value = resourceName.split('/')
                if firstRound:
                    try:
                        firstOperator = float(value)
                        httpCode = b'200 OK'
                        httpPage = PAGE1.format(operando1=firstOperator)
                        firstRound = False
                    except ValueError:
                        httpCode = b'400 Value not accepted'
                        httpPage = PAGE_ERROR.format(error="el numero introducido no es valido. Introduce otro numero.")
                else:
                    try:
                        secondOperator = float(value)
                        result = calculadora.operators[function](firstOperator, secondOperator)
                        httpCode = b'200 OK'
                        httpPage = PAGE2.format(operando1=firstOperator, operacion=operatorSymbol(function),
                                                operando2=secondOperator, resultado=result)
                        firstOperator = 0
                        firstRound = True
                    except KeyError:
                        httpCode = b'400 Operator not accepted'
                        httpPage = PAGE_ERROR.format(error="la operacion elegida no existe" +
                                                           "<p>Los operandos disponibles son: sumar, restar, multiplicar, dividir")
                    except ValueError:
                        httpCode = b'400 Value not accepted'
                        httpPage = PAGE_ERROR.format(error="el numero introducido no es valido. Introduce otro numero.")

            except ValueError:
                httpCode = b'400 Resource not available'
                httpPage = PAGE_NOT_FOUND

        recvSocket.send(b"HTTP/1.1 " + httpCode + b"\r\n\r\n" + bytes(httpPage, 'utf-8'))
        recvSocket.close()

except KeyboardInterrupt:
    mySocket.close()
