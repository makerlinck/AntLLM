import os, six, math, skimage.transform
from gettext import find
from pathlib import Path
from typing import Any, Iterable, List, Tuple, Union, Generator
import tensorflow as tf, tensorflow_io as tfio
from .data_loader import load_tags, load_model_from_project, ALLOW_GPU, THRESHOLD
from app.schemas.tagger import TagItem


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
        image_array, t.inverse, output_shape=warp_shape, order=order, mode=mode
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
        # if not 5889 <= i <= 7718:
        #     print(f"{i}:{tag}")
        result_dict[tag] = (i,y[i])

    key_active ,ratings = [], []
    keys_with_weight = "cum nude anus pussy censored mosaic_censoring ejaculation fellatio imminent_rape imminent_sex imminent_vaginal nipples breasts clitoris urethra uncensored naked no_panties".split(" ")
    keys_ban = "nude anus pussy ejaculation penis naked".split(" ")
    # 过滤置信度低的 Tag; 过滤所有 Charactor-Tags; 保留最后一个分级Tag
    for tag in tags:
        if not (5888 < result_dict[tag][0] < len(tags)) and result_dict[tag][1] >= threshold:
            for key in keys_with_weight:
                if key in tag:
                    key_active.append(tag)
            yield tag, result_dict[tag][1]
        elif result_dict[tag][0] >= len(tags)-3:
            ratings.append((tag, result_dict[tag][1]))

    if ratings[0][1] > ratings[1][1] + ratings[2][1]:
        yield "safe", ratings[0][1]
    else:
        ps = False
        for tag in keys_ban:
            if tag in key_active:
                if result_dict[tag][1] > 0.81:
                    ps = True
        if (ratings[2][1]-ratings[1][1]-ratings[0][1])*(ratings[2][1]-ratings[1][1]-ratings[0][1]) < 0.09:
            if len(key_active) > 1 or ps:
                yield "nsfw", ratings[2][1]
            else:
                yield "sus", ratings[1][1]
        else:
            if ratings[1][1] > ratings[2][1] and not ps:
                yield "sus", ratings[1][1]
            else:
                yield "nsfw", ratings[2][1]



def evaluate(
    image_paths:list[Path | str], #this
    is_return_path:bool = False,
    verbose:bool = False
) -> Generator[TagItem, None, None]:
    if not ALLOW_GPU:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    if not load_model_from_project().exists():
        raise Exception("h5 Model file not found. Please Check!")
    model = tf.keras.models.load_model(load_model_from_project(), compile=False)

    tags = load_tags()
    for image_path in image_paths:
        if type(image_path) == str:
            # 兼容字符串路径
            image_path = Path(image_path)

        if image_path.exists():
            if verbose:print(f"Tags of {image_path}:")
            img_tags = []
            for tag, score in evaluate_image(image_path.as_posix(), model, tags, THRESHOLD):
                if verbose:print(f"tag:{tag} score:({score:05.3f})")
                img_tags.append((str(tag), round(float(score),4)))
            if not is_return_path:
                image_path = str(image_path.as_posix())
            yield TagItem(img_path=image_path, img_tags=img_tags)

