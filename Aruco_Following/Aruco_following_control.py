# Seguimiento de arucos
# Iker Azurmendi Marquinez

# Librerías necesrias para el desarrollo del proyecto
import cv2                  # Importar la librería OpenCV
import pyads                # Importar la librería para la conexión con TwinCat



# Diccionario del aruco que se va a detectar
desired_aruco_dictionary = "DICT_4X4_1000"

# Diccionario posibles de aruco
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

    # Inciar conexión y conectar con el PLC
    plc = pyads.Connection('169.254.153.119.1.1', 851) # IP y puerto para la conexión ADS con TwinCat
    plc.open()
    plc.write_by_name("GVL_Matlab.bStart", True, pyads. PLCTYPE_BOOL)

    # Cargar el diccionario de ArUco
    print("[INFO] detecting '{}' markers...".format(desired_aruco_dictionary))
    this_aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])
    this_aruco_parameters = cv2.aruco.DetectorParameters_create()

    # Iniciar el vídeo
    video = cv2.VideoCapture(0)

    # Parámetros para el controol de vehículo
    error_maximo = 320                          # Error máximo del ángulo
    angulo_maximo = 1.50                        # Error máximo del ángulo
    K = 0.75                                    # Ganancia de moderación del giro
    K1 = K * (angulo_maximo / error_maximo)     # Ganancia para el control del vehículo
    v_max = 4                                   # Velocidad máxima del vehículo


    while True:

        # Capturar fotograma a fotograma
        # Este método devuelve True / False, así como
        # el fotograma de vídeo.
        ret, frame = video.read()

        # Tamaño de la imagen
        height, width = frame.shape[:2]

        # Detectar Arucos en el frame del video
        (esquinas, ids, rechazado) = cv2.aruco.detectMarkers(
            frame, this_aruco_dictionary, parameters=this_aruco_parameters)

        # Se detecta Aruco si el número de esquinas es mayor que cero
        if len(esquinas) > 0:
            # Flatten the ArUco IDs list
            ids = ids.flatten()
            id_aruco = int(ids)
            print(id_aruco)

            # Obtener el centro del aruco
            # Para ello, se realiza un bucle sobre las esquinas de ArUco detectadas
            for (esquina_marcador, marcador_id) in zip(esquinas, ids):

                # Extract the marker corners
                esquinas = esquina_marcador.reshape((4, 2))
                (arriba_izquierda, arriba_derecha, abajo_derecha, abajo_izquierda) = esquinas

                # Convertir los pares de coordenadas (x,y) en enteros
                arriba_derecha = (int(arriba_derecha[0]), int(arriba_derecha[1]))
                abajo_derecha = (int(abajo_derecha[0]), int(abajo_derecha[1]))
                abajo_izquierda = (int(abajo_izquierda[0]), int(abajo_izquierda[1]))
                arriba_izquierda = (int(arriba_izquierda[0]), int(arriba_izquierda[1]))

                # Calcular y dibujar el centro del marcador ArUco
                centro_x = int((arriba_izquierda[0] + abajo_derecha[0]) / 2.0)
                centro_y = int((arriba_izquierda[1] + abajo_derecha[1]) / 2.0)
                cv2.circle(frame, (centro_x, centro_y), 4, (0, 0, 255), -1)

                # Si el aruco es el 991, actuamos
                if id_aruco == 991:

                    # Control del vehículo: velocidad y ángulo de las ruedas
                    error = (width/2) - centro_x
                    angulo = K1 * error
                    velocidad = v_max - (abs(angulo)/angulo_maximo) * v_max

                elif id_aruco == 1:

                    velocidad = 1
                    angulo = 1

        # Mandar consignas al PLC
        plc.write_by_name("GVL_Matlab.Direccion", angulo, pyads.PLCTYPE_REAL)
        plc.write_by_name("GVL_Matlab.Velocidad", velocidad, pyads.PLCTYPE_REAL)

        cv2.imshow('frame', frame)

        # Si se presiona "q" en el teclado,
        # salir del bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Cerrar la conexión con PLC
    plc.write_by_name("GVL_Matlab.Direccion", False, pyads.PLCTYPE_BOOL)    # Ángulo nulo
    plc.write_by_name("GVL_Matlab.Velocidad", 0, pyads.PLCTYPE_BOOL)        # Velocidad nula
    plc.write_by_name("GVL_Matlab.bStart", 0, pyads.PLCTYPE_BOOL)           # Cerrar conexión

    # Cerrar la conexión de video
    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print(__doc__)
    main()