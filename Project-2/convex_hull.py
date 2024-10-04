import matplotlib.pyplot as plt
import numpy as np

# Helper function to find the orientation of the triplet (a, b, c)
# Returns:
# 0 -> a, b, c are collinear
# 1 -> Clockwise
# -1 -> Counterclockwise
def orientation(a, b, c):
    res = (b[1]-a[1]) * (c[0]-b[0]) - (c[1]-b[1]) * (b[0]-a[0])
    if res == 0:
        return 0
    if res > 0:
        return 1
    return -1

# Code for finding the Upper Tangent of both the Hulls
def find_upper_tangent(start_left, start_right, left_hull, right_hull):
    done=False
    while not done:  # finding the lower tangent
        done = True
        while orientation(right_hull[start_right], left_hull[start_left], left_hull[(start_left + 1) % len(left_hull)]) >= 0:
            start_left = (start_left + 1) % len(left_hull)
        while orientation(left_hull[start_left], right_hull[start_right], right_hull[(len(right_hull) + start_right - 1) % len(right_hull)]) <= 0:
            start_right = (start_right - 1) % len(right_hull)
            done=False
    return start_left, start_right


# Code for finding the Lower Tangent of both the Hulls
def find_lower_tangent(start_left, start_right, left_hull, right_hull):
    done=False
    while not done:  # finding the lower tangent
        done = True
        while orientation(left_hull[start_left], right_hull[start_right], right_hull[(start_right + 1) % len(right_hull)]) >= 0:
            start_right = (start_right + 1) % len(right_hull)
        while orientation(right_hull[start_right], left_hull[start_left], left_hull[(len(left_hull)+start_left-1) % len(left_hull)]) <= 0:
            start_left = (start_left - 1) % len(left_hull)
            done=False
    return start_left, start_right

def merge(left_hull, right_hull):
    left_hull_rightmost=left_hull.index(max(left_hull, key=lambda hull: hull[0]))
    right_hull_leftmost=right_hull.index(min(right_hull, key=lambda hull: hull[0]))

    #Finding the tangents for Left and Right Hull
    upper_a, upper_b = find_upper_tangent(left_hull_rightmost, right_hull_leftmost, left_hull, right_hull)
    lower_a, lower_b = find_lower_tangent(left_hull_rightmost, right_hull_leftmost, left_hull, right_hull)

    #Merging the hulls based on the tangents
    # Add left hull elements from upper_a to lower_a (circularly)
    result = left_hull[upper_a:] + left_hull[:lower_a + 1] if lower_a < upper_a else left_hull[upper_a:lower_a + 1]
    # Add right hull elements from lower_b to upper_b (circularly)
    result += right_hull[lower_b:] + right_hull[:upper_b + 1] if upper_b < lower_b else right_hull[lower_b:upper_b + 1]

    return result



def convex_hull(points):
    #Base Condition
    if len(points) <= 3:
        # For 1 or 2 points, the convex hull is the points themselves
        if len(points) == 1:
            return points
        elif len(points) == 2:
            return points if points[0] != points[1] else [points[0]]

        # For 3 points, return the points sorted in counterclockwise order
        a, b, c = points
        if orientation(a, b, c) == 1:
            return [a, c, b]  # Clockwise order
        else:
            return [a, b, c]  # Counterclockwise order
    #Divide in two halves and recalling the function T(n/2)
    middle = len(points) //2
    left=points[:middle]
    right=points[middle:]
    left_hull = convex_hull(left)
    right_hull = convex_hull(right)
    # Merging the convex hulls O(n)
    return merge(left_hull, right_hull)



if __name__ == '__main__':
    for x in [10 ** i for i in range(1,7)]:
        ans = 0
        array_size = x
        # Generate random values for x and y within the range [0, 10000]
        x_range = (-9000000000000000001,9000000000000000001)
        y_range = (-9000000000000000001,9000000000000000001)

        # Combine x and y into a 2D array
        example = [(np.random.randint(x_range[0], x_range[1]), np.random.randint(y_range[0], y_range[1])) for _ in range(array_size)]
        # print(example)

        #Sort the points
        example.sort()
        hull = convex_hull(example)
        a, b = zip(*example)
        hx, hy = zip(*hull)

        plt.scatter(a, b)
        plt.plot(hx + (hx[0],), hy + (hy[0],), 'r-')
        plt.show()