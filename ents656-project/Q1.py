#!/usr/bin/env python3

from Simulator import Simulator

def main():

	NUM_INITIAL_MOBILES = 150
	SIMULATION_ITERATIONS = 3600

	print("callAttempts, blkSig, blkCap, dropSig, HOfail, HO, complSuc, talkTime, GOS, HOFR, intensity")

	for iteration in range(10):
		simulator = Simulator(NUM_INITIAL_MOBILES, 1.0/3600)
		simulator.run(SIMULATION_ITERATIONS, iteration)

if __name__ == "__main__":
	main()