from __future__ import print_function  # Python 2/3 compatibility
import cv2  # Import the OpenCV library
import numpy as np  # Import Numpy library
import torchvision
import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
import cv2
import PIL.Image

def preprocess(image):
    image = PIL.Image.fromarray(image)
    image = transforms.functional.to_tensor(image).to(device).half()
    return image[None, ...]

model = torchvision.models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(512, 2)

model.load_state_dict(torch.load('best_steering_model_xy.pth'))
device = torch.device('cuda')
model = model.to(device)
model = model.eval().half()

def main():

    # Start the video stream
    cap = cv2.VideoCapture(0)

#
    while (True):

        ret, frame = cap.read()

        xy = model(preprocess(frame)).detach().float().cpu().numpy().flatten()
        x = xy[0]
        y = xy[1]

        print(x, y)


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
