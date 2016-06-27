#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importamos la librería
import pygame

import sys

# Importamos constantes locales de pygame
from pygame.locals import *

from aux import *


sprites_serp = pygame.sprite.Group()
 # Establecemos el largo y alto de cada segmento de la serpiente
largodel_segmento = 10
altodel_segmento = 10
# Margen entre cada segmento
margendel_segmento = 3
#rectangulo delimitador
recta = pygame.Rect(0, 50, 958, 640-52)


class Game:
	def __init__(self,Screen):
		self.Screen = Screen
		recta = pygame.Rect(0, 50, self.Screen.get_width()-2, self.Screen.get_height()-52)
		self.black_screen()
		self.serpiente = Serpiente()
		#direcciones de la serpiente: 0: abajo 1:dcha 2: arriba 3:izda
		self.direction= 1
		pygame.display.flip()


	def black_screen(self):
		self.Screen.fill(NEGRO)
		self.Screen.fill(EGG,recta)

		pygame.draw.rect(self.Screen, BLANCO, recta, 2)
		pygame.display.flip()
	def mover(self,dir):
		# Eliminamos el último segmento de la serpiente
		# .pop() este comando elimina el último objeto de una lista.
		self.serpiente.mover(dir)
		self.black_screen()
		sprites_serp.draw(self.Screen)


class Segmento(pygame.sprite.Sprite):
	""" Clase que representa un segmento de la serpiente. """
	# -- Métodos
	#  Función constructor
	def __init__(self, x, y):
		# Llamada al constructor padre
		pygame.sprite.Sprite.__init__(self)
		  
		# Establecemos el alto y largo
		self.image = pygame.Surface([largodel_segmento, altodel_segmento])
		self.image.fill(BLANCO)
  
		# Establecemos como punto de partida la esquina superior izquierda.
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Serpiente():
	def __init__(self):
		#Velocidad inicial
		self.cambio_x = largodel_segmento + margendel_segmento
		self.cambio_y = 0
		# Creamos la serpiente inicial.
		ini_x = 300
		ini_y = 300
		self.segmentos_serpiente = []
		for i in range(5):
			x = ini_x - (largodel_segmento + margendel_segmento) * i
			y = ini_y
			segmento = Segmento(x, y)
			self.segmentos_serpiente.append(segmento)
			sprites_serp.add(segmento)
	def mover(self,dirs):
		check = True
		if dirs == 3:
			cambio_x = (largodel_segmento + margendel_segmento) * -1
			cambio_y = 0
		if dirs == 1:
			cambio_x = (largodel_segmento + margendel_segmento)
			cambio_y = 0
		if dirs == 2:
			cambio_x = 0
			cambio_y = (altodel_segmento + margendel_segmento) * -1
		if dirs == 0:
			cambio_x = 0
			cambio_y = (altodel_segmento + margendel_segmento)


		# Determinamos dónde aparecerá el nuevo segmento
		x = self.segmentos_serpiente[0].rect.x + cambio_x
		y = self.segmentos_serpiente[0].rect.y + cambio_y		
		if not recta.collidepoint(x,y):
			print 'choca' 
			check = False
		else:
			segmento_viejo = self.segmentos_serpiente.pop()
			sprites_serp.remove(segmento_viejo)
			segmento = Segmento(x, y)
			# Insertamos un nuevo segmento en la lista
			self.segmentos_serpiente.insert(0, segmento)
			sprites_serp.add(segmento)
		print check
		return check

