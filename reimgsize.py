import comfy.utils


class Reimgsize:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_method": (s.upscale_methods,),
                "img_size": (
                    "INT",
                    {"default": 512, "min": 64, "max": 8192, "step": 1},
                ),
                "GCD": ("INT", {"default": 64, "min": 1, "max": 512, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "resize"
    CATEGORY = "image"

    def resize(self, image, img_size, upscale_method, GCD):
        samples = image.movedim(-1, 1)

        target_pixels = img_size**2
        original_width = samples.shape[3]
        original_height = samples.shape[2]

        aspect_ratio = original_width / original_height
        new_height = int((target_pixels / aspect_ratio) ** 0.5)
        new_width = int(new_height * aspect_ratio)

        new_width = round(new_width / GCD) * GCD
        new_height = round(new_height / GCD) * GCD

        s = comfy.utils.common_upscale(
            samples, new_width, new_height, upscale_method, "disabled"
        )
        s = s.movedim(1, -1)

        return (s,)


NODE_CLASS_MAPPINGS = {"Resize": Reimgsize}
NODE_DISPLAY_NAME_MAPPINGS = {"Resize": "Image_Size_Normalization"}
