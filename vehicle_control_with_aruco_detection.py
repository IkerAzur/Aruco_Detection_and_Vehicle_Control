#!/usr/bin/env python

'''
Welcome to the ArUco Marker Detector!

This program:
  - Detects ArUco markers using OpenCV and Python
'''

from __future__ import print_function  # Python 2/3 compatibility
import cv2  # Import the OpenCV library
import numpy as np  # Import Numpy library
import time
import sys
import keyboard
import pyads

# connect to plc and open connection
plc = pyads.Connection('169.254.153.119.1.1', 851)  # IP y puerto para la conexion ADS con TwinCat3
plc.open()

desired_aruco_dictionary = "DICT_ARUCO_ORIGINAL"

# The different ArUco dictionaries built into the OpenCV library.
ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}


def main():
    """
    Main method of the program.
    """
    # Check that we have a valid ArUco marker
    if ARUCO_DICT.get(desired_aruco_dictionary, None) is None:
        print("[INFO] ArUCo tag is not supported")
        sys.exit(0)

    # Load the ArUco dictionary
    print("[INFO] detecting '{}' markers...".format(
        desired_aruco_dictionary))
    this_aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])
    this_aruco_parameters = cv2.aruco.DetectorParameters_create()

    # Start the video stream
    cap = cv2.VideoCapture(0)

    num_arucos = 0
    end = -10

    # Inicio conexion
    plc.write_by_name("GVL_Matlab.bStart", True, pyads.PLCTYPE_BOOL)

    # Inicializar variables direccion y velocidad del vehiculo
    dir_vehiculo = 0
    vel_vehiculo = 0

    while (True):

        # Capture frame-by-frame
        # This method returns True/False as well
        # as the video frame.
        ret, frame = cap.read()

        # Detect ArUco markers in the video frame
        (corners, ids, rejected) = cv2.aruco.detectMarkers(
            frame, this_aruco_dictionary, parameters=this_aruco_parameters)

        # Check that at least one ArUco marker was detected
        if len(corners) > 0:

            start = time.time()

            if start - end > 10:
                num_arucos = num_arucos + 1
                print(num_arucos)
                if num_arucos == 1 or num_arucos == 2 or num_arucos == 4:
                    dir_vehiculo = 0
                    vel_vehiculo = 100
                elif num_arucos == 3:
                    dir_vehiculo = 1.5708
                    vel_vehiculo = 50
                else:
                    dir_vehiculo = 0
                    vel_vehiculo = 0

            # Flatten the ArUco IDs list
            ids = ids.flatten()

            # Loop over the detected ArUco corners
            for (marker_corner, marker_id) in zip(corners, ids):
                # Extract the marker corners
                corners = marker_corner.reshape((4, 2))
                (top_left, top_right, bottom_right, bottom_left) = corners

                # Convert the (x,y) coordinate pairs to integers
                top_right = (int(top_right[0]), int(top_right[1]))
                bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
                bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
                top_left = (int(top_left[0]), int(top_left[1]))

                # Draw the bounding box of the ArUco detection
                cv2.line(frame, top_left, top_right, (0, 255, 0), 2)
                cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
                cv2.line(frame, bottom_right, bottom_left, (0, 255, 0), 2)
                cv2.line(frame, bottom_left, top_left, (0, 255, 0), 2)

                # Calculate and draw the center of the ArUco marker
                center_x = int((top_left[0] + bottom_right[0]) / 2.0)
                center_y = int((top_left[1] + bottom_right[1]) / 2.0)
                cv2.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)

                # Draw the ArUco marker ID on the video frame
                # The ID is always located at the top_left of the ArUco marker
                cv2.putText(frame, str(marker_id),
                            (top_left[0], top_left[1] - 15),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)

                end = time.time()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        plc.write_by_name("GVL_Matlab.Direccion", dir_vehiculo, pyads.PLCTYPE_REAL)
        plc.write_by_name("GVL_Matlab.Velocidad", vel_vehiculo, pyads.PLCTYPE_REAL)

        # Varias formas de cerrar la conexion

        # Si se pulsa b se sale del bucle
        if keyboard.is_pressed('b'):
            break

        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        # If "q" is pressed on the keyboard,
        # exit this loop
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

        if num_arucos == 5:  # si se detecta el 5 aruco se termina el programa
            break

    # Close down the video stream
    cap.release()
    cv2.destroyAllWindows()

    # Cerrar la conexion con el plc


if __name__ == '__main__':
    print(__doc__)
    main()
