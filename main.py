#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importamos la librería
import pygame
import random

import sys,string

# Importamos constantes locales de pygame
from pygame.locals import *

import aux
from menu import *
from snake import *
from database import GameConfig

def load_music(music,music_file):
	if music is True:
		pygame.mixer.music.load(music_file)
		pygame.mixer.music.play(-1)
	else:
		pygame.mixer.music.stop()


def hall(gameconfig,posicion=None):
	hall_image_file =  './assets/images/ranking.png'
	surface = pygame.display.get_surface()
	surface_w = surface.get_width()
	surface_h = surface.get_height()
	surface.fill(NEGRO)

	image = load_image(hall_image_file,size=(surface_w -70 , surface_h - 50),opacity=100)
	image_cerrar_b = aux.load_image('./assets/images/b_default.png',(200,75),True)
	background =  aux.load_image('./assets/images/backMenu.png',( surface_w , surface_h))

	surface.blit(background, (0,0))  
	surface.blit(image,(50,10))
	ranking = gameconfig.populate_ranking()
	fuente= pygame.font.SysFont('Impact', 25)
	r_x = -100
	r_y = 0
	for i,a in enumerate(ranking):
		if i % 6 == 0:
			r_x = r_x + 250
			r_y = 200
		print a
		message = "%d. %s : %d (%d)"% (i+1,a['user'],a['score'],a['level'])
		if posicion and posicion == (i+1):
			user = fuente.render(str(message), 1, NEGRO)
		else:
			user = fuente.render(str(message), 1, BLANCO)
		surface.blit(user,(r_x,r_y))
		r_y = r_y + 50
	surface.blit(image_cerrar_b,(image.get_rect().centerx-50,surface_h-150))
	surface.blit(fuente.render('CERRAR', 1, BLANCO),(image.get_rect().centerx,surface_h-130))
	return 'HALL'

def back_menu_draw(music_c,sound_c):
	if music_c is True: music_image_file =  './assets/images/musicon.png'
	else: music_image_file =  './assets/images/musicoff.png'
	if sound_c is True: sound_image_file =  './assets/images/soundon.png'
	else: sound_image_file =  './assets/images/soundoff.png'
	music =  aux.load_image(music_image_file,transparent=True)
	sound =  aux.load_image(sound_image_file,transparent=True)
	hall = aux.load_image('./assets/images/hall.png',transparent=True)
	background =  aux.load_image('./assets/images/backMenu.png',( SCREEN_WIDTH, SCREEN_HEIGHT))
	Screen.fill(BLANCO)
	Screen.blit(background, (0,0)) 
	Screen.blit(music,(10,10))
	Screen.blit(sound,(70,10))
	Screen.blit(hall,(130,10))
 
def get_key():
	while 1:
		event = pygame.event.poll()
		if event.type == KEYDOWN:
			return event.key
		else:
			pass

def display_box(message):
	fuente= pygame.font.SysFont('Impact', 18)
	screen = pygame.display.get_surface()
	w = (screen.get_width()/2)-100
	h = (screen.get_height()/2)-10
	pygame.draw.rect(Screen,NEGRO,(w,h,200,20))
	pygame.draw.rect(Screen,BLANCO,(w-2,h-2,204,24),1)
	screen.blit(fuente.render(message, 1, BLANCO),(w,h))

	pygame.display.flip()

def ask():
	current_string=[]
	question = 'nombre(max 10): '
	display_box(question +string.join(current_string,""))
	while 1:
		inkey = get_key()
		if inkey == K_BACKSPACE:
			current_string = current_string[0:-1]
		elif inkey == K_RETURN:
			break
		elif inkey <= 127 and len(current_string) < 10:
			current_string.append(chr(inkey))
		elif len(current_string) == 10 and sound_c:
			error_sound.play()
		display_box(question + string.join(current_string,""))

	return string.join(current_string,"")


# Iniciamos Pygame
pygame.init()

#conexion a base datos
gameconfig = GameConfig()
sound_c = gameconfig.get_sound()
music_c = gameconfig.get_music()
ranking_limit = gameconfig.get_ranking_limit()



# Creamos una surface (la ventana de juego), asignándole un ancho y un alto
SCREEN_WIDTH=960
SCREEN_HEIGHT=640
pygame.init()
Screen = pygame.display.set_mode( (SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('SNAKE!!!')
music_file = './assets/sound/gamePlay.mp3'
load_music(music_c,music_file)

# Elegimos la fuente y el tamaño
Fuente= pygame.font.SysFont('Impact', 45)

back_menu_draw(music_c,sound_c)
load_music(music_c,music_file)

menu_items = (
	#{'message':'CONTINUAR','action':'continuar'}, 
	{'message':'NUEVO','action':'nuevo'},
	{'message':'SALIR','action':'salir'})
gameMenu = Menu(100,50,menu_items)
gameMenu.draw()

serpi =  aux.load_image('./assets/images/serpi.png',(260,210),True)




# refresca los gráficos
pygame.display.flip()

# Bucle infinito para mantener el programa en ejecución
clock = pygame.time.Clock()
state ='MENU'
direction = 1
ticks = 10
ticks_inicial = 10
gamePlay = Game()

while True:
	# Manejador de estados
	clock.tick(ticks)
	'''
	ESTADOS DEL JUEGO
	0: MENU INICIAL
	1: JUGANDO
	2: JUEGO PAUSADO
	3: GAME OVER
	'''
	if state =='JUEGO' and gamePlay.mover(direction) == 'GAMEOVER':
			if sound_c == True:
				gameover_sound.play()
			gamePlay.gameover()
			state = 'GAMEOVER' #game over
			range_ranking = gameconfig.get_range_ranking()
			score = gamePlay.get_score()
			level =gamePlay.get_level()
			if score > 0 and (range_ranking['count'] < ranking_limit or range_ranking['min'] < score):
				user = ask()
				if user == '':
					user = 'anonymous'
				position = gameconfig.insert_ranking(user,score,level)
				state = hall(gameconfig,position)
			else:
				menu_items = (
					{'message':'NUEVO','action':'nuevo'},
					{'message':'SALIR','action':'salir'})
				gameOverMenu = Menu(100,50,menu_items)


	# if state == 'MENU':
	#     print 'MENU'
	# if state == 'JUEGO':
	#     print 'JUEGO'
	# if state == 'PAUSA':
	#     print 'PAUSADO'

	for evento in pygame.event.get():
		if evento.type == QUIT:
			pygame.quit()
			sys.exit()
		#eventos del menu
		if state =='MENU':
			#eventos de seleccion de botones extra (50*50)
			if evento.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
				mouse_pos = pygame.mouse.get_pos()
				m_x = mouse_pos[0]
				m_y = mouse_pos[1]
				if  m_y >=10 and m_y <=60:
					if m_x >=10 and m_x <=60:
						music_c =gameconfig.change_music()
						if music_c is True: music_image_file =  './assets/images/musicon.png'
						else: music_image_file =  './assets/images/musicoff.png'
						music =  aux.load_image(music_image_file,transparent=True)
						load_music(music_c,music_file)
						Screen.blit(music,(10,10))
					if m_x >=70 and m_x <=120:
						sound_c = gameconfig.change_sound()
						if gamePlay:
							gamePlay.change_sound(sound_c)

						if sound_c is True: sound_image_file =  './assets/images/soundon.png'
						else: sound_image_file =  './assets/images/soundoff.png'
						sound =  aux.load_image(sound_image_file,transparent=True)
						Screen.blit(sound,(70,10))
					if m_x >=130 and m_x <=180:
						gameMenu.change_visibility()
						state = hall(gameconfig)

			state = gameMenu.listenEvents(evento,state)
			if state == 'JUEGO': #comienzo juego
				ticks = ticks_inicial
				gamePlay.change_sound(sound_c)
				direction = gamePlay.new()

		elif state == 'JUEGO':
			if evento.type == KEYDOWN and evento.key == K_ESCAPE:
				state = 'PAUSE' #game over
				menu_items = (
					{'message':'CONTINUAR','action':'continuar'},                    
					{'message':'NUEVO','action':'nuevo'},
					{'message':'SALIR','action':'salir'})
				PauseMenu= Menu(100,50,menu_items)                
			if evento.type == pygame.KEYDOWN:
				if evento.key == K_UP and direction != 0: direction = 2
				elif evento.key == K_DOWN and direction != 2:direction = 0
				elif evento.key == K_LEFT and direction != 1:direction = 3
				elif evento.key == K_RIGHT and direction != 3:direction = 1
				
			ticks = ticks_inicial + (gamePlay.get_level()*gamePlay.get_level())
		#eventos del menu
		elif state =='GAMEOVER':
			state = gameOverMenu.listenEvents(evento,state)
			if state == 'JUEGO': #comienzo juego
				ticks = ticks_inicial
				direction = gamePlay.new()
		elif state == 'PAUSE':
			state = PauseMenu.listenEvents(evento,state)
			if state == 'CONTINUE':
				direction = gamePlay.continuar()
				state = 'JUEGO'
			elif state == 'JUEGO':
				direction = gamePlay.new()
				ticks = ticks_inicial
		elif state == 'HALL':
			if evento.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
				gameMenu.change_visibility()
				back_menu_draw(music_c,sound_c)
				gameMenu.draw()
				state ='MENU'

	if state == 'MENU' or state == 'GAMEOVER' or state == 'PAUSE':
		Screen.blit(serpi,(350,440))


	pygame.display.flip()

