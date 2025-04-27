import comfy.utils


class Reimgsize:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]
    crop_methods = ["disabled", "center"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_method": (s.upscale_methods, {"default": "bicubic"}),
                "crop_methods": (s.crop_methods, {"default": "disabled"}),
                "img_size": (
                    "INT",
                    {"default": 1024, "min": 1, "max": 8192, "step": 1},
                ),
                "GCD": ("INT", {"default": 64, "min": 1, "max": 512, "step": 1}),
            },
            "optional": {
                "width": (
                    "INT",
                    {"min": 1, "max": 8192, "step": 1, "defaultInput": True},
                ),
                "height": (
                    "INT",
                    {"min": 1, "max": 8192, "step": 1, "defaultInput": True},
                ),
            },
        }

    RETURN_TYPES = (
        "IMAGE",
        "INT",
        "INT",
        "INT",
        "INT",
    )
    RETURN_NAMES = (
        "image",
        "width",
        "height",
        "count",
        "channels",
    )
    FUNCTION = "resize"
    CATEGORY = "comfyui_reimgsize"

    def resize(
        self,
        image,
        img_size,
        upscale_method,
        crop_methods,
        GCD,
        width=None,
        height=None,
    ):
        target_pixels = img_size**2
        channels = image.shape[3]
        original_width = image.shape[2]
        original_height = image.shape[1]
        count = image.shape[0]

        aspect_ratio = original_width / original_height

        if width is not None or height is not None:
            if width is not None and height is not None:
                new_width = width
                new_height = height
            elif width is not None:
                new_width = width
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = height
                new_width = int(new_height * aspect_ratio)
        else:
            new_height = int((target_pixels / aspect_ratio) ** 0.5)
            new_width = int(new_height * aspect_ratio)

        new_width = round(new_width / GCD) * GCD
        new_height = round(new_height / GCD) * GCD

        image = image.movedim(-1, 1)
        new_image = comfy.utils.common_upscale(
            image, new_width, new_height, upscale_method, crop_methods
        )
        new_image = new_image.movedim(1, -1)

        return (
            new_image,
            new_width,
            new_height,
            count,
            channels,
        )


class Cropimg:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]
    crop_methods = ["disabled", "center"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "upscale_method": (s.upscale_methods, {"default": "bicubic"}),
                "crop_methods": (s.crop_methods, {"default": "center"}),
                "width_ratio": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.001, "max": 64.0, "step": 0.001},
                ),
                "height_ratio": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.001, "max": 64.0, "step": 0.001},
                ),
            },
        }

    RETURN_TYPES = (
        "IMAGE",
        "INT",
        "INT",
        "INT",
        "INT",
    )
    RETURN_NAMES = (
        "image",
        "width",
        "height",
        "count",
        "channels",
    )
    FUNCTION = "crop"
    CATEGORY = "comfyui_reimgsize"

    def crop(self, image, upscale_method, crop_methods, width_ratio, height_ratio):
        channels = image.shape[3]
        original_width = image.shape[2]
        original_height = image.shape[1]
        count = image.shape[0]

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

        samples = image.movedim(-1, 1)
        s = comfy.utils.common_upscale(
            samples, new_width, new_height, upscale_method, crop_methods
        )
        s = s.movedim(1, -1)

        return (
            s,
            new_width,
            new_height,
            count,
            channels,
        )


class Resizebyratio:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "size": (
                    "INT",
                    {"default": 1024, "min": 32, "max": 8192, "step": 1},
                ),
                "width_ratio": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.001, "max": 64.0, "step": 0.001},
                ),
                "height_ratio": (
                    "FLOAT",
                    {"default": 1.0, "min": 0.001, "max": 64.0, "step": 0.001},
                ),
                "GCD": ("INT", {"default": 64, "min": 1, "max": 512, "step": 1}),
            },
        }

    RETURN_TYPES = (
        "INT",
        "INT",
    )
    RETURN_NAMES = (
        "width",
        "height",
    )
    FUNCTION = "resizebyratio"
    CATEGORY = "comfyui_reimgsize"

    def resizebyratio(self, size, width_ratio, height_ratio, GCD):
        target = size**2
        ratio = width_ratio / height_ratio
        height = (target / ratio) ** 0.5
        width = ratio * height
        height = round(height / GCD) * GCD
        width = round(width / GCD) * GCD

        return (
            width,
            height,
        )


NODE_CLASS_MAPPINGS = {
    "Reimgsize": Reimgsize,
    "Cropimg": Cropimg,
    "Resizebyratio": Resizebyratio,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Reimgsize": "Reimgsize",
    "Cropimg": "Cropimg",
    "Resizebyratio": "Resizebyratio",
}
