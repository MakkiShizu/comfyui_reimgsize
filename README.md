# comfyui_reimgsize

simple image resize node(s) in comfyui | 简单的comfyui节点用于重载图像大小

[[简体中文](README_CN.md)|English]

## Description

Some simple ComfyUI nodes are used to scale an image to a specified **sum of pixels** and standardize the resolution to a multiple of the given GCD.

This repository is not specific to the length and width values of an image, but focuses more on adjusting the **total pixel count**, **side length specifications**, and **size ratios** of the image.

## Features

- Resize images to a specified resolution
- Maintain the original aspect ratio/Adjust to the given aspect ratio
- Ensure dimensions are multiples of GCD(most cases 32 or 64)

## Example

![image](./example_workflows/comfyui_reimgsize.png)

## Installation

Clone the repository to `custom_nodes`:

```
git clone https://github.com/MakkiShizu/comfyui_reimgsize.git
```

nodes path：

- image/Reimgsize
- image/Cropimg
- utils/Resizebyratio

#### License

This project is licensed under the MIT License.

<hr>
