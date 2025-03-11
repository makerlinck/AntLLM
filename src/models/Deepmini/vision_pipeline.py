import os,tensorflow as tf, tensorflow_io as tfio
from pathlib import Path
from typing import Any, Iterable, Generator
from .data_loader import load_tags, load_model_from_project, ALLOW_GPU, THRESHOLD
from src.schemas.tagger import TagItem, SUPPORTED_TAG_LANG
from .transform import transform_and_pad_image

def evaluate_image(
    image_input: Path, model: Any, lang_tags: list[str], zero_tags: list[str], threshold: float,normalize:bool = True
) -> Iterable[tuple[str, float]]:

    image_raw = tf.io.read_file(image_input.as_posix())
    try:
        image = tf.io.decode_png(image_raw, channels=3)
    except:
        print("Failed decode image as png,trying decode as webp")
        image = tfio.image.decode_webp(image_raw)
        image = tfio.experimental.color.rgba_to_rgb(image)

    width, height = model.input_shape[2], model.input_shape[1]
    image = tf.image.resize(
        image,
        size=(height, width),
        method=tf.image.ResizeMethod.AREA,
        preserve_aspect_ratio=True,
    )
    image = image.numpy()  # EagerTensor to np.array
    image = transform_and_pad_image(image, width, height)

    if normalize:image = image / 255.0

    img_shape = image.shape
    image = image.reshape((1, img_shape[0], img_shape[1], img_shape[2]))
    predict_result = model.predict(image)[0]
    result_dict = {}


    # 过滤置信度低的 Tag; 过滤所有 Charactor-Tags; 保留最后一个分级Tag
    CENSORED_KEYS = "nude anus pussy ejaculation penis nipples naked fellatio urethra".split(" ")
    len_tags, tags_activated, rating = len(lang_tags), [], []
    t_safe, t_sus, t_nsfw = lang_tags[-3], lang_tags[-2], lang_tags[-1]

    for i,tag in enumerate(lang_tags):
        result_dict[tag] = (i, predict_result[i])
        if not (len(lang_tags) - 3 < result_dict[tag][0] < len(lang_tags)) and result_dict[tag][1] >= threshold:
            tags_activated.append(zero_tags[i])
            yield tag, result_dict[tag][1]
        elif result_dict[tag][0] >= len(lang_tags)-3:
            rating.append(result_dict[tag][1])

    if any(tag in CENSORED_KEYS for tag in tags_activated):
        yield t_nsfw, result_dict[lang_tags[len_tags-1]][1]
    else:
        if max(*rating) == rating[0]:
            yield t_safe, rating[0]
        elif max(*rating) == rating[1]:
            if rating[0] > rating[2]:
                yield t_sus, rating[1]
            else:yield t_nsfw,rating[2]
        else:
            yield t_nsfw, rating[2]

from src.utils.FileManager import check
def evaluate(
    image_paths:list[Path],
    tag_language:SUPPORTED_TAG_LANG = "en",
    is_return_path:bool = False,
    verbose:bool = False
) -> Generator[TagItem, None, None]:
    if not ALLOW_GPU: os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    if not load_model_from_project().exists():
        raise Exception("h5 Model file not found. Please Check!")

    model = tf.keras.models.load_model(load_model_from_project(), compile=False)
    lang_tags = load_tags(tag_language)
    zero_tags = load_tags("zero")
    for image_path in image_paths:
        # 兼容字符串路径
        image_path = Path(image_path)
        # 检查当前图像文件是否合法,若检查未通过则跳过该图像文件后续处理
        if not check.check_file(image_path, "image"):continue
        img_tags = []
        # 收集通过阈值验证的图像标签（evaluate_image已内置阈值过滤逻辑）
        for tag, score in evaluate_image(
                image_path,
                model, zero_tags= zero_tags,
                lang_tags= lang_tags,
                threshold= THRESHOLD
        ):
            if verbose: print(f"tag:{tag} score:({score:05.3f})")
            img_tags.append(tag)
        # 统一路径格式输出（优先使用字符串类型）
        image_path = str(image_path) if not is_return_path else image_path

        if verbose: print(f"Tags of {image_path}:")
        yield TagItem(img_path=image_path, img_tags=img_tags)
