# -*- coding: utf-8 -*-
import uuid
import socket
import urllib.request

class Red():
	nombre_equipo = 0
	ip_lan = 0
	dir_mac = 0
	ip_publica = ''

	def __init__(self):
		self.getPublicIP()
		self.getInfoEquipo()

	def getPublicIP(self):
		# Solicitamos a 'icanhazip.com' nuestra IP pública y la devolvemos
		self.ip_publica = str(urllib.request.urlopen('http://icanhazip.com').read())
		self.ip_publica = self.ip_publica[2:-3]

	def getInfoEquipo(self):
		self.nombre_equipo = socket.gethostname()
		self.ip_lan = socket.gethostbyname(self.nombre_equipo)
		self.dir_mac = hex(uuid.getnode())

if __name__ == '__main__':

	obj_red = Red()

	print('Nombre del equipo:', obj_red.nombre_equipo)
	print('ip_lan:', obj_red.ip_lan)
	print('Dir mac:', obj_red.dir_mac)
	print('ip_publica:', obj_red.ip_publica)
