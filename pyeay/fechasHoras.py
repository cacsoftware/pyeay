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

    @staticmethod
    def cantidadSegundosEntre2Fechas(obj_control_date1, obj_control_date2, obj_timePicker1=-1, obj_timePicker2=-1):
        """
		trabaja con el control wx.timePicker

		:param obj_timePicker
		:return: la cantidad de segundos entre dos fechas
		"""

        hora1 = obj_timePicker1.GetValue()
        hora2 = obj_timePicker2.GetValue()
        fecha1 =obj_control_date1.GetValue()
        fecha2 = obj_control_date2.GetValue()

        if obj_timePicker1 == -1:
            hora_1 = 0
            minuto_1 = 0
            segundo_1 = 0
        else:
            hora_1 = hora1.hour
            minuto_1 = hora1.minute
            segundo_1 = hora1.second
        anyo_1 = fecha1.year
        mes_1 = fecha1.month
        dia_1 = fecha1.day

        if obj_timePicker2 == -1:
            hora_2 = 0
            minuto_2 = 0
            segundo_2 = 0
        else:
            hora_2 = hora2.hour
            minuto_2 = hora2.minute
            segundo_2 = hora2.second
        anyo_2 = fecha2.year
        mes_2 = fecha2.month
        dia_2 = fecha2.day

        la_fecha1 = datetime(anyo_1, mes_1 + 1, dia_1, hora_1, minuto_1, segundo_1)
        la_fecha2 = datetime(anyo_2, mes_2 + 1, dia_2, hora_2, minuto_2, segundo_2)

        diferencia = la_fecha2 -la_fecha1

        return diferencia.seconds + (diferencia.days * 24 * 3600)
