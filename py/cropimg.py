import comfy.utils


class Cropimg:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_method": (s.upscale_methods,),
                "height_ratio": ("INT", {"default": 1, "min": 1, "max": 64, "step": 1}),
                "width_ratio": ("INT", {"default": 1, "min": 1, "max": 64, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "crop"
    CATEGORY = "image"

    def crop(self, image, upscale_method, height_ratio, width_ratio):
        samples = image.movedim(-1, 1)

        original_width = samples.shape[3]
        original_height = samples.shape[2]

        desired_aspect = height_ratio / width_ratio
        aspect = original_width / original_height

        if aspect > desired_aspect:
            new_width = int(original_height * desired_aspect)
            new_height = original_height
        else:
            new_width = original_width
            new_height = int(original_width / desired_aspect)

        s = comfy.utils.common_upscale(
            samples, new_width, new_height, upscale_method, "center"
        )
        s = s.movedim(1, -1)

        return (s,)


NODE_CLASS_MAPPINGS = {"Cropimg": Cropimg}
NODE_DISPLAY_NAME_MAPPINGS = {"Cropimg": "Crop_Image_Ratio"}
