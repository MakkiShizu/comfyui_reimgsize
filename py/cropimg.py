import comfy.utils


class Cropimg:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_method": (s.upscale_methods,),
                "width_ratio": ("INT", {"default": 1, "min": 1, "max": 64, "step": 1}),
                "height_ratio": ("INT", {"default": 1, "min": 1, "max": 64, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "crop"
    CATEGORY = "image"

    def crop(self, image, upscale_method, width_ratio, height_ratio):
        samples = image.movedim(-1, 1)

        original_width = samples.shape[3]
        original_height = samples.shape[2]
        original_resolution = original_width * original_height

        desired_aspect = width_ratio / height_ratio
        aspect = original_width / original_height

        if aspect > desired_aspect:
            new_width = int(original_height * desired_aspect)
            new_height = original_height
        else:
            new_width = original_width
            new_height = int(original_width / desired_aspect)

        target_resolution = new_width * new_height
        scale = (original_resolution / target_resolution) ** 0.5

        new_width = int(new_width * scale)
        new_height = int(new_height * scale)

        s = comfy.utils.common_upscale(
            samples, new_width, new_height, upscale_method, "center"
        )
        s = s.movedim(1, -1)

        return (s,)


NODE_CLASS_MAPPINGS = {"Cropimg": Cropimg}
NODE_DISPLAY_NAME_MAPPINGS = {"Cropimg": "Crop_Image_Ratio"}
