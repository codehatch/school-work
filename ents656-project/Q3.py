#!/usr/bin/env python3

from Simulator import Simulator

def main():

	NUM_INITIAL_MOBILES = 150
	SIMULATION_ITERATIONS = 3600

	print("callAttempts, blkSig, blkCap, dropSig, HOfail, HO, complSuc, talkTime, GOS, HOFR, intensity")

	for iteration in range(10):
		simulator = Simulator(NUM_INITIAL_MOBILES, 1.0/3600)
#		simulator.basestations[0].ANTENNA_GAIN = 10
#		simulator.basestations[1].ANTENNA_GAIN = 10
		simulator.basestations[0].NUM_CHANNELS = 20
		simulator.basestations[1].NUM_CHANNELS = 20
		simulator.run(SIMULATION_ITERATIONS, iteration)

if __name__ == "__main__":
	main()