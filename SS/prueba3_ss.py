# Prueba nº 3 - SS - Iker
import pixellib
from pixellib.semantic import semantic_segmentation
import cv2
from tensorflow.keras.layers import BatchNormalization

cam = cv2.VideoCapture(0)

segment_video = semantic_segmentation()
segment_video.load_ade20k_model("C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/SS/deeplabv3_xception65_ade20k.h5")

seg, result = segment_video.process_camera_ade20k(cam, overlay = True, frames_per_second=15, show_frames=True, frame_name="frame", output_video_name="C:/Users/Iker/PycharmProjects/Aruco_Detection_and_Vehicle_Control/SS/SS_v1.mp4")