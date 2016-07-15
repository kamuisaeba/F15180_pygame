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
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
pygame.mixer.init()
error_sound = pygame.mixer.Sound('./assets/sound/error.ogg')
score_sound = pygame.mixer.Sound('./assets/sound/score.ogg')
levelup_sound = pygame.mixer.Sound('./assets/sound/levelup.ogg')
gameover_sound = pygame.mixer.Sound('./assets/sound/gameover.ogg')



#helper para cargar imágenes
def load_image(filename, size=None,transparent=False,opacity=None):
		try: image = pygame.image.load(filename)
		except pygame.error, message:
				raise SystemExit, message
		if size:
			image = pygame.transform.scale(image,size)
		if transparent:
			image.convert_alpha()
		if opacity:
			image.set_alpha(opacity)
		return image