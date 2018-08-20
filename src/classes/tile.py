# -*- coding: utf-8 -*-


class Tile:

	def __init__(self, pos, x=-1, y=-1, type=0):
		self.__x = x
		self.__y = y
		self.__type = type
		self.__pos = pos

	def reset(self, pos, x=-1, y=-1, type=0):
		self.__init__(pos, x, y, type)

	@property
	def x(self):
		return self.__x

	@x.setter
	def x(self, x):
		self.__x = x

	@property
	def y(self):
		return self.__y

	@y.setter
	def y(self, y):
		self.__y = y

	@property
	def type(self):
		return self.__type

	@type.setter
	def type(self, type):
		self.__type = type

	@property
	def pos(self):
		return self.__pos
