import cv2
import glob
import matplotlib

images = [cv2.imread(file) for file in glob.glob('C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/NN/Imagenes/*.jpg')]

print(len(images))

im = images[0]
x, y, _ = im.shape
print(x, y)

# cv2.imshow("alcachofa", images[2])
# cv2.waitKey(0)
# cv2.destroyAllWindows()


