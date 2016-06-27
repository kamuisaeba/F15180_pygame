#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importamos la librería
import pygame

import sys

# Importamos constantes locales de pygame
from pygame.locals import *

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GREEN = (51, 255, 51)
EGG = (102, 255, 140)

#helper para cargar imágenes
def load_image(filename, size,transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = pygame.transform.scale(image,size)
        if transparent:
            image.convert_alpha()
        return image