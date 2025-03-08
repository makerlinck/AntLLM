import os, six, math, skimage.transform
from pathlib import Path
from typing import Any, Iterable, List, Tuple, Union
import tensorflow as tf, tensorflow_io as tfio
def load_tags(tags_path):
    with open(tags_path, "r") as tags_stream:
        tags = [tag for tag in (tag.strip() for tag in tags_stream) if tag]
        return tags
def load_tags_from_project(project_path):
    tags_path = os.path.join(project_path, "tags.txt")

    return load_tags(tags_path)
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
    """
    Transform image and pad by edge pixels.
    """
    image_width = image.shape[1]
    image_height = image.shape[0]
    image_array = image

    t = skimage.transform.AffineTransform(
        translation=(-image_width * 0.5, -image_height * 0.5)
    )

    if scale:
        t += skimage.transform.AffineTransform(scale=(scale, scale))

    if rotation:
        radian = (rotation / 180.0) * math.pi
        t += skimage.transform.AffineTransform(rotation=radian)

    t += skimage.transform.AffineTransform(
        translation=(target_width * 0.5, target_height * 0.5)
    )

    if shift:
        t += skimage.transform.AffineTransform(
            translation=(target_width * shift[0], target_height * shift[1])
        )

    warp_shape = (target_height, target_width)

    image_array = skimage.transform.warp(
        image_array, (t).inverse, output_shape=warp_shape, order=order, mode=mode
    )

    return image_array

def load_image_for_evaluate(
    input_: Union[str, six.BytesIO], width: int, height: int, normalize: bool = True
) -> Any:
    if isinstance(input_, six.BytesIO):
        image_raw = input_.getvalue()
    else:
        image_raw = tf.io.read_file(input_)
    try:
        image = tf.io.decode_png(image_raw, channels=3)
    except:
        image = tfio.image.decode_webp(image_raw)
        image = tfio.experimental.color.rgba_to_rgb(image)

    image = tf.image.resize(
        image,
        size=(height, width),
        method=tf.image.ResizeMethod.AREA,
        preserve_aspect_ratio=True,
    )
    image = image.numpy()  # EagerTensor to np.array
    image = transform_and_pad_image(image, width, height)

    if normalize:
        image = image / 255.0

    return image

def evaluate_image(
    image_input: Union[str, six.BytesIO], model: Any, tags: List[str], threshold: float
) -> Iterable[Tuple[str, float]]:
    width = model.input_shape[2]
    height = model.input_shape[1]
    image = load_image_for_evaluate(image_input, width=width, height=height)
    image_shape = image.shape
    image = image.reshape((1, image_shape[0], image_shape[1], image_shape[2]))
    y = model.predict(image)[0]
    result_dict = {}

    for i, tag in enumerate(tags):
        result_dict[tag] = y[i]

    for tag in tags:
        if result_dict[tag] >= threshold:
            yield tag, result_dict[tag]
def evaluate(
    target_image_paths:list[Path], #this
    project_path:Path,
    threshold:float = 6.18,
    allow_gpu:bool = True,
):
    if not allow_gpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    model_path = os.path.join(project_path, "model-resnet_custom_v4.h5")
    model = tf.keras.models.load_model(model_path, compile=False)

    tags = load_tags_from_project(project_path)
    img_tags = {str:list}
    for image_path in target_image_paths:
        print(f"Tags of {image_path}:") #yup!
        tag_list = [list[str, float]]
        for tag, score in evaluate_image(image_path, model, tags, threshold):
            print(f"tag:{tag} score:({score:05.3f})")
            tag_list.append([str(tag),float(score)])
        img_tags.update({image_path:tag_list})
    return img_tags