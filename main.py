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
music =  aux.load_image('./assets/images/musicon.png',(50,50),True)
sound =  aux.load_image('./assets/images/soundon.png',(50,50),True)
Screen.blit(music,(10,10))
Screen.blit(sound,(70,10))


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
            print 'GAME OVER'
            gamePlay.gameover()
            state = 'GAMEOVER' #game over
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
                
            ticks = ticks_inicial * gamePlay.getLevel()
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