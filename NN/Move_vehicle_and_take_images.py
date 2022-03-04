# mover vehículo y capturar imagenes

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

                top__right = top_right[0]
                bottom__right = bottom_right[0]

            # en funcion del id del aruco vamos para delante o giramos
            if int(marker_id) == 1:
                dir_vehiculo = 0
                vel_vehiculo = 4.2
            elif int(marker_id) == 3:
                dir_vehiculo = 1.5708/5
                vel_vehiculo = 50
            else:
                dir_vehiculo = 0
                vel_vehiculo = 0

            # guardar imagenes si el aruco esta a la izquierda de la imagen
            if top__right < 0.2 * 640 and bottom__right < 0.2 * 640:
                print('bacalao')
                captura = cap.read()[1]
                height, width = captura.shape[:2]
                print(height, width)
                captura_recortada = captura[96:480, 128:640]
                new_image = cv2.resize(captura_recortada, (224, 224))

                # Poner punto rojo en la imagen en funcion del id del aruco
                if int(marker_id) == 1:
                    x = 112
                    y = 112
                    new_image = cv2.circle(new_image, (x, y), radius=3, color=(0, 0, 255), thickness=-1)
                elif int(marker_id) == 3:
                    x = 200
                    y = 112
                    new_image = cv2.circle(new_image, (x, y), radius=3, color=(0, 0, 255), thickness=-1)
                else:
                    x = 24
                    y = 112
                    new_image = cv2.circle(new_image, (x, y), radius=3, color=(0, 0, 255), thickness=-1)

                # guardar imagenes en directorio
                cv2.imshow("Imagen redimensionada", new_image)
                # directorio = "C:/Users/Iker/PycharmProjects/Aruco_v2/NN/Imagenes/"
                # directorio = "C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/NN/Imagenes/"
                # directorio = "C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/NN/Imagenes_redimensionadas/"
                directorio = "C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/NN/Imagenes_vehiculo_redimensionadas/"

                # texto_imagen = "captura_recortada_"
                # str_id_aruco = str(id_aruco) + "_"
                num_imagen = num_imagen + 1
                # formato_imagen = ".jpg"
                # filename = directorio + texto_imagen + str_id_aruco + str(num_imagen) + formato_imagen
                filename = directorio + 'xy_%03d_%03d_%s.jpg' % (x, y, str(num_imagen))
                cv2.imwrite(filename, new_image)


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

        if marker_id == 5:  # si se detecta el 5 aruco se termina el programa
            break

    # Close down the video stream
    cap.release()
    cv2.destroyAllWindows()

    # Cerrar la conexion con el plc
    plc.write_by_name("GVL_Matlab.bStart", False, pyads.PLCTYPE_BOOL)
    plc.write_by_name("GVL_Matlab.Direction", False, pyads.PLCTYPE_REAL)
    plc.write_by_name("GVL_Matlab.Velocidad", False, pyads.PLCTYPE_REAL)
    plc.close()


if __name__ == '__main__':
    print(__doc__)
    main()
