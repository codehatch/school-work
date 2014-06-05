#!/usr/bin/env python3

from Simulator import Simulator

def main():

	NUM_INITIAL_MOBILES = 150
	SIMULATION_ITERATIONS = 3600

	print("callAttempts, blkSig, blkCap, dropSig, HOfail, HO, complSuc, talkTime, GOS, HOFR, intensity")

	for iteration in range(20):
		call_rate = (1.0+0.5*iteration)
		simulator = Simulator(NUM_INITIAL_MOBILES, call_rate/3600)
		simulator.run(SIMULATION_ITERATIONS, call_rate)

if __name__ == "__main__":
	main()