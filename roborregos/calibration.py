import cv2
import numpy as np
import os

def nothing(x):
    pass

#
#       Cambia la imagen acá
#
image = os.path.join(os.path.dirname(__file__), 'WIN_20251015_16_28_32_Pro.jpg')
image = cv2.imread(image)

if image is None:
    print("Error: Image not found. Check the file path.")
    exit()

# Create a window to display the trackbars
cv2.namedWindow('Trackbars')
cv2.resizeWindow('Trackbars', 600, 300)

# Create trackbars for the Lower and Upper HSV bounds
# Hue (H) has a range of 0-179 in OpenCV
cv2.createTrackbar('L - H', 'Trackbars', 0, 179, nothing)
cv2.createTrackbar('L - S', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('L - V', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('U - H', 'Trackbars', 179, 179, nothing)
cv2.createTrackbar('U - S', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('U - V', 'Trackbars', 255, 255, nothing)

# Set some initial trackbar positions (a good starting point for orange)
cv2.setTrackbarPos('L - H', 'Trackbars', 5)
cv2.setTrackbarPos('L - S', 'Trackbars', 100)
cv2.setTrackbarPos('L - V', 'Trackbars', 100)
cv2.setTrackbarPos('U - H', 'Trackbars', 20)
cv2.setTrackbarPos('U - S', 'Trackbars', 255)
cv2.setTrackbarPos('U - V', 'Trackbars', 255)

print("Adjust the trackbars to isolate the orange ball in the 'Mask' window.")
print("Press 'q' to quit and print the final HSV values.")

while True:
    # Convert the image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Get the current trackbar positions
    l_h = cv2.getTrackbarPos('L - H', 'Trackbars')
    l_s = cv2.getTrackbarPos('L - S', 'Trackbars')
    l_v = cv2.getTrackbarPos('L - V', 'Trackbars')
    u_h = cv2.getTrackbarPos('U - H', 'Trackbars')
    u_s = cv2.getTrackbarPos('U - S', 'Trackbars')
    u_v = cv2.getTrackbarPos('U - V', 'Trackbars')

    # Create the lower and upper HSV range arrays
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])

    # Create the mask using the current range
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # Display the original image and the mask
    cv2.imshow('Original Image', image)
    cv2.imshow('Mask', mask)

    # Exit the loop if 'q' is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# When the loop is exited, print the final HSV values
print("\n--- Calibration Complete ---")
print(f"np.array([{l_h}, {l_s}, {l_v}])")
print(f"np.array([{u_h}, {u_s}, {u_v}])")
print("----------------------------")

cv2.destroyAllWindows()