# -*- coding: utf-8 -*-

import sqlite3
import os
import psycopg2
import psycopg2.extras

def crearConexionDB(dbalias):
	# En la carpeta raiz del proyecto se debe crear una carpeta llamada dbcac y que contenga la base de datos
	# sqlite llamada dbCAC.sqlite
	cadConexion = os.path.join(os.getcwd(), 'pyeay', 'dbcac', 'dbCAC.sqlite')

	#print(cadConexion)

	conn = sqlite3.connect(cadConexion)
	conn.row_factory = sqlite3.Row  ## para trabajar con los nombre de columna al retornar  las consultas
	cur = conn.cursor()

	cad_sql = """
				SELECT *
				FROM bases_de_datos	
				WHERE dbalias = '{0}' AND activo = 1
				""".format(dbalias)

	cur.execute(cad_sql)
	rows = cur.fetchone()

	if rows != None:
		tipo_base_datos = rows['tipo_base_datos']

		if tipo_base_datos == 'postgresql':
			dbname = rows['dbname']
			usuario = rows['usuario']
			password = rows['password']
			host = rows['host']
			puerto = rows['puerto']

			cadConexion = "dbname={0} user={1} password={2}  host= {3} port={4}".format( dbname, usuario, password, host, puerto)

			print(dbname,  'conectado a: ', host)
			conn = psycopg2.connect(cadConexion)
			cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

			return conn, cur

		if tipo_base_datos == 'sqlite':
			dbname = rows['dbname']
			ubicacion = rows['ubicacion']
			cadConexion = os.path.join(ubicacion,  dbname)

			conn = sqlite3.connect(ubicacion)
			conn.row_factory = sqlite3.Row  ## para trabajar con los nombre de columna al retornar  las consultas
			cur = conn.cursor()
	else:
		print('la base de datos no existe, debes registrarla en dbCAC.sqlite')

	cur.close()
	conn.close()


class Ejecutar_SQL():

	@staticmethod
	def select_varios_registros(cad_sql, nom_funcion, cant_registros, dbalias):
		conn, cur = crearConexionDB(dbalias)
		cur.execute(cad_sql)
		rows = cur.fetchmany(cant_registros)
		cur.close()
		conn.close()
		return rows

	@staticmethod
	def select_un_registro(cad_sql, nom_funcion, dbalias):
		conn, cur = crearConexionDB(dbalias)
		cur.execute(cad_sql)
		rows = cur.fetchone()
		cur.close()
		conn.close()
		return rows

	@staticmethod
	def insert_filas(cad_sql, nom_funcion, dbalias):
		conn, cur = crearConexionDB(dbalias)

		try:
			cur.execute(cad_sql)
			conn.commit()
			cur.close()
			conn.close()

			valor_retorno = 1

		except psycopg2.Error as error:
			print(u' ***  No hemos podido  Insertar datos desde la función : {}()'.format(nom_funcion))
			print(u'    Falla --> : ', error)
			valor_retorno = 0

		return valor_retorno

	@staticmethod
	def update_filas(cad_sql, nom_funcion, dbalias):
		conn, cur = crearConexionDB(dbalias)

		try:
			cur.execute(cad_sql)
			conn.commit()
			cur.close()
			conn.close()

			valor_retorno = 1

		except psycopg2.Error as error:
			print(u' ***  No hemos podido  Actualizar datos desde la función : {}()'.format(nom_funcion))
			print(u'    Falla --> : ', error)
			valor_retorno = 0

		return valor_retorno


class GenerarSql():

	@staticmethod
	def crearMultiInsertSql(nom_tabla, dic_campos, list_valores):
		"""
		:param nom_tabla:
		:param dic_campos: Eel estilo {´nom_empleado': 'str', 'cant':'int'}
		:param list_valores: Es una lista de listas     [[], [], []]
		:return: Un string con la Sentencia SQL completa
		"""

		cad_campos = ''
		cad_valores = ''

		list_campos = dic_campos.keys()
		list_tipo_campos = list(dic_campos.values())

		for i in list_campos:
			cad_campos += str(i) + ', '
		cad_campos = cad_campos[:-2]

		for fila in list_valores:
			i = 0
			cad_valores += '('
			for dato in fila:
				tipo_dato = list_tipo_campos[i]
				if tipo_dato == 'str':
					cad_valores += "'" + str(dato) + "', "
				if tipo_dato == 'int':
					cad_valores += str(dato) + ", "
				i += 1
			cad_valores = cad_valores[:-2]
			cad_valores += '), '

		cad_valores = cad_valores[:-2]
		sSql = ' INSERT INTO {0} ( {1} ) VALUES {2}'.format(nom_tabla, cad_campos, cad_valores)

		return sSql

	@staticmethod
	def crearMultiUpdateSql(nom_tabla, rows, cols_busqueda, cols_a_modificar, nom_campos, tipo_campos):
		"""
				EJEMPLO

				nom_tabla = 'producto'

				nom_campos = ['id', 'marca', 'ref', 'color', 'precio_detal', 'precio_mayor']

				tipo_campos = ['int', 'str', 'str', 'str', 'int', 'int']

				rows = [
							['1', 'AEROFLEX', '1609', 'GRIS', '500', '1000'],
							['2', 'AEROFLEX', '8801', 'ROJO', '600', '1200'],
							['3', 'AEROFLEX', 'J2268', 'NARANJADO', '400', '800'],
							['4', 'AEROFLEX', 'R328', 'VERDE', '550', '1100']
						]

				cols_busqueda = [1, 2, 3]
				cols_a_modificar = [4, 5]

				RESULTADO

				UPDATE producto SET
						precio_detal = CASE
											WHEN marca = 'AEROFLEX' AND ref = '1609' AND color = 'GRIS'  THEN 500
											WHEN marca = 'AEROFLEX' AND ref = '8801' AND color = 'ROJO'  THEN 600
											WHEN marca = 'AEROFLEX' AND ref = 'J2268' AND color = 'NARANJADO'  THEN 400
											WHEN marca = 'AEROFLEX' AND ref = 'R328' AND color = 'VERDE'  THEN 550
										END,
						precio_mayor = CASE
											WHEN marca = 'AEROFLEX' AND ref = '1609' AND color = 'GRIS'  THEN 1000
											WHEN marca = 'AEROFLEX' AND ref = '8801' AND color = 'ROJO'  THEN 1200
											WHEN marca = 'AEROFLEX' AND ref = 'J2268' AND color = 'NARANJADO'  THEN 800
											WHEN marca = 'AEROFLEX' AND ref = 'R328' AND color = 'VERDE'  THEN 1100
										END
				WHERE 	marca IN (AEROFLEX, AEROFLEX, AEROFLEX, AEROFLEX)  AND
						ref IN (1609, 8801, J2268, R328)  AND
						color IN (GRIS, ROJO, NARANJADO, VERDE)

				"""

		cad = ''
		cad_WHEN = ''
		cad_CASE = ''

		for i in cols_a_modificar:
			## craear un   CASE ... END,
			cad_WHEN = ''
			for fila in rows:
				## crear un   WHEN  ...  THEN
				cad = ''
				for k in cols_busqueda:
					## enlazamos con AND cada comparacion   por ejemplo  ref = 'R155'  AND color = 'NEGRO'
					nomCampo = nom_campos[k]
					tipoCampo = tipo_campos[k]
					dato = fila[k]
					if tipoCampo == 'str':
						dato = "'" + dato + "'"
					cad += nomCampo + " = " + str(dato) + " AND "
				cad = cad[:-4]

				valor = fila[i]
				tipoCampo = tipo_campos[i]
				if tipoCampo == 'str':
					valor = "'" + valor + "'"
				cad_WHEN += ' WHEN ' + cad + ' THEN ' + str(valor) + '  '

			nomCampo = nom_campos[i]
			cad_CASE += nomCampo + ' = CASE ' + cad_WHEN + ' END,'

		cad_CASE = cad_CASE[:-1]

		sSql = 'UPDATE ' + nom_tabla + ' SET ' + cad_CASE

		cad_WHERE = ''
		for j in cols_busqueda:
			nomCampo = nom_campos[j]
			cad_WHERE += nomCampo + ' IN ('
			for fila in rows:
				dato = fila[j]
				tipoCampo = tipo_campos[j]
				if tipoCampo == 'str':
					dato = "'" + dato + "'"
				cad_WHERE += str(dato) + ', '
			cad_WHERE = cad_WHERE[:-2] + ')  AND '

		cad_WHERE = cad_WHERE[:-4]

		sSql = 'UPDATE ' + nom_tabla + ' SET ' + cad_CASE + ' WHERE ' + cad_WHERE

		return sSql

	@staticmethod
	def crearMultiUpdateSql_operaciones(nom_tabla, rows, cols_busqueda, cols_a_modificar, nom_campos, tipo_campos, dic_operaciones = {}):
		"""
				EJEMPLO

				nom_tabla = 'producto'

				nom_campos = ['id', 'marca', 'ref', 'color', 'precio_detal', 'precio_mayor']

				tipo_campos = ['int', 'str', 'str', 'str', 'int', 'int']

				rows = [
							['1', 'AEROFLEX', '1609', 'GRIS', '500', '1000'],
							['2', 'AEROFLEX', '8801', 'ROJO', '600', '1200'],
							['3', 'AEROFLEX', 'J2268', 'NARANJADO', '400', '800'],
							['4', 'AEROFLEX', 'R328', 'VERDE', '550', '1100']
						]

				cols_busqueda = [1, 2, 3]
				cols_a_modificar = [4, 5]

				RESULTADO

				UPDATE producto SET
						precio_detal = CASE
											WHEN marca = 'AEROFLEX' AND ref = '1609' AND color = 'GRIS'  THEN 500
											WHEN marca = 'AEROFLEX' AND ref = '8801' AND color = 'ROJO'  THEN 600
											WHEN marca = 'AEROFLEX' AND ref = 'J2268' AND color = 'NARANJADO'  THEN 400
											WHEN marca = 'AEROFLEX' AND ref = 'R328' AND color = 'VERDE'  THEN 550
										END,
						precio_mayor = CASE
											WHEN marca = 'AEROFLEX' AND ref = '1609' AND color = 'GRIS'  THEN 1000
											WHEN marca = 'AEROFLEX' AND ref = '8801' AND color = 'ROJO'  THEN 1200
											WHEN marca = 'AEROFLEX' AND ref = 'J2268' AND color = 'NARANJADO'  THEN 800
											WHEN marca = 'AEROFLEX' AND ref = 'R328' AND color = 'VERDE'  THEN 1100
										END
				WHERE 	marca IN (AEROFLEX, AEROFLEX, AEROFLEX, AEROFLEX)  AND
						ref IN (1609, 8801, J2268, R328)  AND
						color IN (GRIS, ROJO, NARANJADO, VERDE)

				"""

		cad = ''
		cad_WHEN = ''
		cad_CASE = ''

		for i in cols_a_modificar:
			## craear un   CASE ... END,
			cad_WHEN = ''
			for fila in rows:
				## crear un   WHEN  ...  THEN
				cad = ''
				for k in cols_busqueda:
					## enlazamos con AND cada comparacion   por ejemplo  ref = 'R155'  AND color = 'NEGRO'
					nomCampo = nom_campos[k]
					tipoCampo = tipo_campos[k]
					dato = fila[k]
					if tipoCampo == 'str':
						dato = "'" + dato + "'"
					cad += nomCampo + " = " + str(dato) + " AND "
				cad = cad[:-4]

				valor = fila[i]
				tipoCampo = tipo_campos[i]
				if tipoCampo == 'str':
					valor = "'" + valor + "'"
				if dic_operaciones == {}:
					cad_WHEN += ' WHEN ' + cad + ' THEN '  + str(valor) + '  '
				else:
					cad_WHEN += ' WHEN ' + cad + ' THEN ' + dic_operaciones[nom_campos[i]] + ' ' + str(valor) + '  '

			nomCampo = nom_campos[i]
			cad_CASE += nomCampo + ' = CASE ' + cad_WHEN + ' END,'

		cad_CASE = cad_CASE[:-1]

		sSql = 'UPDATE ' + nom_tabla + ' SET ' + cad_CASE

		cad_WHERE = ''
		for j in cols_busqueda:
			nomCampo = nom_campos[j]
			cad_WHERE += nomCampo + ' IN ('
			for fila in rows:
				dato = fila[j]
				tipoCampo = tipo_campos[j]
				if tipoCampo == 'str':
					dato = "'" + dato + "'"
				cad_WHERE += str(dato) + ', '
			cad_WHERE = cad_WHERE[:-2] + ')  AND '

		cad_WHERE = cad_WHERE[:-4]

		sSql = 'UPDATE ' + nom_tabla + ' SET ' + cad_CASE + ' WHERE ' + cad_WHERE

		return sSql