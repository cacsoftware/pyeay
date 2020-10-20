# -*- coding: utf-8 -*-
import string

class FormatearNumeros():
    @staticmethod
    def toNumTelefonico(cad):
        cadInv = cad[::-1]  # invierte la cadena

        t = 0
        nuevaCadena = ''
        for i in cadInv:
            nuevaCadena += i
            t += 1
            if t in [2, 4, 7, 10]:
                nuevaCadena += '.'

        if nuevaCadena[-1] == '.':
            nuevaCadena = nuevaCadena[:-1]
        return nuevaCadena[::-1]

    @staticmethod
    def toNumMilesSigno(cad, signo=''):
        cad = str(cad)
        cadInv = cad[::-1]  # invierte la cadena
        t = 0
        nuevaCadena = ''
        for i in cadInv:
            nuevaCadena += i
            t += 1
            if t in [3, 6, 9, 12, 15]:
                nuevaCadena += '.'
        if nuevaCadena[-1] == '.':
            nuevaCadena = nuevaCadena[:-1]
        if signo == '':
            return nuevaCadena[::-1]
        else:
            return signo + ' ' + nuevaCadena[::-1]

    @staticmethod
    def toNumSinPuntos(cad):
        nuevaCadena = ''
        for i in cad:
            if i != '.':
                nuevaCadena += i
        return int(nuevaCadena)

    @staticmethod
    def extraerCant_idProducto(cad):
        lista = []
        sw = 0
        num1 = ''
        num2 = ''
        i = 0
        for i in range(len(cad)):
            if cad[i] in string.digits:
                num1 += cad[i]
                sw = 1
            else:
                if sw == 1:
                    break
        cad2 = cad[i + 1:]
        sw = 0
        for j in range(len(cad2)):
            if cad2[j] in string.digits:
                num2 += cad2[j]
                sw = 1
            else:
                if sw == 1:
                    break
        if num1 != '':
            lista.append(num1)
        if num2 != '':
            lista.append(num2)

        return lista