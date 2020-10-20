# -*- coding: utf-8 -*-

class ManipularRows():

    @staticmethod
    def crearListaValoresYDicccionario(rows, pos_x, pos_y):
        """
        Es una forma compacta de utilizar las funciones:  crear_listaValores()  y  crear_diccionario()

        :param rows:
        :param pos_x:
        :param pos_y:
        :return:
        """
        if rows != None:
            diccionario ={}
            la_lista = []
            for i in rows:
                clave = i[pos_x]
                valor = i[pos_y]

                la_lista.append(valor)
                diccionario[clave] = valor
            return la_lista, diccionario

    @staticmethod
    def crearListaValores(rows, pos_valor):
        """

        :param rows:
        :param pos_valor: es el numero de columna para obtener la lista de valores, es util para cargar por ejemplos comboBox
        :return:
        """
        if rows != None:
            la_lista = []
            for i in rows:
                valor=i[pos_valor]
                la_lista.append(valor)
            return la_lista

    @staticmethod
    def crearDiccionario(rows, pos_clave, pos_valor):
        """
        Crea un diccionario donde las claves son los id de cada registro, y el valor es el campo de busqueda, se utiliza
        por lo general para encontrar la clave principal de la lista de valores de un comboBox, la idea es evitar hacer
        consultas extras a la base de datos

        :param rows:
        :param pos_clave:
        :param pos_valor:
        :return:
        """
        if rows != None:
            diccionario ={}
            for i in rows:
                clave = i[pos_clave]
                valor = i[pos_valor]

                diccionario[clave] = valor
            return diccionario

    @staticmethod
    def crearDiccionarioTodosLosCampos(rows, pos_clave):
        """
        Crea un diccionario, toma como clave la columna dada por pos_clave, y como valor todos los campos

        :param rows:
        :param pos_clave:
        :return:
        """
        if rows != None:
            diccionario ={}
            for i in rows:
                clave = i[pos_clave]
                valor = i

                diccionario[clave] = valor
            return diccionario