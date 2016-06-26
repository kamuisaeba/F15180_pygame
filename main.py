#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importamos la librería
import pygame

import sys

# Importamos constantes locales de pygame
from pygame.locals import *

# Iniciamos Pygame
pygame.init()

def load_image(filename, size,transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = pygame.transform.scale(image,size)
        if transparent:
            image.convert_alpha()
        return image

# Creamos una surface (la ventana de juego), asignándole un ancho y un alto
SCREEN_WIDTH=960
SCREEN_HEIGHT=640
pygame.init()
Ventana = pygame.display.set_mode( (SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('SNAKE!!!')

# Elegimos la fuente y el tamaño
Fuente= pygame.font.SysFont('Impact', 45)

# Renderizamos (convertimos a imagen) el mensaje con la fuente definida

b_click = load_image('./assets/images/b_click.png',(300,100),True)
b_disabled = load_image('./assets/images/b_disabled.png',(300,100),True)
b_default = load_image('./assets/images/b_default.png',(300,100),True)

music = load_image('./assets/images/musicon.png',(50,50),True)
sound = load_image('./assets/images/soundon.png',(50,50),True)
menu = load_image('./assets/images/menu.png',(SCREEN_WIDTH-200, SCREEN_HEIGHT-100),True)
serpi = load_image('./assets/images/serpi.png',(260,210),True)

background = load_image('./assets/images/backMenu.png',( SCREEN_WIDTH, SCREEN_HEIGHT))
Ventana.fill((0,0,0))

m_nuevo = Fuente.render("NUEVO", 1, (83, 80, 70))
m_continuar = Fuente.render("CONTINUAR", 1, (83, 80, 70))
m_salir = Fuente.render("SALIR", 1, (83, 80, 70))

Ventana.blit(background, (0,0))
Ventana.blit(menu,(100,50))
Ventana.blit(music,(10,10))
Ventana.blit(sound,(70,10))
Ventana.blit(b_default,(325,150))
Ventana.blit(m_continuar,(375,170))

Ventana.blit(b_default,(325,250))
Ventana.blit(m_nuevo,(375,270))
Ventana.blit(b_default,(325,350))
Ventana.blit(m_salir,(375,370))
Ventana.blit(serpi,(350,440))




# posiciona las imágenes en Ventana
#Ventana.blit(Fondo, (0, 0))
# refresca los gráficos
pygame.display.flip()

# Bucle infinito para mantener el programa en ejecución
while True:
    
    # Manejador de eventos
    for evento in pygame.event.get():
        # Pulsación de la tecla escape
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                sys.exit()