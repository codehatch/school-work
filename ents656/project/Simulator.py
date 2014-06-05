#!/usr/bin/env python3

from Position import Position
from Mobile import Mobile
from Basestation import Basestation
import numpy as np
import math
import sys

class Simulator:

	# ALL UNITS ARE IN METERS
	ROAD_LEN = 6000
	CELL_RADIUS_KM = 1600
	SIM_STEP_SIZE_SEC = 1
	SIM_TIME_SEC = 3600
	MOBILE_APPEARANCE_RATE = 2 # Tm (1 mobile every 2 seconds)

	basestations = {}
	BS0 = Basestation(0, Position(1500, 100), 900)
	BS1 = Basestation(1, Position(4500, 100), 905)
	next_mobile_id = 0
	mobiles = []

	mobileCallRate = 1.0 / 3600

	def __init__(self, initial_mobiles, mobileCallRate):
		self.mobileCallRate = mobileCallRate
		self.mobiles = []
		X_ARR = np.linspace(0, self.ROAD_LEN, initial_mobiles)
		for x in X_ARR:
			self.add_mobile(x)

		self.basestations = {}
		self.basestations[0] = Basestation(0, Position(1500, 100), 900)
		self.basestations[1] = Basestation(1, Position(4500, 100), 905)

	def dump_mobiles(self):
		for mobile in self.mobiles:
			print("\t%s" % mobile.toJson())

	def add_mobile(self, x):

		# Randomly determine if moving East
		moving_east = bool(np.random.binomial(1, 0.5))

		# Default to no call up
		call_up = False

		self.mobiles.append(Mobile(self.next_mobile_id, Position(x, 0), moving_east, call_up, self.mobileCallRate))

		# Increment ID
		self.next_mobile_id = self.next_mobile_id + 1

	def run(self, iterations, header):
		# Loop the appropriate number of iterations
		for iteration in range(iterations):

			# Increment talk time for towers
			for bsid in self.basestations:
				self.basestations[bsid].incrementTalkTime()

			# introduce new mobile at apperance rate
			if iteration % self.MOBILE_APPEARANCE_RATE == 0:
				random_pos = np.random.randint(0, self.ROAD_LEN+1)
				self.add_mobile(random_pos)

			# update mobiles (iterate backwards to support delete)
			for index in range(len(self.mobiles)-1, -1, -1):
				mobile = self.mobiles[index]

				# Update position
				mobile.updatePosition()

				# Delete if off road
				if mobile.position.x >= self.ROAD_LEN or mobile.position.x <= 0:
					# Handle hand off if was up
					if mobile.callUp:
						servingBs = self.basestations[mobile.servingBsid]
						servingBs.disconnectHandoff()
					del self.mobiles[index]
				else:
					mobile.updateStatus(self)

		# Print out stats
		for bsid in self.basestations:
			self.basestations[bsid].reportStats("%s, %d," % (header, bsid))


	def printConnectionSummary(self):
		for basestationId in self.basestations:
			print("BS%d: %s" % (basestationId, self.basestations[basestationId].mobileIds()))