# -*- coding: utf-8 -*-

from datetime import date, datetime

class ManejoFechasHoras():

    @staticmethod
    def getFechaHoraActual():
        """
        Devuelve fecha, hora  sirve hacer transacciones SQL

        :return: fecha, hora
        """

        fecha = date.today()
        hora = datetime.now()

        fecha = date.strftime(fecha, ' %d/%m/%Y')

        hora_transacion = str(hora.hour) + ':' + str(hora.minute) + ':' + str(hora.second)

        return fecha, hora_transacion

    @staticmethod
    def getDiaSemanaToNumero(obj_control_date):
        """
        trabaja con el control wx.datePicker

        :param obj_control_date:
        :return: un numero que indica el dia de la semana 0 lunes, 1 martes ...
        """

        fecha = obj_control_date.GetValue()

        dia_semana = fecha.GetWeekDay()
        ## weekday devuelve un numero que indica el dia de la semana 1 lunes, 2 martes ...

        return dia_semana

    @staticmethod
    def formatearFechaXSql(obj_control_date):
        """
        trabaja con el control wx.datePicker

        :param obj_control_date:
        :return: una cadena con el formato dia/mes/año lista para se incluida en una transaccion SQL
        """

        fecha = obj_control_date.GetValue()
        fecha_formateada = fecha.Format("%d/%m/%y")
        return fecha_formateada

    @staticmethod
    def formatearHoraXSql(obj_timePicker):
        """
        trabaja con el control wx.timePicker

        :param obj_timePicker
        :return: una cadena con el formato 05:25:37  lista para se incluida en una transaccion SQL
        """

        hora = obj_timePicker.GetValue()
        hora_formateada = hora.Format("%H:%M:%S")
        return hora_formateada