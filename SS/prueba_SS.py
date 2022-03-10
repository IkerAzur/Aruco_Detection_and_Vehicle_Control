import pixellib
from pixellib.semantic import semantic_segmentation

segment_image = semantic_segmentation()
segment_image.load_ade20k_model("C:/Users/Iker/Downloads/deeplabv3_xception65_ade20k.h5")
segment_image.segmentAsAde20k("imagen_a_segmentar.jpeg", output_image_name= "imagen_segmentada.jpeg")