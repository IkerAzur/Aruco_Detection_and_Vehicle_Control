import numpy as np
import cv2
import cv2.aruco as aruco

image = cv2.imread("../Captura.PNG")
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(
    image, aruco_dict, parameters=parameters)
print(corners, ids, rejectedImgPoints)
aruco.drawDetectedMarkers(image, corners, ids)
aruco.drawDetectedMarkers(image, rejectedImgPoints, borderColor=(100, 0, 240))

cv2.imshow('so52814747', image)
cv2.waitKey(0)
cv2.destroyAllWindows()