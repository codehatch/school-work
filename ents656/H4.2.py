#!/usr/bin/env python3

import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import math

# x: 10000 evenly spaced values from 0 to 6
X_MIN = 0
X_MAX = 6
X_NUM = 10000
x = np.linspace(X_MIN, X_MAX, X_NUM)

# y = sin(x)
y = np.sin(x)

# n: array of 10000 normally distributed random numbers with mean=0 and std=0.1
N_NUM_SAMP = 10000
N_MEAN = 0.0
N_STD = 0.1
n = rnd.normal(N_MEAN, N_STD, size = N_NUM_SAMP)

# z = y + n
z = y + n

plt.subplot2grid((2,2),(0,0),colspan=2)
plt.plot(x, z, 'b-')
plt.plot(x, y, 'w--')
plt.title('sine wave in noise [0:6]')
plt.xlabel('radians')
plt.ylabel('values')
plt.legend(['singal+noise', 'signal'])

plt.subplot2grid((2,2),(1,0))
plt.plot(x, z)
plt.plot(x, y, 'w--')
plt.axis([1, 1.5, 0.5, 1.5])
plt.title('sine wave in noise[1:1.5]')
plt.xlabel('radians')
plt.ylabel('values')
plt.legend(['signal+noise', 'signal'])

plt.subplot2grid((2,2),(1,1))
plt.plot(x, z)
plt.plot(x, y, 'r--')
plt.axis([1, 1.05, 0.5, 1.5])
plt.title('sine wave in noise [1:1.05]')
plt.xlabel('radians')
plt.ylabel('values')
plt.legend(['signal+noise', 'signal'])

plt.show()
