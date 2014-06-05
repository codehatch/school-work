#!/usr/bin/env python3

import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import math


GAUS_NUM_SAMP = 100000
GAUS_MEAN = 0.0
GAUS_STD = (1 / math.sqrt(2))

gaussian1 = rnd.normal(GAUS_MEAN, GAUS_STD, size = GAUS_NUM_SAMP)
gaussian2 = rnd.normal(GAUS_MEAN, GAUS_STD, size = GAUS_NUM_SAMP)

gaussian = gaussian1 + 0j
gaussian.imag = gaussian2

NUM_BINS = 100
plt.hist(np.abs(gaussian), NUM_BINS, normed=True)

plt.title('Rayleigh distribution histogram, 100000 samples')
plt.xlabel('distribution value')
plt.ylabel('number of occurences')

plt.show()
