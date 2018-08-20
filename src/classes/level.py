# -*- coding: utf-8 -*-
from ..render.stages import LEVELS


class Level:

	def __init__(self, id):
		self.__id = LEVELS[id]['id']
		self.__name = LEVELS[id]['name']
		self.__design = LEVELS[id]['design']
		self.__start = LEVELS[id]['start']
		self.__end = LEVELS[id]['end']
		self.__music = LEVELS[id]['background_music']
		self.__completion = LEVELS[id]['top_score']

	@property
	def id(self):
		return self.__id

	@property
	def name(self):
		return self.__name

	@property
	def design(self):
		return self.__design

	@property
	def start(self):
		return self.__start

	@property
	def end(self):
		return self.__end

	@property
	def music(self):
		return self.__music

	@property
	def completion(self):
		return self.__completion
