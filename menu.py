#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importamos la librería
import pygame

import sys

# Importamos constantes locales de pygame
from pygame.locals import *
import aux

class Menu:
	def __init__(self, x, y,items=[]):
		self.Screen = pygame.display.get_surface()
		self.width = self.Screen.get_width() - 200
		self.heigth = self.Screen.get_height() - 100
		self.items = []
		self.visible = True
		self.selected = -1


		menu =  aux.load_image('./assets/images/menu.png',(self.width, self.heigth),True)
		self.Screen.blit(menu, (x,y))

		#calculamos ancho y alto elementos menu
		item_menu_base_dim_w= (menu.get_width()/2)
		item_menu_base_dim_h= (menu.get_height()-200) / len(items)
		item_menu_base_dim = (menu.get_width()-100,menu.get_height()-200)
		item_menu_base_coord_x = x+200
		item_menu_base_coord_y = y+100
		for index,item in enumerate(items):
			item_x= item_menu_base_coord_x
			item_y= item_menu_base_coord_y + (index* item_menu_base_dim_h)
			menu_item = MenuItem(self,item['message'],item['action'],item_menu_base_dim_w,item_menu_base_dim_h,item_x,item_y)
			self.items.append(menu_item)
		for item in self.items:
			self.Screen.blit(item.image,item.image_position)
			self.Screen.blit(item.text,item.text_position)

	def listenEvents(self,evento,state):
		#EVENTOS DE RATON
		if evento.type == pygame.MOUSEMOTION:
			for item in self.get_items():
				if item.is_mouse_selection(pygame.mouse.get_pos()):
					item.set_selected() 
				elif self.get_visibility():
					item.set_deselected()
		elif evento.type == pygame.KEYDOWN and evento.key in (K_UP,K_DOWN):
			self.items[self.selected].set_deselected()
			if evento.key == K_DOWN: 
				if self.selected < 0:
					self.selected = 0
				else: self.selected = (self.selected +1) % (len(self.items))
			elif evento.key == K_UP: 
				if self.selected <= 0:
					self.selected = (len(self.items) - 1)
				else: 
					self.selected = (self.selected -1) % (len(self.items))
			self.items[self.selected].set_selected()
		item = self.get_selected_item()
		if item and (evento.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]) or (evento.type == pygame.KEYDOWN and evento.key == K_RETURN):
				state =item.execute_action() 
		return state

	def get_selected_item(self):
		for a in self.get_items():
			if a.is_selected():
				return a
		return None
	def get_visibility(self):
		return self.visible

	def change_visibility(self):
		self.visible = not self.visible

	def get_items(self):
		return self.items



class MenuItem(pygame.font.Font):
	"""docstring for MenuItem"""
	def __init__(self,menu,message,action,w,h,x,y):
		self.image_default = aux.load_image('./assets/images/b_default.png',(w,h),True)
		self.image_selected = aux.load_image('./assets/images/b_click.png',(w,h),True)
		self.Fuente= pygame.font.SysFont('Impact', 45)
		pygame.font.Font.__init__(self, './assets/font/FFF_Tusj.ttf', 45)
		self.image = self.image_default
		self.pos_x = x
		self.pos_y = y
		self.height = h
		self.width = w
		self.message =message
		self.image_position = (x,y)
		self.text_position  = (x+50,y+20)
		self.font_color =  (83, 80, 70)
		self.text = self.render(self.message, 1, self.font_color)
		self.selected = False
		self.action = action
		self.menu =menu
		self.Screen = self.menu.Screen

	def is_mouse_selection(self, (posx, posy)):
		if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
			(posy >= self.pos_y and posy <= self.pos_y + self.height):
				return True
		return False

	def set_selected(self):
		if not self.selected:
			self.text = self.render(self.message, 1, self.font_color)
			self.set_italic(True)
			self.image = self.image_selected
			self.Screen.blit(self.image,self.image_position)
			self.Screen.blit(self.text,self.text_position)
			self.selected = True
	def set_deselected(self):
		if self.selected:
			self.text = self.render(self.message, 1, self.font_color)
			self.set_italic(False)
			self.image = self.image_default
			self.Screen.blit(self.image,
				self.image_position)
			self.Screen.blit(self.text,self.text_position)
			self.selected = False

	def is_selected(self):
		return self.selected
	def execute_action(self):
		if self.action == 'salir':
			pygame.quit()
			sys.exit()
		elif self.action == 'nuevo':
			self.menu.change_visibility()
			return 'JUEGO'
		elif self.action == 'continuar':
			self.menu.change_visibility()
			return 'CONTINUE'
