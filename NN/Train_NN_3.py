import torch
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
import glob
import PIL.Image
import os
import numpy as np
import cv2
import csv
import pandas as pd


class XYDataset(torch.utils.data.Dataset):

    def __init__(self, directory, random_hflips=False):
        self.directory = directory
        self.random_hflips = random_hflips
        self.image_paths = glob.glob(os.path.join(self.directory, '*.jpg'))
        self.color_jitter = transforms.ColorJitter(0.3, 0.3, 0.3, 0.3)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]

        image = PIL.Image.open(image_path)

        if float(np.random.rand(1)) > 0.5:
            image = transforms.functional.hflip(image)

        image = self.color_jitter(image)
        image = transforms.functional.resize(image, (224, 224))
        image = transforms.functional.to_tensor(image)
        image = image.numpy()[::-1].copy()
        image = torch.from_numpy(image)

        # data_file = 'C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/NN/data.csv'
        df = pd.read_csv('data4nn.csv', names=('x', 'y'))
        datos = df.to_numpy()

        x = datos[:, 0]
        y = datos[:, 1]

        return image, torch.tensor([x, y]).float()
#


dataset = XYDataset('C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/NN/Imagenes/', random_hflips=False)

print(len(dataset))
print(dataset[1])

