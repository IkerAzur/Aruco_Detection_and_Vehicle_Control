'''
5-3-22
Programa para el seguimiento de aruco y obtención de imágenes para
el entrenamiento de una red neuronal de regresión.
El Aruco cuando sea detectado en la zona izquierda de la imagen,
se guardarán tanto la imagen recortada como las consignas de velocidad
y ángulo del vehículo
Iker Azurmendi
GitHub: https://github.com/IkerAzur/Aruco_Detection_and_Vehicle_Control
'''

# Librerías necesrias para el desarrollo del proyecto
import cv2                  # Importar la librería OpenCV
import numpy as np          # Importar la librería Numpy
from numpy import savetxt   # Importar la librería para guardar archivos de texto
import keyboard             # Importar la librería para el teclado
import sys
import pyads

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

# Vectores de salida de la red
salidas_nn_vel = []
salidas_nn_ang = []

def main():

    # Comprpbar aruco valido
    if ARUCO_DICT.get(desired_aruco_dictionary, None) is None:
        print("[INFO] ArUCo tag of '{}' is not supported".format(
            args["type"]))
        sys.exit(0)

    # Inciar conexión y conectar con el PLC
    plc = pyads.Connection('169.254.153.119.1.1', 851) # IP y puerto para la conexión ADS con TwinCat
    plc.open()
    plc.write_by_name("GVL_Matlab.bStart", True, pyads. PLCTYPE_BOOL)

    # Cargar el diccionario de ArUco
    print("[INFO] detecting '{}' markers...".format(
        desired_aruco_dictionary))
    this_aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])
    this_aruco_parameters = cv2.aruco.DetectorParameters_create()

    # Iniciar el vídeo
    video = cv2.VideoCapture(0)

    # Parámetros para el controol de vehículo
    K1 = 0.01875                # Ganancia para el control del vehículo
    angulo_maximo = 1.50        # Error máximo del ángulo
    v_max = 3                   # Velocidad máxima del vehículo

    # Inicializar el contador de imágenes
    num_imagen = 0

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

                # Nos quedamos con las esquinas derechas para el posterior recorte de la imagen
                esquina_arriba_derecha = arriba_derecha[0]
                esquina_abajo_derecha = abajo_derecha[0]

                # Calcular y dibujar el centro del marcador ArUco
                centro_x = int((arriba_izquierda[0] + abajo_derecha[0]) / 2.0)
                centro_y = int((arriba_izquierda[1] + abajo_derecha[1]) / 2.0)
                cv2.circle(frame, (centro_x, centro_y), 4, (0, 0, 255), -1)

                # Si el aruco es el 991, actuamos
                if id_aruco == 991:

                    # Recortar la imagen y guardar si está en la zona izquierda (25%)
                    # Además, solo daremos orden de movimiento si estamos en ese 25% de la imagen
                    if esquina_arriba_derecha < 0.25 * 640 and esquina_abajo_derecha < 0.25 * 640:

                        # Guardar la captura de pantalla si se cumplen las condiciones
                        captura = video.read()[1]
                        captura_recortada = captura[int(0.25*height):height, int(0.25*width):width]

                        # Mostrar la captura recortada
                        cv2.imshow("captura recortada", captura_recortada)

                        # Control del vehículo: velocidad y ángulo de las ruedas
                        error = width / 8 - centro_x
                        angulo = K1 * error
                        velocidad = v_max - (abs(angulo)/angulo_maximo) * v_max

                        # Actualizar vectores salidas
                        salidas_nn_vel.append(velocidad)
                        salidas_nn_ang.append(angulo)

                        # Guardar las imagenes recortadas
                        directorio = "C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/Vehicle_control/Imagenes_recortadas/"
                        directorio = "C:/Users/dteso001/Desktop/Iker/ArUco_IKER/Aruco_Detection_and_Vehicle_Control/Vehicle_control/Imagenes_recortadas_3/"

                        num_imagen = num_imagen + 1
                        filename = directorio + 'Vel-y-Ang_%s_%03f_%03f.jpg' % (str(num_imagen), velocidad, angulo)
                        cv2.imwrite(filename, captura_recortada)

                    else:
                        angulo = 0
                        velocidad = 0

        # Si no se detecta Aruco daremos la orden de no movimiento al robot
        else:
            angulo = 0
            velocidad = 0

        plc.write_by_name("GVL_Matlab.Direccion", angulo, pyads.PLCTYPE_REAL)
        plc.write_by_name("GVL_Matlab.Velocidad", velocidad, pyads.PLCTYPE_REAL)


        cv2.imshow('frame', frame)

        # Si se presiona "q" en el teclado,
        # salir del bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Crear vector de salidas conjunto [vel, ang]
    salidas_nn = np.stack((salidas_nn_vel, salidas_nn_ang), axis=1)
    # print(salidas_nn)
    # Guardar valores de dos formas diferentes
    # savetxt('data4nn.csv', salidas_nn, delimiter=',')
    # np.save('data4nn_numpy.npy', salidas_nn)

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


