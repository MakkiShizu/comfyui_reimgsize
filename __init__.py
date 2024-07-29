from .py.reimgsize import Reimgsize
from .py.cropimg import Cropimg

NODE_CLASS_MAPPINGS = {"Resize": Reimgsize, "Cropimg": Cropimg}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Resize": "Image_Size_Normalization",
    "Cropimg": "Crop_Image_Ratio",
}
