
import csv
import pandas as pd
import numpy as np  # Import Numpy library
from numpy import savetxt


df = pd.read_csv('data.csv')

print(df.to_string())


# data_file = 'C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/NN/data.csv'
# csv_reader = csv.reader(data_file)
# print(csv_reader)