#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

# x: 101 evenly spaced values between 0 and 10 (including 0 and 10)
X_MIN = 0
X_MAX = 10
X_NUM = 101
X_ARR =   np.linspace(X_MIN, X_MAX, X_NUM)

def plot_exponent(n):
    # y1 = (x^n)*(e^-x)
    Y1_ARR = np.power(X_ARR, n) * np.exp(-X_ARR)

    # y2 = x / (x^2 + 1)    
    Y2_ARR = X_ARR / (np.power(X_ARR, 2) + 1)

    # plot y1 with blue line
    plt.plot(X_ARR, Y1_ARR, 'b-')

    # plot y2 with red dot-dashed line
    plt.plot(X_ARR, Y2_ARR, 'r-.')

    # Labels
    plt.xlabel('x, n=%.1f' % n)
    plt.ylabel('f(x)')
    plt.title('$x/(x^2+1)$ vs $x^ne^{-x}$')

    # Display plot
    plt.show()


while True:
    n_str = input("Enter exponent n (q to quit)>")

    if n_str == "q":
        break

    try:
        n = float(n_str)
        print("Close plot window to continue...")
        plot_exponent(n)
    except ValueError:
        print("That's not a number!!!")

    
