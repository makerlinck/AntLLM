import multiprocessing as mp
import os
from pathlib import Path
from typing import Generator

from src.utils.FileManager import check
from src.schemas.tagger import TagItem, SUPPORTED_TAG_LANG
from .data_loader import load_tags, load_model_from_project, ALLOW_GPU, THRESHOLD
from .vision_pipeline import evaluate_image
is_return_path = False

# 新增：进程初始化函数
def init_process(model_path_str, tag_lang):
    import tensorflow as tf

    global shared_model, shared_lang_tags, shared_zero_tags
    model_path = Path(model_path_str)
    shared_model = tf.keras.models.load_model(model_path, compile=False)
    shared_lang_tags = load_tags(tag_lang)
    shared_zero_tags = load_tags("zero")

# 新增：任务处理函数
def process_image(image_path_str):
    image_path = Path(image_path_str)
    if not check.check_file(image_path, "image"):
        return None  # 跳过无效文件
    img_tags = []
    for tag, score in evaluate_image(
        image_path,
        shared_model,
        lang_tags=shared_lang_tags,
        zero_tags=shared_zero_tags,
        threshold=THRESHOLD
    ):
        img_tags.append(tag)
    image_path = str(image_path) if not is_return_path else image_path
    return TagItem(img_path=image_path, img_tags=img_tags)
def evaluate(
    image_paths: list[str],
    tag_language: SUPPORTED_TAG_LANG = "en",
    is_return_path: bool = False,
    verbose: bool = False
) -> Generator[TagItem, None, None]:
    if not ALLOW_GPU:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    model_path = load_model_from_project()
    if not model_path.exists():
        raise Exception("h5 Model file not found. Please Check!")

    # 创建进程池并并行处理
    with mp.Pool(
        processes=2,
        initializer=init_process,
        initargs=(str(model_path), tag_language)
    ) as pool:
        results = pool.map(process_image, image_paths)

    # 处理结果并生成TagItem
    for res in results:
        if res is None:
            continue
        img_path, img_tags = res
        if not is_return_path:
            img_path = str(img_path)
        if verbose:
            print(f"Tags of {img_path}:")
        yield TagItem(img_path=img_path, img_tags=img_tags)
