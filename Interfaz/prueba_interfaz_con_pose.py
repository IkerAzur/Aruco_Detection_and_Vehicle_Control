
from __future__ import print_function  # Python 2/3 compatibility
# Para interfaz
import pygame
import os
import time
import math
from utilidades import scale_image, blit_rotate_center

# Para estimación pose

import cv2  # Import the OpenCV library
import numpy as np  # Import Numpy library
from scipy.spatial.transform import Rotation as R
import math  # Math library

fondo = pygame.image.load(os.path.join('Imagenes_interfaz', 'labo.png'))
agv = scale_image(pygame.image.load(os.path.join('Imagenes_interfaz', 'agv3.png')), 0.35)

width, height = fondo.get_width(), fondo.get_height()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interfaz")

FPS = 60

# Dictionary that was used to generate the ArUco marker
aruco_dictionary_name = "DICT_4X4_1000"

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

# Side length of the ArUco marker in meters
aruco_marker_side_length = 0.0785

# Calibration parameters yaml file
camera_calibration_parameters_filename = 'calibration_chessboard.yaml'

class AbstractCar:

    def __init__(self, x, y):
        self.img = self.IMG
        self.angle = 0
        self.x, self.y = self.START_POS

    def move(self, x, y):

        self.x = abs(x) * 600
        self.y = abs(y) * 200

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

class ComputerCar(AbstractCar):
    IMG = agv
    START_POS = (100, 450)



run = True
clock = pygame.time.Clock()

images = [(fondo, (0, 0))]
car = ComputerCar(0, 0)


def draw(win, images, car):
    for img, pos in images:
        win.blit(img, pos)

    car.draw(win)
    pygame.display.update()

# Load the camera parameters from the saved file
cv_file = cv2.FileStorage(
    camera_calibration_parameters_filename, cv2.FILE_STORAGE_READ)
mtx = cv_file.getNode('K').mat()
dst = cv_file.getNode('D').mat()
cv_file.release()

# Load the ArUco dictionary
print("[INFO] detecting '{}' markers...".format(
    aruco_dictionary_name))
this_aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_dictionary_name])
this_aruco_parameters = cv2.aruco.DetectorParameters_create()

# Start the video stream
cap = cv2.VideoCapture(0)

transform_translation_x = 0
transform_translation_z = 0

while run:

    clock.tick(FPS)

    draw(win, images, car)

    # Capture frame-by-frame
    # This method returns True/False as well
    # as the video frame.
    ret, frame = cap.read()

    # Detect ArUco markers in the video frame
    (corners, marker_ids, rejected) = cv2.aruco.detectMarkers(
        frame, this_aruco_dictionary, parameters=this_aruco_parameters,
        cameraMatrix=mtx, distCoeff=dst)

    # Check that at least one ArUco marker was detected
    if marker_ids is not None:

        # Draw a square around detected markers in the video frame
        cv2.aruco.drawDetectedMarkers(frame, corners, marker_ids)

        # Get the rotation and translation vectors
        rvecs, tvecs, obj_points = cv2.aruco.estimatePoseSingleMarkers(
            corners,
            aruco_marker_side_length,
            mtx,
            dst)

        # The pose of the marker is with respect to the camera lens frame.
        # Imagine you are looking through the camera viewfinder,
        # the camera lens frame's:
        # x-axis points to the right
        # y-axis points straight down towards your toes
        # z-axis points straight ahead away from your eye, out of the camera
        for i, marker_id in enumerate(marker_ids):
            # Store the translation (i.e. position) information
            transform_translation_x = tvecs[i][0][0]
            transform_translation_y = tvecs[i][0][1]
            transform_translation_z = tvecs[i][0][2]


    # Display the resulting frame
    cv2.imshow('frame', frame)

    car.move(transform_translation_x, transform_translation_z)

    # If "q" is pressed on the keyboard,
    # exit this loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break



pygame.quit()
# Close down the video stream
cap.release()
cv2.destroyAllWindows()