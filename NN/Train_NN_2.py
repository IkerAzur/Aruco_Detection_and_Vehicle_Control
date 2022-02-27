from PIL import Image
import os, os.path

imgs = []
path = "C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/NN/Imagenes/"
valid_images = [".jpg", ".gif", ".png", ".tga"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs.append(Image.open(os.path.join(path, f)))

# path = 'C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/NN/Imagenes/'