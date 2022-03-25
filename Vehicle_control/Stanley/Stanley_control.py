
import numpy as np
import math


# Parametros camara
thita_camara = 15 # Angulo de giro de la camara (º)
h_camara = 0.20 # Altura a la que está situada la camara (m)

# Parametros del control Stanley
k1 = 1              # Ganancia proporcional 1
k2 = 1              # Ganancia proporcional 2
k3 = 0.5            # Ganancia proporcional de velocidad
d_min = 0           # Ángulo mínimo de giro
d_max = 90          # Ángulo máximo de giro

# Parametros que se obtienen del codigo POSE aruco
psi =               # Error de encabezamiento

error = 1           # Desplazamiento lateral

x_aruco =
z_aruco =

# Trigonometria
z_hor = z_aruco * math.cos(thita_camara)
d_hor = math.sqrt(z_hor**2+x_aurco**2)
dist =  math.sqrt(d_hor**2+h_camara*2)           # Distancia vehículo-aruco

vel = k3 * dist     # Velocidad del vehículo

delta = k1 * (psi + np.arctan2(k2*error/vel))

if delta < 0:
    delta = 0
elif delta > 0:
    delta = 90
else:
    delta=delta

