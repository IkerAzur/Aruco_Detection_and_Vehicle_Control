import cv2

def screenshot():
    global cam
    cv2.imshow("screenshot", cam.read()[1]) # shows the screenshot directly
    #cv2.imwrite('screenshot.png',cam.read()[1]) # or saves it to disk

if __name__ == '__main__':

    cam = cv2.VideoCapture(0) # initializes video capture

    while True:
        ret, img = cam.read()
        cv2.imshow("cameraFeed", img) # a window is needed as a context for key capturing (here, I display the camera feed, but there could be anything in the window)
        ch = cv2.waitKey(5)
        if ch == ord('q'):
            break
        if ch == ord('c'): # calls screenshot function when 'c' is pressed
            screenshot()

    cv2.destroyAllWindows()