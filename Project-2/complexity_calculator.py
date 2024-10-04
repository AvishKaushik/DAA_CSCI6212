import matplotlib.pyplot as plt
import numpy as np
import time
import math
from convex_hull import convex_hull


if __name__ == '__main__':
    nRange = []
    exp = []
    theo = []
    total_experimental = 0
    for x in [10 ** i for i in range(1,8)]:
        ans = 0
        for m in range(1):
            array_size = x

            # Generate random values for x and y within the range [0, 10000]
            x_range = (-9000000000000000001,9000000000000000001)
            y_range = (-9000000000000000001,9000000000000000001)

            # Combine x and y into a 2D array
            example = [(np.random.randint(x_range[0], x_range[1]), np.random.randint(y_range[0], y_range[1])) for _ in range(array_size)]
            # print(example)

            start = time.time_ns()
            #Sort the points
            example.sort()
            hull = convex_hull(example)
            end = time.time_ns()
            a, b = zip(*example)
            hx, hy = zip(*hull)

            plt.scatter(a, b)
            plt.plot(hx + (hx[0],), hy + (hy[0],), 'r-')
            plt.show()
            elapsed_time = end - start
            ans += elapsed_time
        nRange.append(x)
        exp.append(ans // 1)
        theo.append((x * (math.log2(x))))

    scaling_constant = np.average(exp) // np.average(theo)
    print("Experimental Average: ",np.average(exp) )
    print("Theoritical Average: ",np.average(theo) )
    print("Theoritical Values Before : ", theo)
    for i in range(len(theo)):
        theo[i] *= scaling_constant

    print("Value of n : ", nRange)
    print("Experimental Values : ", exp)
    print("Theoritical Values : ", theo)

    # Plotting
    plt.figure(figsize=(10, 6))

    # Plotting theoretical times
    plt.plot(nRange, theo, label="Theoretical Time (O(n * log n))", marker='o')

    # Plotting experimental times
    plt.plot(nRange, exp, label="Experimental Time", marker='x')

    # Logarithmic scale for better comparison
    plt.xscale('log')
    plt.yscale('log')

    plt.xlabel("n (log scale)")
    plt.ylabel("Time (log scale)")
    plt.title("Comparison of Theoretical and Experimental Time Complexity")
    plt.legend()

    # Show the plot
    plt.show()