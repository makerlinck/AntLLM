import os

import tensorflow as tf
tf.config.optimizer.set_jit(True)   # 启用XLA加速
import math, skimage.transform
# 图像处理业务函数
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


from pathlib import Path
from typing import Any, Iterable


def evaluate_image(
        image_input: Path, model: Any, lang_tags: list[str], zero_tags: list[str], threshold: float,
        normalize: bool = True
) -> Iterable[tuple[str, float]]:
    try:
        image_raw = tf.io.read_file(image_input.as_posix())
        image = tf.io.decode_png(image_raw, channels=3)
    except tf.errors.InvalidArgumentError as e:
        print(f"Decode PNG failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    width, height = model.input_shape[2], model.input_shape[1]
    image = tf.image.resize(
        image,
        size=(height, width),
        method=tf.image.ResizeMethod.AREA,
        preserve_aspect_ratio=True,
    )
    image = image.numpy()  # EagerTensor to np.array
    image = transform_and_pad_image(image, width, height)

    if normalize: image = image / 255.0

    img_shape = image.shape
    image = image.reshape((1, img_shape[0], img_shape[1], img_shape[2]))
    predict_result = model.predict(image)[0]
    result_dict = {}

    # 过滤置信度低的 Tag; 过滤所有 Charactor-Tags; 保留最后一个分级Tag
    CENSORED_KEYS = "nude anus pussy ejaculation penis nipples naked fellatio urethra".split(" ")
    len_tags, tags_activated, rating = len(lang_tags), [], []
    t_safe, t_sus, t_nsfw = lang_tags[-3], lang_tags[-2], lang_tags[-1]
    for index_, tag in enumerate(lang_tags):
        result_dict[tag] = predict_result[index_]
        if 0 <= index_ < len(lang_tags) - 3 and result_dict[tag] >= threshold:
            tags_activated.append(zero_tags[index_])
            yield tag, result_dict[tag]
        elif index_ >= len(lang_tags) - 3:
            rating.append(result_dict[tag])

    try:
        if any(tag in CENSORED_KEYS for tag in tags_activated):
            yield t_nsfw, rating[2]
        else:
            if max(*rating) == rating[0]:
                yield t_safe, rating[0]
            elif max(*rating) == rating[1]:
                if rating[0] > rating[2]:
                    yield t_sus, rating[1]
                else:
                    yield t_nsfw, rating[2]
            else:
                yield t_nsfw, 0.5
    except ValueError as e:
        print(f"Error: {e}")
        max_rating_value = max(rating)
        max_index = rating.index(max_rating_value)
        RATING_TAGS = [t_safe, t_sus, t_nsfw]
        selected_tag = RATING_TAGS[max_index]
        yield selected_tag, max_rating_value


