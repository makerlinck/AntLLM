import math, skimage.transform
def transform_and_pad_image(
    image,
    target_width,
    target_height,
    scale=None,
    rotation=None,
    shift=None,
    order=1,
    mode="edge",
):
    """ 应用仿射变换处理图像，并通过边缘像素扩展填充至目标尺寸 """
    image_height, image_width = image.shape[:2]  # 直接获取形状

    # 构建变换步骤
    tf_steps = [
        skimage.transform.AffineTransform(translation=(-image_width * 0.5, -image_height * 0.5))
    ]
    if scale:
        tf_steps.append(skimage.transform.AffineTransform(scale=(scale, scale)))
    if rotation:
        tf_steps.append(skimage.transform.AffineTransform(rotation=rotation * math.pi / 180))
    tf_steps.append(
        skimage.transform.AffineTransform(translation=(target_width * 0.5, target_height * 0.5)))  # 必须的中心对齐
    if shift:
        tf_steps.append(
            skimage.transform.AffineTransform(translation=(target_width * shift[0], target_height * shift[1])))

    # 合并所有变换
    t = tf_steps[0]
    for tr in tf_steps[1:]:
        t += tr

    image = skimage.transform.warp(
        image,
        t.inverse,
        output_shape=(target_height, target_width),
        order=order,
        mode=mode
    )
    return image