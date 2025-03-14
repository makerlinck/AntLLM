import asyncio
import os
from pathlib import Path
from typing import Literal, AsyncIterable

from .data_loader import get_model_path, get_tags, MAX_TASKS, THRESHOLD, ALLOW_GPU
from .vision_pipeline import evaluate_image
from .schemas import TagItem, SUPPORTED_LANGUAGES

# 全局进程池
global_pool = None


def init_process(model_path, zero_tags):
    global shared_model, shared_zero_tags
    import tensorflow as tf
    shared_model = tf.keras.models.load_model(model_path, compile=False)
    shared_zero_tags = zero_tags


from concurrent.futures import ProcessPoolExecutor
def init_pool():
    model_path = get_model_path()
    zero_tags = get_tags("zero")
    global global_pool
    global_pool = ProcessPoolExecutor(
        max_workers=MAX_TASKS,
        initializer=init_process,
        initargs=(model_path, zero_tags)
    )


def shutdown_pool():
    """ 关闭进程池 """
    global global_pool
    if global_pool:
        global_pool.shutdown(wait=True)
        global_pool = None


def process_image(params):
    """ 接收图片路径和语言参数 """
    idx, image_path, tag_language = params
    lang_tags = get_tags(tag_language)  # 动态获取标签
    img_tags = []
    for tag, score in evaluate_image(
            image_path,
            model=shared_model,
            lang_tags=lang_tags,
            zero_tags=shared_zero_tags,
            threshold=THRESHOLD
    ):
        img_tags.append(tag)
    return idx, image_path, img_tags


async def evaluate(
    imgs_seq: list[tuple[int, Path]],
    tag_language: Literal[*SUPPORTED_LANGUAGES],
    is_return_uri_as_path: bool = False
) -> AsyncIterable[TagItem]:
    if not ALLOW_GPU:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    params = [(idx, path, tag_language) for idx, path in imgs_seq]
    loop = asyncio.get_event_loop()
    # 使用全局进程池提交任务（确保已初始化）
    tasks = [
        loop.run_in_executor(
            global_pool,  # 使用全局进程池
            process_image,
            p
        )
        for p in params
    ]

    for future in asyncio.as_completed(tasks):
        try:
            res = await future
            if res is None:
                continue
            idx, path, img_tags = res
            path = str(path) if not is_return_uri_as_path else path
            yield TagItem(
                img_seq=(idx, path),
                img_tags=img_tags,
            )
        except Exception as e:
            print(f"Error processing image: {e}")
            continue

def run_test_evaluation():
    from .data_loader import PACKAGE_PATH
    from datetime import datetime
    print("Input test or dir of image to run test_demo")
    while input_ := input("Press Enter to quit: "):
        path = PACKAGE_PATH.joinpath("test/test.jpg") if input_ == "test" else Path(input_)
        print(path)
        if not (path.exists() and path.suffix in [".jpg", ".png", ".webp"]):
            print(f"Invalid path of {path}")
            continue
        print(datetime.now())
        return evaluate(
            [path.as_posix()],
            tag_language="zh-cn",
            is_return_path=True,
            verbose=True
        )
