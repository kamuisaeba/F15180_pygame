#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importamos la librería
import pygame
import random

import sys

# Importamos constantes locales de pygame
from pygame.locals import *

import aux
from menu import *
from snake import *
from database import GameConfig

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


# Elegimos la fuente y el tamaño
Fuente= pygame.font.SysFont('Impact', 45)
background =  aux.load_image('./assets/images/backMenu.png',( SCREEN_WIDTH, SCREEN_HEIGHT))
Screen.blit(background, (0,0))  

menu_items = (
    #{'message':'CONTINUAR','action':'continuar'}, 
    {'message':'NUEVO','action':'nuevo'},
    {'message':'SALIR','action':'salir'})
gameMenu = Menu(100,50,menu_items)

serpi =  aux.load_image('./assets/images/serpi.png',(260,210),True)


if music_c is True: music_image_file =  './assets/images/musicon.png'
else: music_image_file =  './assets/images/musicoff.png'
if sound_c is True: sound_image_file =  './assets/images/soundon.png'
else: sound_image_file =  './assets/images/soundoff.png'
music =  aux.load_image(music_image_file,transparent=True)
sound =  aux.load_image(sound_image_file,transparent=True)
hall = aux.load_image('./assets/images/hall.png',transparent=True)
Screen.blit(music,(10,10))
Screen.blit(sound,(70,10))
Screen.blit(hall,(130,10))


# refresca los gráficos
pygame.display.flip()

# Bucle infinito para mantener el programa en ejecución
clock = pygame.time.Clock()
state ='MENU'
direction = 1
ticks = 10
ticks_inicial = 10
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
            gamePlay.gameover()
            state = 'GAMEOVER' #game over
            range_ranking = gameconfig.get_range_ranking()
            score = gamePlay.get_score()
            level =gamePlay.get_level()
            print range_ranking,score
            if score > 0 and (range_ranking['count'] < ranking_limit or range_ranking['min'] < score):
                print 'hall of fame'
                gameconfig.insert_ranking('yomismo',score,level)

            print ranking_limit
            gameconfig.populate_ranking()
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
                        Screen.blit(music,(10,10))
                    if m_x >=70 and m_x <=120:
                        sound_c = gameconfig.change_sound()
                        if sound_c is True: sound_image_file =  './assets/images/soundon.png'
                        else: sound_image_file =  './assets/images/soundoff.png'
                        sound =  aux.load_image(sound_image_file,transparent=True)
                        Screen.blit(sound,(70,10))
                    if m_x >=130 and m_x <=180:
                        print 'hall'

            state = gameMenu.listenEvents(evento,state)
            if state == 'JUEGO': #comienzo juego
                ticks = ticks_inicial
                gamePlay = Game()
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
                
            ticks = ticks_inicial * gamePlay.get_level()
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

    if state == 'MENU' or state == 'GAMEOVER' or state == 'PAUSE':
        Screen.blit(serpi,(350,440))


    pygame.display.flip()