#!/usr/bin/env python

'''
Welcome to the ArUco Marker Detector!

This program:
  - Detects ArUco markers using OpenCV and Python
'''

from __future__ import print_function  # Python 2/3 compatibility
import cv2  # Import the OpenCV library
import numpy as np  # Import Numpy library
from numpy import savetxt

# Project: ArUco Marker Detector
# Date created: 12/18/2021
# Python version: 3.8
# Reference: https://www.pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/

desired_aruco_dictionary = "DICT_4X4_1000"

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

salidas_nn_x = []
salidas_nn_y = []

def main():
    """
    Main method of the program.
    """
    # Check that we have a valid ArUco marker
    if ARUCO_DICT.get(desired_aruco_dictionary, None) is None:
        print("[INFO] ArUCo tag of '{}' is not supported".format(
            args["type"]))
        sys.exit(0)

    # Load the ArUco dictionary
    print("[INFO] detecting '{}' markers...".format(
        desired_aruco_dictionary))
    this_aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])
    this_aruco_parameters = cv2.aruco.DetectorParameters_create()

    # Start the video stream
    cap = cv2.VideoCapture(0)

    num_imagen = 0

    while (True):

        top__right = 1000
        bottom__right = 1000

        # Capture frame-by-frame
        # This method returns True/False as well
        # as the video frame.
        ret, frame = cap.read()

        # Detect ArUco markers in the video frame
        (corners, ids, rejected) = cv2.aruco.detectMarkers(
            frame, this_aruco_dictionary, parameters=this_aruco_parameters)

        # Check that at least one ArUco marker was detected
        if len(corners) > 0:
            # Flatten the ArUco IDs list
            ids = ids.flatten()
            id_aruco = int(ids)
            print(id_aruco)

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

                print('top right x', top_right[0])
                print('bottom right x', bottom_right[0])
                print('top left x', top_left[0])
                print('bottom left x', bottom_left[0])

                top__right = top_right[0]
                bottom__right = bottom_right[0]

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

        # Display the resulting frame
        cv2.imshow('frame', frame)


        if top__right < 0.2 * 640 and bottom__right< 0.2 * 640:
            print('bacalao')
            captura = cap.read()[1]
            height, width = captura.shape[:2]
            print(height, width)
            captura_recortada = captura[96:480, 128:640]
            new_image = cv2.resize(captura_recortada, (224, 224))

            # Poner punto rojo en la imagen en funcion del id del aruco
            if id_aruco == 1:
                x = 112
                y = 112
                new_image = cv2.circle(new_image, (x, y), radius=3, color=(0, 0, 255), thickness=-1)
            elif id_aruco == 2:
                x = 200
                y = 112
                new_image = cv2.circle(new_image, (x, y), radius=3, color=(0, 0, 255), thickness=-1)
            else:
                x = 24
                y = 112
                new_image = cv2.circle(new_image, (x, y), radius=3, color=(0, 0, 255), thickness=-1)

            salidas_nn_x.append(x)
            salidas_nn_y.append(y)

            cv2.imshow("Imagen redimensionada", new_image)
            # directorio = "C:/Users/Iker/PycharmProjects/Aruco_v2/NN/Imagenes/"
            #directorio = "C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/NN/Imagenes/"
            directorio = "C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/NN/Imagenes_redimensionadas/"
            #texto_imagen = "captura_recortada_"
            #str_id_aruco = str(id_aruco) + "_"
            num_imagen = num_imagen + 1
            #formato_imagen = ".jpg"
            #filename = directorio + texto_imagen + str_id_aruco + str(num_imagen) + formato_imagen
            filename = directorio + 'xy_%03d_%03d_%s.jpg' % (x, y, str(num_imagen))
            cv2.imwrite(filename, new_image)


        # If "q" is pressed on the keyboard,
        # exit this loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    salidas_nn = np.stack((salidas_nn_x, salidas_nn_y), axis = 1)
    print(salidas_nn)
    savetxt('data4nn.csv', salidas_nn, delimiter=',')
    np.save('data4nn_numpy.npy', salidas_nn)

    # Close down the video stream
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)
    main()