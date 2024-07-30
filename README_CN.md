# comfyui_reimgsize
a simple reimgsize node(s) in comfyui | 一个简单的comfyui重载图像大小节点

## 简介
一个简单的ComfyUI节点，用于将图像按比例调整到给定像素量大小，并将分辨率标准化至符合给定的GCD的倍数。

## 作用
- 将图像总分辨率调整到指定分辨率^2
- 保持原有宽高比/调整至给定宽高比
- 确保分辨率是GCD（通常是32或64）的倍数

## 例子
![image](./workflow/workflow.png)

## 安装
到ComfyUI文件夹目录下的 `custom_nodes` 后执行以下命令：
```
git clone https://github.com/MakkiShizu/comfyui_reimgsize.git
```
使用时节点位置：
- image/Image_Size_Normalization
- image/Crop_Image_Ratio

#### 许可证
该项目使用MIT许可证。
<hr>