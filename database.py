#!/usr/bin/env python
# -*- coding: utf-8 -*-


import MySQLdb
import ConfigParser
import io

class Database:
	def __init__(self):
		self.read_yaml_config()
	def read_yaml_config(self,dict=0):
		'''
		lee el fichero de configuracion
		'''
		with open('config.yml') as f:
			readed = f.read()
		cfg = ConfigParser.RawConfigParser(allow_no_value=True)
		cfg.readfp(io.BytesIO(readed))
		self.user = cfg.get('mysql','user')
		self.host = cfg.get('mysql','host')
		self.port = cfg.getint('mysql','port')
		self.passwd = cfg.get('mysql','pass')
		self.db = cfg.get('mysql','db')
		self.conection = MySQLdb.connect(host=self.host,port=self.port, user=self.user, passwd =self.passwd, db=self.db)
		self.micursor = self.conection.cursor(MySQLdb.cursors.DictCursor)  
		self.create_database()
		self.populate_ranking()
		self.micursor.close()
		

	def create_database (self):
		'''
		genera en caso necesario la base de datos
		'''
		self.micursor = self.conection.cursor(MySQLdb.cursors.DictCursor)  
		query ='create table if not exists config (music bit,sound bit)'
		self.micursor.execute(query)
		query ='create table if not exists ranking (user varchar(255),score int)'
		self.micursor.execute(query)
		self.conection.commit()

	def init_game(self):
		'''
		obtiene los datos de configuracion necesarios para el juego
		'''
		self.micursor = self.conection.cursor(MySQLdb.cursors.DictCursor)  
		query ='select top 1 sound,music from config'
		self.micursor.execute(query)
		data = self.micursor.fetchone()
		self.micursor.close()
		return data['sound'],data['music']

	def change_sound(self,estado):
		'''
		modifica en base de datos el estado de configuracion del sonido
		'''
		self.micursor = self.conection.cursor()  
		query ='update config set sound ='+ str(estado)
		self.micursor.execute(query)
		self.conection.commit()
		self.micursor.close()

	def change_music(self,estado):
		'''
		modifica en base de datos el estado de configuracion de la musica
		'''
		self.micursor = self.conection.cursor()  
		query ='update config set music ='+ str(estado)
		self.micursor.execute(query)
		self.conection.commit()
		self.micursor.close()

	def populate_ranking(self):
		'''
		devuelve el ranking del juego, ordenado por puntuacion,usando un top configurable
		'''
		self.micursor = self.conection.cursor(MySQLdb.cursors.DictCursor)  
		query ='select user,score from ranking order by score desc limit ' +str(10)
		self.micursor.execute(query)
		data = self.micursor.fetchall()
		self.micursor.close()
		print data
		return data

	def insert_ranking(self,user,score):
		'''
		Inserta en el ranking una nueva puntuacion
		'''
		self.micursor = self.conection.cursor(MySQLdb.cursors.DictCursor)  
		query ="insert into ranking (user,score) values ('"+user+"',"+str(score)+") from ranking"
		self.micursor.execute(query)
		self.micursor.close()	
	def get_range_ranking(self):
		'''
		devuelve el minimo y maximo actual para estar en el ranking
		'''
		self.micursor = self.conection.cursor(MySQLdb.cursors.DictCursor)  
		query ='select min(score) as min,max(score) as max,count(1) as count from ranking'
		self.micursor.execute(query)
		data = self.micursor.fetchone()
		self.micursor.close()
		return data['min'],data['max'],
Database()