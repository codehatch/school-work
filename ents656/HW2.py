#!/usr/bin/python
# ENTS656: Python Homework 2
# Cody Smith

############
### H2.1 ###
############

persons = {}
#for i in range(5):
#	name = raw_input("Please enter person %d's name: " % (i+1))
#	name = input("Please enter person %d's name: " % (i+1))
#	age = int(input("Please enter person %d's age: " % (i+1)))
#	loyalty_points = int(input("Please enter person %d's loyalty points: " % (i+1)))
#	persons[name] = [age, loyalty_points]

persons = {'Adam':[24,50], 'Beth':[10,70], 'Carl':[65,110], 'Dana':[45,500], 'Elvis':[70,1200], 'Fran':[33,770]}

print("The dictionary contains:\n")

i = 0
for name in persons:
    person = persons[name]
    age = person[0]
    loyalty_points = person[1]

    print("For person %d: name=%s, age=%s, loyalty points=%d" % (i, name, person[0], person[1]))

    if age >= 65:
        print("\tEligible for a senior citizen discount")
    if age < 12:
        print("\tEligible for free kid's dessert")
    if loyalty_points >= 100 and loyalty_points < 500:
        print("\tEligible for a 10% discount")
    elif loyalty_points >= 500 and loyalty_points < 1000:
        print("\tEligible for a 20% discount")
    elif loyalty_points >= 1000:
        print("\tEligible for a free meal")

    print("")

    i+=1


############
### H2.2 ###
############

def prime_factor(x):
    if isinstance(x, int) and x > 0:
        factors = []
        d = 2
        while x > 1:
            while x % d == 0:
                factors.append(d)
                x /= d
            d = d + 1

            # Condition to improve performance and break out
            if d*d > x:
                if x > 1: factors.append(x)
                break
        return factors
    else:
        return None

print(prime_factor(12))
print(prime_factor(18))
print(prime_factor(19))
print(prime_factor(999))
print(prime_factor(-4.7))


print("\n\n")

############
### H2.3 ###
############

import math

# Based on Erlang B Formula
#   A = capacity in Erlangs
#   C = # channels (traffic channels, things actually hold users and keep call up)
#
#   Probability of Blocking:
#       Pr(blocking) = GOS = (A^C / C!) / ( E:k=0->C (A^k / k!) )
#
# Tried using float() for all variables and did not improve any...
def GOS_Erlang(channels, capacity):
    if isinstance(channels, int) and isinstance(capacity, float):
        numerator = math.pow(capacity, channels) / math.factorial(channels)
        denominator = 0.0
        k = 0
        while k < channels:
            denominator += (math.pow(capacity, k) / math.factorial(k))
            k+=1

        return numerator / denominator
    else:
        return None

# 

# determine capacity given GOS and channels
def E_Erlang(GOS, channels):
    a = 0.0
    b = float(channels)
    c = 0.0

    gos_a = 0.0
    gos_b = 0.0
    gos_c = 0.0

    # increasing to 0.001 didn't help too much
    while math.fabs(a-b) >= 0.001:
        # average a and b
        c = (a+b)/2

        gos_a = GOS_Erlang(channels, a)
        gos_b = GOS_Erlang(channels, b)
        gos_c = GOS_Erlang(channels, c)

        # replace a or b
        if GOS > gos_c:
            a = c
        else:
            b = c

    return c

channels = [7, 15, 22, 30, 37, 45, 52, 60]
gos = 0.01

print("Capacity of channels for GOS 0.01")
for channel in channels:
    print("%d:\t%.3f" % (channel, E_Erlang(gos, channel)))