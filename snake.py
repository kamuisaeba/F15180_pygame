#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importamos la librería
import pygame

import sys
import random
from math import sqrt,exp

# Importamos constantes locales de pygame
from pygame.locals import *

from aux import *


sprites_serp = pygame.sprite.Group()
manzanas = pygame.sprite.Group()

 # Establecemos el largo y alto de cada segmento de la serpiente
largodel_segmento = 10
altodel_segmento = 10
# Margen entre cada segmento
margendel_segmento = 1
#rectangulo delimitador
recta = pygame.Rect(0, 50, 958, 640-52)


class Game:
	def __init__(self):
		Screen = pygame.display.get_surface()
		self.ancho_col = 5
		self.x_ini=self.ancho_col
		self.x_fin= Screen.get_width()-(self.ancho_col*2)
		self.y_ini = 50
		self.y_fin = Screen.get_height()-self.y_ini-(self.ancho_col*2)
		recta = pygame.Rect(self.x_ini, self.y_ini, self.x_fin, self.y_fin)
		self.score = 0
		self.level = 1
		self.direction = 1
		#sprites_serp.clear(pygame.display.get_surface(),pygame.display.get_surface())
		self.score_img = load_image('./assets/images/puntuacion.png', (150,40),True)	
		self.level_img = load_image('./assets/images/nivel.png', (150,40),True)	

		self.serpiente = Serpiente()
		self.nuevaManzana()
		pygame.display.flip()

		#direcciones de la serpiente: 0: abajo 1:dcha 2: arriba 3:izda
		self.state = 'JUEGO'
		self.score = 0

	def wait_for_key(self):
		message = 'PULSE UNA TECLA PARA CONTINUAR'
		self.black_screen(message)
		pygame.event.clear()
		wait = True
		while wait:
			evento = pygame.event.wait()
			if evento.type == KEYDOWN and evento.key != K_ESCAPE:
				if evento.key == K_UP and self.direction != 0: self.direction = 2
				elif evento.key == K_DOWN and self.direction != 2: self.direction = 0
				elif evento.key == K_LEFT and self.direction != 1: self.direction = 3
				elif evento.key == K_RIGHT and self.direction != 3:self.direction = 1
				print self.direction
				wait = False

	def continuar(self):
		self.wait_for_key()
		return self.direction

	def new(self):
		self.score = 0
		self.level = 1
		self.serpiente.destroy()
		self.serpiente = Serpiente()
		self.nuevaManzana()
		self.wait_for_key()
		return self.direction


	def get_score(self):
		return self.score

	def get_level(self):
		return self.level
	def puntosNecesarios(self):
		constant = 0.1
		return round(pow(self.level,2) / constant)

	def black_screen(self,message=None):
		Screen = pygame.display.get_surface()
		Screen.fill(NEGRO)
		Screen.fill(EGG,recta)
		Screen.blit(self.score_img,(5,5))
		Screen.blit(self.level_img,(155,5))
		fuente= pygame.font.SysFont('Impact', 25)
		score = fuente.render(str(self.score), 1, BLANCO)
		Screen.blit(score,(30,8))
		level = fuente.render(str(self.level), 1, BLANCO)
		Screen.blit(level,(230,8))
		pygame.draw.rect(Screen, BLANCO, recta, self.ancho_col)
		sprites_serp.draw(pygame.display.get_surface())
		manzanas.draw(pygame.display.get_surface())
		if message:
			message = fuente.render(message, 1, NEGRO)
			Screen.blit(message,(300,300))

		pygame.display.flip()

	def mover(self,dir):
		self.direction = dir
		self.state = self.serpiente.mover(dir)
		if self.state == 'SUMA':
			self.sumapunto()
		self.black_screen()
		return self.state
	def gameover(self):
		self.serpiente.destroy()
	def sumapunto(self):
		self.score = self.score + 1
		if self.score == self.puntosNecesarios():
			self.levelup()
		self.nuevaManzana()
		self.state = 'JUEGO'
	def levelup(self):
		self.level = self.level+1

	def nuevaManzana(self):
		for i in range (random.randint(1, 3)):
			if len(manzanas) < 3:
				x =random.randint(self.x_ini+largodel_segmento, self.x_fin-largodel_segmento)
				y =random.randint(self.y_ini+altodel_segmento, self.y_fin-altodel_segmento)
				manzanas.add(Manzana(x,y))



class Segmento(pygame.sprite.Sprite):
	""" Clase que representa un segmento de la serpiente. """
	# -- Métodos
	#  Función constructor
	def __init__(self, x, y,head=False):
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

		for i in range(3):
			x = ini_x - (largodel_segmento + margendel_segmento) * i
			y = ini_y
			if i == 0:
				segmento = Segmento(x, y,True)
			else:
				segmento = Segmento(x, y)
			self.segmentos_serpiente.append(segmento)
			sprites_serp.add(segmento)
	def mover(self,dirs):
		state = 'JUEGO'
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
		segmento = Segmento(x, y)
		if not recta.collidepoint(x,y) or len(pygame.sprite.spritecollide(segmento, sprites_serp, False)) > 0:
			state = 'GAMEOVER'
		elif len(pygame.sprite.groupcollide(sprites_serp, manzanas, False, True)) > 0 :
			state = 'SUMA'
		else:
			segmento_viejo = self.segmentos_serpiente.pop()
			sprites_serp.remove(segmento_viejo)
		# Insertamos un nuevo segmento en la lista
		self.segmentos_serpiente.insert(0, segmento)
		if state != 'GAMEOVER':
			sprites_serp.add(segmento)
		else:
			self.destroy()
		return state
	def destroy(self):
		del self.segmentos_serpiente[:]
		sprites_serp.empty()
		sprites_serp.remove()
		manzanas.empty()
		manzanas.remove()

class Manzana(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		# Establecemos el alto y largo
		#self.image = pygame.Surface([largodel_segmento, altodel_segmento])
		#self.image.fill(RED)  
		self.image = load_image('./assets/images/apple.png',(largodel_segmento, altodel_segmento),True)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self,x,y):
		self.rect.x = x
		self.rect.y = y
	#Add this draw function so we can draw individual sprites
	def draw(self,screen):
		screen.blit(self.image, self.rect)




