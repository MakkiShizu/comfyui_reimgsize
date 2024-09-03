import comfy.utils


class Reimgsize:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_method": (s.upscale_methods, {"default": "bicubic"}),
                "img_size": (
                    "INT",
                    {"default": 1024, "min": 64, "max": 8192, "step": 1},
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


class Cropimg:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_method": (s.upscale_methods, {"default": "bicubic"}),
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


NODE_CLASS_MAPPINGS = {"Reimgsize": Reimgsize, "Cropimg": Cropimg}
NODE_DISPLAY_NAME_MAPPINGS = {"Reimgsize": "Reimgsize", "Cropimg": "Cropimg"}
