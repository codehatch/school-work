#!/usr/bin/env python3
import math


# Represents an entities position in the simulation
class Position:
	# Distance from West endpoint on the road (in km)
	x = 0.0

	# distance North of the road (in km)
	y = 0.0

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def toJson(self):
		return "{x:%.0f,y:%.0f}" % (self.x, self.y)

	def moveEast(self, distance):
		self.x = self.x + distance

	def moveWest(self, distance):
		self.x = self.x - distance

	# Use simple trig to determine the difference between 2 points
	#
	# @return:
	#	Distance between points
	def distance(self, position):
		d_x_m = math.fabs(self.x - position.x)
		d_y_m = math.fabs(self.y - position.y)

		# compute hypotenuse
		return math.sqrt(math.pow(d_x_m, 2) + math.pow(d_y_m, 2))
