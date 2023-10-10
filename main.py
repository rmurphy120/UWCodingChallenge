import cv2
import numpy as np


def main():
    # Loads the image
    image = cv2.imread('red.png')
    image = cv2.resize(image, (0, 0), fx=0.4, fy=0.4)

    # Converts the image to HSV color space
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

    # Creates a threshold of the image that only leaves orange(ish) colors
    img_thresh_low = cv2.inRange(img_hsv, np.array([0, 135, 135]),
                                 np.array([15, 255, 255]))
    img_thresh_high = cv2.inRange(img_hsv, np.array([159, 135, 135]),
                                  np.array([179, 255, 255]))
    img_thresh = cv2.bitwise_or(img_thresh_low, img_thresh_high)

    # Creating kernel
    kernel = np.ones((5, 5), np.uint8)

    # Smoothing the image
    thresh_smooth = cv2.erode(img_thresh, kernel)
    thresh_smooth = cv2.dilate(thresh_smooth, kernel)
    thresh_smooth = cv2.blur(thresh_smooth, (2, 2), 0)

    # Applies a Canny edge detector to the image
    edges = cv2.Canny(thresh_smooth, 30, 200)

    # Finds the contours in the image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Calculates the center of each contour and classifies it as left or right
    left_centers = []
    right_centers = []
    for each in contours:
        m = cv2.moments(each)
        if m["m00"] != 0:
            c_x = int(m["m10"] / m["m00"])
            c_y = int(m["m01"] / m["m00"])
            if c_x < 400:
                left_centers.append((c_x, c_y))
            else:
                right_centers.append((c_x, c_y))

    plot_line_of_best_fit(left_centers, image)
    plot_line_of_best_fit(right_centers, image)

    # Displays the image
    cv2.imshow('Cone Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("answer.png", image)


# Plots a line of best fit onto a set of points
def plot_line_of_best_fit(points, image):
    # Makes sure there are a valid number of points
    if len(points) <= 1:
        return

    points_x, points_y = split_points_into_x_and_y(points)

    # Calculates the slopes of the line of best fit when a point is removed
    slopes = []
    for i in range(0, len(points)):
        copy_points_x = points_x.copy()
        copy_points_y = points_y.copy()
        copy_points_x.remove(copy_points_x[i])
        copy_points_y.remove(copy_points_y[i])
        a, b = np.polyfit(copy_points_x, copy_points_y, 1)
        slopes.append(a)

    # Calculate the upper and lower limits using the IRQ
    q1 = np.percentile(slopes, 25, method='midpoint')
    q3 = np.percentile(slopes, 75, method='midpoint')
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    # Removes outliers
    counter = 0
    for i in range(0, len(slopes)):
        if not (lower < slopes[i] < upper):
            points.remove(points[i - counter])
            counter += 1

    points_x, points_y = split_points_into_x_and_y(points)

    # Creates line of best fit in form y = ax + b
    a, b = np.polyfit(points_x, points_y, 1)

    start_point = (0, int(b))
    end_point = (1000, int(b + a * 1000))

    # Maps the line onto the image
    cv2.line(image, start_point, end_point, (255, 255, 255), 2)


# Helper function that splits points into an array for the x component and an array for the y component
def split_points_into_x_and_y(points):
    points_x = []
    points_y = []
    for each in points:
        points_x.append(each[0])
        points_y.append(each[1])
    return points_x, points_y


main()
