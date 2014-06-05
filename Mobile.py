#!/usr/bin/env python3

import Simulator

import numpy
import math

class Mobile:

	HEIGHT = 1.5 # h_m (m)
	SPEED = 10 # v (m/s)
	CALL_RATE = 1.0 / 3600.0 # 1 call per hour
	CALL_DURATION = 180 # H (3 minutes)
	RSL_THRESH = -102 # (dBm)
	HOM = 3 # HOm (dB) handoff margin

	id = 0
	position = None
	movingEast = False
	callDuration = 0
	callUp = False
	servingBsid = -1
	servingRSL = 0.0

	def __init__(self, id, position, movingEast, callUp, callRate):
		self.id = id
		self.position = position
		self.movingEast = movingEast
		self.callUp = callUp
		self.CALL_RATE = callRate

	def toJson(self):
		return "{id: %d, pos:%s, east:%s, call_up:%s}" % (self.id, self.position.toJson(), self.movingEast, self.callUp)

	def updatePosition(self):
		if self.movingEast:
			self.position.moveEast(self.SPEED)
		else:
			self.position.moveWest(self.SPEED)

	def updateStatus(self, simulator):
		if self.callUp:
			self._updateCallUp(simulator)
		else:
			self._updateNoCallUp(simulator)

	def _updateCallUp(self, simulator):
		self.callDuration += 1

		if self.callDuration >= self.CALL_DURATION:
			# Call completed
			simulator.basestations[self.servingBsid].hangUp()
			self.disconnect()
			return


		RSL0 = self.calculateRSL(simulator.basestations[0])
		RSL1 = self.calculateRSL(simulator.basestations[1])

		if self.servingBsid == 0:
			serving_rsl = RSL0
			other_rsl = RSL1
		else:
			serving_rsl = RSL1
			other_rsl = RSL0

		# Debug
		#print("Talking to BS-%d: %f dB to %f dB" % (self.servingBsid, serving_rsl, other_rsl))

		if serving_rsl < self.RSL_THRESH and other_rsl < self.RSL_THRESH:
			# Call dropped due to lack of signal strength
			simulator.basestations[self.servingBsid].dropSigStrength()
			self.disconnect()
		elif serving_rsl < self.RSL_THRESH and other_rsl >= self.RSL_THRESH and other_rsl < (serving_rsl + self.HOM):
			# Call dropped due to lack of isgnal strength
			simulator.basestations[self.servingBsid].dropSigStrength()
			self.disconnect()
		elif serving_rsl < self.RSL_THRESH and other_rsl >= self.RSL_THRESH and other_rsl >= (self.RSL_THRESH + self.HOM):
			# dropped due to lack of signal strength during handoff
			simulator.basestations[self.servingBsid].dropSigStrength()
			simulator.basestations[0].handoffFailures += 1
			simulator.basestations[1].handoffFailures += 1
			self.disconnect()
		elif serving_rsl >= self.RSL_THRESH and other_rsl >= (serving_rsl + self.HOM):
			# Attempt handoff

			# Determine other basestation
			if self.servingBsid == 0:
				other_bsid = 1
			else:
				other_bsid = 0

			if simulator.basestations[other_bsid].requestHandoff():
				# Disconnect from other original
				simulator.basestations[self.servingBsid].disconnectHandoff()
				self.servingBsid = other_bsid
			# else handoff failed, stay on serving, other record fail handoff
		#else stay where you are

	#
	# Handle status update for a mobile with no call currently up
	#
	def _updateNoCallUp(self, simulator):
		# Determine if mobile will place a call with given call rate
		make_call = bool(numpy.random.binomial(1, self.CALL_RATE))

		if make_call:
			# Determine which basestation has largest RSL & request channel
			RSL0 = self.calculateRSL(simulator.basestations[0])
			RSL1 = self.calculateRSL(simulator.basestations[1])

			# Attempt to connect to basestation with greater RSL
			if RSL0 > RSL1:
				self.servingBsid = 0
				self.servingRSL = RSL0
				self.callUp = simulator.basestations[0].requestConnection(self)
			else:
				self.servingBsid = 1
				self.servingRSL = RSL1
				self.callUp = simulator.basestations[1].requestConnection(self)

	#
	# Disconnect device (clear serving bs, no longer call up, reset call duration)
	#
	def disconnect(self):
		self.servingBsid = -1
		self.callUp = False
		self.callDuration = 0


	#
	# RSL Calculation
	#
	#	RSL = EIRP - PropogationLoss + Shadowing + Fading
	#
	def calculateRSL(self, basestation):
		eirp = basestation.getEIRP()
		proploss = self.calculatePropogationLoss(basestation)
		shadowing = self.calculateShadowing()
		#print("Shadow: %f" % shadowing)
		fading = self.calculateFading()

		#print("RSL = %f - %f + %f + %f = %f" % (eirp, proploss, shadowing, fading, eirp - proploss + shadowing + fading))

		return eirp - proploss + shadowing + fading

	#
	# Okamura-Hata model for a small city
	#
	#	OH = L_50 = 69.55 + 26.16*log(f_MHz) - 13.82*log(h_B) + 
	#			(44.9 - 6.55*log(h_B))*log(d_km) - a(h_m)
	#
	# 	where mobile antenna correction factor given by:
	#		a(h_m) = (1.1*log(f_MHz))*h_m - (1.56*log(f_MHz)-0.8)
	#	
	def calculatePropogationLoss(self, basestation):
		
		f_MHz = basestation.frequency

		h_B = basestation.ANTENNA_HEIGHT

		# Calculate distance in km
		d_m = self.position.distance(basestation.position)
		d_km = d_m / 1000

		h_m = self.HEIGHT

		# calculate L_50
		L_50 = 69.55 + 26.16*math.log(f_MHz, 10)-13.82*math.log(h_B, 10) + (44.9-6.55*math.log(h_B, 10))*math.log(d_km, 10)

		# calculate the antenna correction factor
		a_h_m = (1.1*math.log(f_MHz, 10))*h_m - (1.56*math.log(f_MHz, 10)-0.8)

		# combine parts
		return  L_50 - a_h_m


	#
	# Log-normal distribution
	#
	#	location variability (std): 2 dB
	#	mean: 0.0
	#
	def calculateShadowing(self):
		return numpy.random.normal(0.0, 2.0, 1)

	#
	# Rayleigh distribution
	#
	#	magnitude of complete Gaussian distribution w/ real & complex
	# parts having zero mean and unit variance
	#
	#	generate 4 each sample, throw away deepest fade and report
	# the second deepest
	#
	def calculateFading(self):
		num_samples = 4
		# TODO: Put back to 4
		gaussian1 = numpy.random.normal(0, 1, size = 4)
		gaussian2 = numpy.random.normal(0, 1, size = 4)

		gaussian = gaussian1 + 0j
		gaussian.imag = gaussian2

		voltage = numpy.abs(gaussian)
		power = numpy.square(voltage)
		log = 10*numpy.log10(power)

		# Now find the second smallest (sort and get the 2nd)
		second_smallest = numpy.sort(log)[1]

		return second_smallest