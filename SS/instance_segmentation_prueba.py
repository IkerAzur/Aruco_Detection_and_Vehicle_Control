from pixellib.instance import instance_segmentation
import cv2

cam = cv2.VideoCapture(0)

segment_video = instance_segmentation()

segment_video.load_model("C:/Users/Iker/OneDrive/Documentos/Universidad/TFM/TFM Iker/ModelosSS/mask_rcnn_coco.h5")

segment_video.process_video(cam, show_bboxes=True, extract_segmented_objects=True, output_video_name="instance.mp4")