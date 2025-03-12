import os,tensorflow as tf
global shared_model, shared_lang_tags, shared_zero_tags
def init_process(model_path_str, tag_lang):
    global shared_model, shared_lang_tags, shared_zero_tags
    model_path = Path(model_path_str)
    shared_model = tf.keras.models.load_model(model_path, compile=False)
    shared_lang_tags = load_tags(tag_lang)
    shared_zero_tags = load_tags("zero")

# 任务处理函数
from .vision_pipeline import evaluate_image
def process_image(image_path_str):
    image_path = Path(image_path_str)

    if checker.check_file(image_path, "image"): # 跳过无效文件
        img_tags = []
        for tag, score in evaluate_image(
            image_path,
            shared_model,
            lang_tags=shared_lang_tags,
            zero_tags=shared_zero_tags,
            threshold=THRESHOLD
        ):
            img_tags.append(tag)
        return image_path, img_tags


from typing import Generator
from .data_loader import load_tags, ALLOW_GPU, MAX_TASK_COUNT
from src.schemas.tagger import SUPPORTED_TAG_LANG
import multiprocessing as mp
from pathlib import Path
from src.models.Deepmini.data_loader import load_model_from_project, THRESHOLD
from src.schemas.tagger import TagItem
from src.utils.FileManager import checker
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
        processes=MAX_TASK_COUNT,
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
