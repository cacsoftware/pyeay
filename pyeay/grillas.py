# -*- coding: utf-8 -*-
import wx
from pyeay.formato import FormatearNumeros

class ManipularGrillas():

    @staticmethod
    def setCantidadColumnasGrilla(obj_grilla, columnas):
        """
        el parametro columna indica la nueva cantidad de columnas que tendra la grilla

        :param obj_grilla:
        :return: puntero_fila
        """

        cant_colsEliminar = obj_grilla.GetNumberCols()
        if cant_colsEliminar > 0:
            obj_grilla.DeleteCols(0, cant_colsEliminar)
        obj_grilla.InsertCols(0, columnas)

    @staticmethod
    def limpiarGrilla(obj_grilla):
        """

        :param obj_grilla:
        :return: puntero_fila
        """
        cant_filasEliminar = obj_grilla.GetNumberRows()
        if cant_filasEliminar > 0:
            obj_grilla.DeleteRows(0, cant_filasEliminar)
        obj_grilla.ClearGrid()
        puntero_fila = 0
        return puntero_fila

    @staticmethod
    def setCabecerasGrilla(obj_grilla, list_cabeceras):
        i=0
        for cabecera in list_cabeceras:
            obj_grilla.SetColLabelValue(i, cabecera)
            i+=1
        obj_grilla.AutoSizeColumns()

    @staticmethod
    def setColorGrisFilasEstadoTrueFalse(obj_grilla, col_true_false):
        filas = obj_grilla.GetNumberRows()
        cols = obj_grilla.GetNumberCols()

        COLOR_GRIS = wx.Colour(115, 155, 115)

        for i in range(filas):
            is_activo = obj_grilla.GetCellValue(i, col_true_false)
            if is_activo == 'False':
                for j in range(cols):
                    col_true_false.SetCellTextColour(i, j, COLOR_GRIS)


    @staticmethod
    def setColorFondoCeldaGrilla(obj_grilla, dic_color):
        """
        :param obj_grilla:
        :param dic_color: { 1: wx.RED} pone de Rojo la columna 1
        :return:
        """
        cant_filas = obj_grilla.GetNumberRows()
        for key in dic_color:
            for i in range(cant_filas):
                color = dic_color[key]
                obj_grilla.SetCellBackgroundColour(i, key, color)

    @staticmethod
    def setColumnasSoloLectura(obj_grilla, list_columnas):
        attr = wx.grid.GridCellAttr()
        attr.SetReadOnly(True)
        # attr.SetTextColour(wx.RED)
        for i in list_columnas:
            obj_grilla.SetColAttr(i, attr)
            attr.IncRef()  ## muy importante para evitar la asercion c++

    @staticmethod
    def setColumnasSoloNumeros(obj_grilla, list_columnas):
        for i in list_columnas:
            obj_grilla.SetColFormatNumber(i)

    @staticmethod
    def setColumnasFormatoCHK(obj_grilla, list_columnas):
        for i in list_columnas:
            obj_grilla.SetColFormatBool(i)  # PARA Q LA COLUMNA 5 CONTENGA CHECKBOX

    @staticmethod
    def convertirColumnasFormatoMilesConSimbolo(obj_grilla, list_columnas, signo):
        """
        Se utiliza para darle formato de numero con miles, a una lista de columnas de una grilla
        afecta todas las filas

        :param obj_grilla:
        :param list_columnas:
        :param signo:
        :return:
        """
        #formato_numeros = FormatearNumeros()


        cant_filas = obj_grilla.GetNumberRows()

        for j in list_columnas:
            for i in range(cant_filas):
                dato = obj_grilla.GetCellValue(i, j)
                dato = int(float(FormatearNumeros.toNumMilesSigno(dato, signo)))
                obj_grilla.SetCellValue(i, j, dato)

    @staticmethod
    def llenarGrilla(obj_grilla, rows):

        if rows == None:
            ManipularGrillas.limpiarGrilla(obj_grilla)
        if rows != None:
            ManipularGrillas.limpiarGrilla(obj_grilla)
            i = 0
            for fila in rows:
                # Se crea una unafila
                cant_filas = obj_grilla.GetNumberRows()
                obj_grilla.InsertRows(cant_filas, 1)
                j=0
                for dato in fila:
                    obj_grilla.SetCellValue(i, j, str(dato))
                    j += 1
                i += 1
            obj_grilla.AutoSizeColumns()

    @staticmethod
    def nuevaFilaGrilla(obj_grilla, row, puntero_fila):
        """
        :param obj_grilla:
        :param row:
        :param puntero_fila:
        :return: puntero_fila +1
        """
        # Se crea una unafila
        cant_filas = obj_grilla.GetNumberRows()
        obj_grilla.InsertRows(cant_filas, 1)

        j=0
        for dato in row:
            obj_grilla.SetCellValue(puntero_fila, j, str(dato))
            j += 1

        puntero_fila += 1

        obj_grilla.AutoSizeColumns()  # PARA AJUSTAR AUTOMATICAMENTE EL ANCHO DE LAS COLUMNAS

        return puntero_fila

    @staticmethod
    def nuevaFilaVaciaGrilla(obj_grilla, puntero_fila):
        """
        :param obj_grilla:
        :param row:
        :param puntero_fila:
        :return: puntero_fila +1
        """

        # Se crea una unafila
        cant_filas = obj_grilla.GetNumberRows()
        obj_grilla.InsertRows(cant_filas, 1)

        puntero_fila += 1

        obj_grilla.AutoSizeColumns()  # PARA AJUSTAR AUTOMATICAMENTE EL ANCHO DE LAS COLUMNAS

        return puntero_fila

    @staticmethod
    def nuevaColumnaVaciaGrilla(obj_grilla, puntero_columna):
        """
        :param obj_grilla:
        :param puntero_columna:
        :return: puntero_columna +1
        """
        # Se crea una una columna
        cant_columnas = obj_grilla.GetNumberCols()
        obj_grilla.InsertCols(cant_columnas, 1)

        puntero_columna += 1

        obj_grilla.AutoSizeColumns()  # PARA AJUSTAR AUTOMATICAMENTE EL ANCHO DE LAS COLUMNAS

        return puntero_columna

    @staticmethod
    def delFilasCHK(obj_grilla, puntero_col):
        """
        :param obj_grilla:
        :param puntero_col:
        :return: puntero_fila
        """
        cant_filas = obj_grilla.GetNumberRows()
        cant_cols = obj_grilla.GetNumberCols()
        rows = []
        for i in range(cant_filas):
            fila = []
            for j in range(cant_cols):
                if obj_grilla.GetCellValue(i, puntero_col) == '':
                    dato = obj_grilla.GetCellValue(i,j)
                    fila.append(dato)
            if fila != []:
                rows.append(fila)
        ManipularGrillas.limpiarGrilla(obj_grilla)
        puntero_fila = ManipularGrillas.llenarGrilla(obj_grilla, rows)

        puntero_fila = len(rows)
        if puntero_fila < 0:
            puntero_fila = 0

        return puntero_fila

    @staticmethod
    def deseleccionarFilasCHK(obj_grilla, puntero_col):
        """
        :param obj_grilla:
        :param puntero_col:
        :return:
        """
        cant_filas = obj_grilla.GetNumberRows()

        for i in range(cant_filas):
            if obj_grilla.GetCellValue(i, puntero_col) != '':
                obj_grilla.SetCellValue (i, puntero_col, '')

    @staticmethod
    def delFila(obj_grilla, puntero_fila):
        """
        :param obj_grilla:
        :param puntero_col:
        :return: puntero_fila
        """
        cant_filas = obj_grilla.GetNumberRows()
        cant_cols = obj_grilla.GetNumberCols()
        rows = []
        for i in range(cant_filas):
            fila = []
            for j in range(cant_cols):
                if i != puntero_fila:
                    dato = obj_grilla.GetCellValue(i, j)
                    fila.append(dato)
            if fila != []:
                rows.append(fila)
        ManipularGrillas.limpiarGrilla(obj_grilla)
        puntero_fila = ManipularGrillas.llenarGrilla(obj_grilla, rows)

        puntero_fila = len(rows)
        if puntero_fila < 0:
            puntero_fila = 0

        return puntero_fila

    @staticmethod
    def delColumna(obj_grilla, puntero_Columna):
        """
        :param obj_grilla:
        :param puntero_col:
        :return: puntero_fila
        """
        cant_filas = obj_grilla.GetNumberRows()
        cant_cols = obj_grilla.GetNumberCols()
        rows = []
        labelsRows = []

        for i in range(cant_filas):
            fila = []
            for j in range(cant_cols):
                if j != puntero_Columna:
                    dato = obj_grilla.GetCellValue(i, j)
                    fila.append(dato)
            if fila != []:
                rows.append(fila)

        for j in range(cant_cols):
            if j != puntero_Columna:
                dato_label = obj_grilla.GetColLabelValue(j)
                labelsRows.append(dato_label)

        ManipularGrillas.setCantidadColumnasGrilla(obj_grilla, cant_cols - 1)
        puntero_fila = ManipularGrillas.llenarGrilla(obj_grilla, rows)

        cant_cols = len(labelsRows)
        for j in range(cant_cols):
            obj_grilla.SetColLabelValue(j, labelsRows[j])

        puntero_Columna = cant_cols
        return puntero_Columna

    @staticmethod
    def ordenarGrillaPorColumna(obj_grilla, puntero_Columna, list_tipoColumna, is_orden_ascendente=True):
        """
        :param obj_grilla:
        :param puntero_col:
        :return: puntero_fila
        """
        cant_filas = obj_grilla.GetNumberRows()
        cant_cols = obj_grilla.GetNumberCols()
        rows = []
        labelsRows = []

        tipo_columna = list_tipoColumna[puntero_Columna]

        for i in range(cant_filas):
            fila = []
            for j in range(cant_cols):
                if j == puntero_Columna:
                    if tipo_columna == 'int':
                        dato = int(obj_grilla.GetCellValue(i, j))
                    if tipo_columna == 'float':
                        dato = float(obj_grilla.GetCellValue(i, j))
                    if tipo_columna == 'str':
                        dato = obj_grilla.GetCellValue(i, j)
                else:
                    dato = obj_grilla.GetCellValue(i, j)
                fila.append(dato)
            if fila != []:

            ## invertir orden
                rows.append(fila)

        rows = sorted(rows, key=lambda a_entry: a_entry[puntero_Columna], reverse= is_orden_ascendente)

        puntero_fila = ManipularGrillas.llenarGrilla(obj_grilla, rows)

    @staticmethod
    def reemplazarValorCeldaGrilla(obj_grilla, cad_buscar='None', cad_reemplazar_con='0'):
        filas = obj_grilla.GetNumberRows()
        cols = obj_grilla.GetNumberCols()

        for i in range(filas):
            for j in range(cols):
                if obj_grilla.GetCellValue(i, j) == cad_buscar:
                    obj_grilla.SetCellValue(i, j, cad_reemplazar_con)

    @staticmethod
    def ocultarColumnasGrilla(obj_grilla, list_columnas):
        for i in list_columnas:
            obj_grilla.HideCol(i)