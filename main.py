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

# Iniciamos Pygame
pygame.init()

# --- Globales ---
# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
 



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
    {'message':'CONTINUAR','action':'continuar'}, 
    {'message':'NUEVO','action':'nuevo'},
    {'message':'SALIR','action':'salir'})
gameMenu = Menu(100,50,menu_items)

serpi =  aux.load_image('./assets/images/serpi.png',(260,210),True)
music =  aux.load_image('./assets/images/musicon.png',(50,50),True)
sound =  aux.load_image('./assets/images/soundon.png',(50,50),True)
Screen.blit(music,(10,10))
Screen.blit(sound,(70,10))


#anotamos eventos

# refresca los gráficos
pygame.display.flip()

# Bucle infinito para mantener el programa en ejecución



clock = pygame.time.Clock()
state ='MENU'
dirs = 1
while True:
    # Manejador de estados
    clock.tick(25)
    '''
    ESTADOS DEL JUEGO
    0: MENU INICIAL
    1: JUGANDO
    2: JUEGO PAUSADO
    3: GAME OVER
    '''
    if state =='JUEGO' and gamePlay.mover(dirs) == 'GAMEOVER':
            print 'GAME OVER'
            gamePlay.gameover()
            state = 'GAMEOVER' #game over
            menu_items = (
                {'message':'CONTINUAR','action':'continuar'}, 
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
        # Pulsación de la tecla escape.. valido en cualquier estado
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                sys.exit()
        #eventos del menu
        if state =='MENU':
            for item in gameMenu.get_items():
                if item.is_mouse_selection(pygame.mouse.get_pos()):
                    item.set_selected()
                    if pygame.mouse.get_pressed()[0]:
                        state =item.execute_action()  
                        if state == 'JUEGO': #comienzo juego
                            gamePlay = Game()
                elif gameMenu.get_visibility():
                    item.set_deselected()
        if state == 'MENU':
                Screen.blit(serpi,(350,440))

        if state == 'JUEGO':
            if evento.type == pygame.KEYDOWN:
                if evento.key == K_UP and dirs != 0:dirs = 2
                elif evento.key == K_DOWN and dirs != 2:dirs = 0
                elif evento.key == K_LEFT and dirs != 1:dirs = 3
                elif evento.key == K_RIGHT and dirs != 3:dirs = 1
        #eventos del menu
        if state =='GAMEOVER':
            for item in gameOverMenu.get_items():
                if item.is_mouse_selection(pygame.mouse.get_pos()):
                    item.set_selected()
                    if pygame.mouse.get_pressed()[0]:
                        state =item.execute_action()  
                        if state == 'JUEGO': #comienzo juego
                            gamePlay = Game()
                elif gameOverMenu.get_visibility():
                    item.set_deselected()
        if state == 'GAMEOVER':
                Screen.blit(serpi,(350,440))


    pygame.display.flip()