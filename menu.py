#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importamos la librería
import pygame

import sys

# Importamos constantes locales de pygame
from pygame.locals import *
import aux

class Menu:
    def __init__(self,Screen, x, y,items=[]):
        self.width = Screen.get_width() - 200
        self.heigth = Screen.get_height() - 100
        self.items = []
        self.visible = True
        self.Screen = Screen

        menu =  aux.load_image('./assets/images/menu.png',(self.width, self.heigth),True)
        Screen.blit(menu, (x,y))

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
            Screen.blit(item.image,item.image_position)
            Screen.blit(item.text,item.text_position)

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
        pygame.font.Font.__init__(self, './assets/FFF_Tusj.ttf', 45)
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
        self.text = self.render(self.message, 1, self.font_color)
        self.set_italic(True)
        self.image = self.image_selected
        self.Screen.blit(self.image,self.image_position)
        self.Screen.blit(self.text,self.text_position)
    def set_deselected(self):
        self.text = self.render(self.message, 1, self.font_color)
        self.set_italic(False)
        self.image = self.image_default
        self.Screen.blit(self.image,
            self.image_position)
        self.Screen.blit(self.text,self.text_position)
    def is_selected(self):
        return self.selected
    def execute_action(self):
        if self.action == 'salir':
            pygame.quit()
            sys.exit()
        elif self.action == 'nuevo':
            self.menu.change_visibility()
            return 2