#!/usr/bin/env python3

import math
import sys

class Basestation:

	# PWR -> 50, GAIN -> 24
	TRANSMIT_POWER = 20 # P_TX (watts)
	LINE_LOSS = 4 # (dB)
	ANTENNA_GAIN = 8 # AG_TX (dB)
	ANTENNA_HEIGHT = 30  # h_b (m)
	NUM_CHANNELS = 15 # NUM_CHANNELS

	# Fields
	id = -1
	position = None
	frequency = 0 # (MHz)

	# Stats
	callAttempts = 0
	blockedLowSignalStrength = 0
	blockedCapacity = 0
	numActiveCalls = 0
	handoffs = 0
	handoffFailures = 0
	droppedCalls = 0
	talkTime = 0
	totalCalls = 0
	numDroppedSignalStrength = 0
	numHangUps = 0

	def __init__(self, id, position, frequency):
		self.id = id
		self.position = position
		self.frequency = frequency

	# 
	# Calculate EIRP for tower
	#
	#	EIRP = P_T - L + AG 	(dB)
	#
	def getEIRP(self):
		# Convert tx power to dBm
		tx_dBm = 10 * math.log(self.TRANSMIT_POWER * math.pow(10,3), 10)

		return tx_dBm - self.LINE_LOSS + self.ANTENNA_GAIN


	def toJson(self):
		return "{pos:%s, freq:%d, active:%d, blockSig:%d, blockCap: %d}" % (self.position.toJson(), self.frequency, self.numActiveCalls, self.blockedLowSignalStrength, self.blockedCapacity)

	def requestConnection(self, mobile):
		self.callAttempts += 1

		# Determine if RSL level meets threshold
		if mobile.servingRSL < mobile.RSL_THRESH:
			self.blockedLowSignalStrength += 1
			return False

		# Determine if capacity available
		if self.numActiveCalls >= self.NUM_CHANNELS:
			self.blockedCapacity += 1
			return False

		# Connect device
		self.numActiveCalls += 1
		self.totalCalls += 1
		self.handoffs += 1
		return True

	def requestHandoff(self):
		if self.numActiveCalls >= self.NUM_CHANNELS:
			self.handoffFailures += 1
			return False

		self.numActiveCalls += 1
		return True

	def disconnectHandoff(self):
		self.handoffs += 1
		self.numActiveCalls -= 1

	def handleHandoff(self, mobile):
		self.numActiveCalls -= 1
		self.handoffs += 1

	def incrementTalkTime(self):
		# TODO: Remove this debug logging
		if self.numActiveCalls < 0:
			print("NO!")
			sys.exit(1)
		self.talkTime += self.numActiveCalls


	def dropSigStrength(self):
		self.numActiveCalls -= 1
		self.numDroppedSignalStrength += 1

	def hangUp(self):
		self.numActiveCalls -= 1
		self.numHangUps += 1

	def reportStats(self, header):
		gos = (self.blockedLowSignalStrength + self.blockedCapacity + self.numDroppedSignalStrength) / self.callAttempts
		handoff_failure_rate = self.handoffFailures / (self.handoffFailures + self.handoffs)
		traffic_intensity = self.totalCalls / 3600
		print("%s %d, %d, %d, %d, %d, %d, %d, %d, %f, %f, %f" % (header, self.callAttempts, self.blockedLowSignalStrength, self.blockedCapacity, self.numDroppedSignalStrength, self.handoffFailures, self.handoffs, self.totalCalls, self.talkTime, gos, handoff_failure_rate, traffic_intensity))
