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
gameMenu = Menu(Screen,100,50,menu_items)

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
state =1
dirs = 1
while True:
    clock.tick(5)
    # Manejador de eventos
    if state ==2:
        if gamePlay.mover(dirs) == False:
            print 'cambio estado'
            state = 4 #game over
    if state == 4:
        print 'state 4'
        menu_items = (
            {'message':'CONTINUAR','action':'continuar'}, 
            {'message':'NUEVO','action':'nuevo'},
            {'message':'SALIR','action':'salir'})
        gameOverMenu = Menu(Screen,100,50,menu_items)
    for evento in pygame.event.get():
        # Pulsación de la tecla escape
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                sys.exit()
        #eventos del menu
        if state ==1:
            for item in gameMenu.get_items():
                if item.is_mouse_selection(pygame.mouse.get_pos()):
                    item.set_selected()
                    if pygame.mouse.get_pressed()[0]:
                        state =item.execute_action()  
                        if state == 2: #comienzo juego
                            gamePlay = Game(Screen)
                elif gameMenu.get_visibility():
                    item.set_deselected()
        if gameMenu and gameMenu.get_visibility():
            Screen.blit(serpi,(350,440))

        if state == 2:
            if evento.type == pygame.KEYDOWN:
                if evento.key == K_UP and dirs != 0:dirs = 2
                elif evento.key == K_DOWN and dirs != 2:dirs = 0
                elif evento.key == K_LEFT and dirs != 1:dirs = 3
                elif evento.key == K_RIGHT and dirs != 3:dirs = 1



    pygame.display.flip()