
import csv
import pandas as pd
import numpy as np  # Import Numpy library
from numpy import savetxt


# df = pd.read_csv('data4nn.csv', header = None)

df = pd.read_csv('data4nn.csv', names = ('x', 'y'))
datos=df.to_numpy()

x = datos[:, 0]
y = datos [:, 1]

print(x)
print(y)

# data_file = 'C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/NN/data.csv'
# csv_reader = csv.reader(data_file)
# print(csv_reader)