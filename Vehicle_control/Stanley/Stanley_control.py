
from __future__ import print_function  # Python 2/3 compatibility
import cv2  # Import the OpenCV library
import numpy as np  # Import Numpy library
from scipy.spatial.transform import Rotation as R
import math  # Math library
import time


# Diccionario de deteccion de arucos
aruco_dictionary_name = "DICT_4X4_1000"

# Diccionarios Arucos en OpenCV
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

# Dimension de un lado del aruco en metros
aruco_marker_side_length = 0.0735

# Parametros de calibracion
camera_calibration_parameters_filename = 'calibration_chessboard.yaml'

# Tranformada de euler para obtener roll, pitch y yaw en radianes
def euler_from_quaternion(x, y, z, w):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return roll_x, pitch_y, yaw_z  # in radians

# Parametros camara
thita_camara = 15 # Angulo de giro de la camara (??)
h_camara = 0.20 # Altura a la que est?? situada la camara (m)

# Parametros del control Stanley
k1 = 1              # Ganancia proporcional 1
k2 = 0.5              # Ganancia proporcional 2
k3 = 10            # Ganancia proporcional de velocidad
d_min = 0           # ??ngulo m??nimo de giro
d_max = 90          # ??ngulo m??ximo de giro


def main():

    # Inciar parametros a cero
    yaw_z = 0
    transform_translation_x = 0
    transform_translation_z = 0

    # Cargar los parametros de calibracion de la camara
    cv_file = cv2.FileStorage(
        camera_calibration_parameters_filename, cv2.FILE_STORAGE_READ)
    mtx = cv_file.getNode('K').mat()
    dst = cv_file.getNode('D').mat()
    cv_file.release()

    # Cargar el diccionario de Aruco
    print("[INFO] detecting '{}' markers...".format(
        aruco_dictionary_name))
    this_aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_dictionary_name])
    this_aruco_parameters = cv2.aruco.DetectorParameters_create()

    # Empezar la captura de video
    cap = cv2.VideoCapture(0)

    while (True):

        # Capture frame-by-frame
        # This method returns True/False as well
        # as the video frame.
        ret, frame = cap.read()

        # print(frame.shape)

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

            # Print the pose for the ArUco marker
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

                # Store the rotation information
                rotation_matrix = np.eye(4)
                rotation_matrix[0:3, 0:3] = cv2.Rodrigues(np.array(rvecs[i][0]))[0]
                r = R.from_matrix(rotation_matrix[0:3, 0:3])
                quat = r.as_quat()

                # Quaternion format
                transform_rotation_x = quat[0]
                transform_rotation_y = quat[1]
                transform_rotation_z = quat[2]
                transform_rotation_w = quat[3]

                # Euler angle format in radians
                roll_x, pitch_y, yaw_z = euler_from_quaternion(transform_rotation_x,
                                                               transform_rotation_y,
                                                               transform_rotation_z,
                                                               transform_rotation_w)

                roll_x = math.degrees(roll_x)
                pitch_y = math.degrees(pitch_y)
                yaw_z = math.degrees(yaw_z)
                # print("transform_translation_x: {}".format(transform_translation_x))
                # print("transform_translation_y: {}".format(transform_translation_y))
                # print("transform_translation_z: {}".format(transform_translation_z))
                # print("roll_x: {}".format(roll_x))
                # print("pitch_y: {}".format(pitch_y))
                # print("yaw_z: {}".format(yaw_z))

                print(i, transform_translation_x, transform_translation_z, yaw_z)
                time.sleep(2)

                # Draw the axes on the marker
                cv2.aruco.drawAxis(frame, mtx, dst, rvecs[i], tvecs[i], 0.05)

        # Parametros que se obtienen del codigo POSE aruco
        psi = yaw_z  # Error de encabezamiento

        x_aruco = transform_translation_x
        z_aruco = transform_translation_z

        # Trigonometria
        z_hor = z_aruco * math.cos(thita_camara)
        d_hor = math.sqrt(z_hor ** 2 + x_aruco ** 2)
        dist = math.sqrt(d_hor ** 2 + h_camara ** 2)  # Distancia veh??culo-aruco

        vel = k3 * dist  # Velocidad del veh??culo

        # Saturacion de velocidad
        if vel < 1:
            vel = 1
        elif vel > 9:
            vel = 9
        else:
            vel = vel

        beta = math.atan2(x_aruco, z_hor)
        psi_1 = psi - beta

        error = d_hor * math.sin(psi_1) # Desplazamiento lateral

        delta = k1 * (psi + np.arctan2(k2 * error, vel))

        if delta < -45:
            delta = -45
        elif delta > 45:
            delta = 45
        else:
            delta = delta

        print(vel, delta)
        print(x_aruco, z_aruco, psi)

        #time.sleep(2)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # If "q" is pressed on the keyboard,
        # exit this loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Close down the video stream
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)
    main()