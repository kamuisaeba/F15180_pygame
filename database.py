#!/usr/bin/env python
# -*- coding: utf-8 -*-


import MySQLdb
import ConfigParser
import io

class GameConfig:
	def __init__(self):
		self.read_yaml_config()
	def read_yaml_config(self,dict=0):
		'''
		lee el fichero de configuracion
		'''
		self.config_f = 'config.yml'
		with open(self.config_f,'r') as f:
			config_file = f.read()
		self.cfg = ConfigParser.RawConfigParser(allow_no_value=True)
		self.cfg.readfp(io.BytesIO(config_file))
		self.user = self.cfg.get('mysql','user')
		self.host = self.cfg.get('mysql','host')
		self.port = self.cfg.getint('mysql','port')
		self.passwd = self.cfg.get('mysql','pass')
		self.db = self.cfg.get('mysql','db')
		self.music = self.cfg.getboolean('global','music')
		self.sound = self.cfg.getboolean('global','sound')
		self.top_ranking = self.cfg.getint('halloffame','limit')
		self.conection = MySQLdb.connect(host=self.host,port=self.port, user=self.user, passwd =self.passwd, db=self.db)
		self.micursor = self.conection.cursor(MySQLdb.cursors.DictCursor)  
		self.create_database()
		self.micursor.close()
		

	def create_database (self):
		'''
		genera en caso necesario la base de datos
		'''
		self.micursor = self.conection.cursor(MySQLdb.cursors.DictCursor)  
		query ='create table if not exists ranking (user varchar(255),score int)'
		self.micursor.execute(query)
		self.conection.commit()

	def init_game(self):
		'''
		obtiene los datos de configuracion necesarios para el juego
		'''
		return self.sound,self.music

	def change_sound(self):
		'''
		modifica en configuracion el estado de configuracion del sonido
		'''
		self.sound = not self.sound
		self.cfg.set('global','sound',self.sound)
		with open(self.config_f,'wb') as f:
			self.cfg.write(f)
		return self.sound

	def change_music(self):
		'''
		modifica en configuracion el estado de configuracion de la musica
		'''
		self.music = not self.music
		self.cfg.set('global','music',self.music)
		with open(self.config_f,'wb') as f:
			self.cfg.write(f)
		return self.music

	def populate_ranking(self):
		'''
		devuelve el ranking del juego, ordenado por puntuacion,usando un top configurable
		'''
		self.micursor = self.conection.cursor(MySQLdb.cursors.DictCursor)  
		query ='select user,score,level from ranking order by score desc limit ' +str(self.top_ranking)
		self.micursor.execute(query)
		data = self.micursor.fetchall()
		self.micursor.close()
		print data
		return data

	def insert_ranking(self,user,score,level):
		'''
		Inserta en el ranking una nueva puntuacion
		'''
		self.micursor = self.conection.cursor(MySQLdb.cursors.DictCursor)  
		query ="insert into ranking (user,score,level) values ('"+user+"',"+str(score)+","+str(level)+")"
		self.micursor.execute(query)
		self.micursor.close()	
		self.conection.commit()
	def get_range_ranking(self):
		'''
		devuelve el minimo y maximo actual para estar en el ranking
		'''
		self.micursor = self.conection.cursor(MySQLdb.cursors.DictCursor)  
		query ='select min(score) as min,max(score) as max,count(1) as count '\
		+'from (select user,score,level from ranking order by score desc limit ' +str(self.top_ranking)+') a'
		self.micursor.execute(query)
		data = self.micursor.fetchone()
		self.micursor.close()
		return data

	def get_music(self):
		return self.music

	def get_sound(self):
		return self.sound

	def get_ranking_limit (self):
		return self.top_ranking

#print GameConfig().get_range_ranking()