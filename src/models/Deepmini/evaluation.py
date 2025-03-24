import asyncio
import os
from pathlib import Path
from typing import Literal, AsyncIterable

from .data_loader import (
    get_model_path,        # 获取模型路径的函数
    get_tags,              # 根据语言获取标签的函数
    MAX_TASKS,             # 最大并发任务数
    THRESHOLD,             # 标签置信度阈值
    ALLOW_GPU              # 是否启用GPU标志
)

from .vision_pipeline import evaluate_image     # 图像评估核心函数
from .schemas import TagItem, SUPPORTED_LANGUAGES

# 全局进程池
global_pool = None
global shared_model, shared_zero_tags

def init_process(model_path, zero_tags):
    """初始化每个进程的共享资源
    Args:
        model_path (str): 模型文件路径
        zero_tags (dict): 基础标签字典（零样本标签）
    """
    global shared_model, shared_zero_tags
    import tensorflow as tf
    shared_model = tf.keras.models.load_model(model_path, compile=False)
    shared_zero_tags = zero_tags


from concurrent.futures import ProcessPoolExecutor
def init_pool():
    """初始化全局进程池并预加载模型资源"""
    model_path = get_model_path()
    zero_tags = get_tags("zero")
    global global_pool
    global_pool = ProcessPoolExecutor(
        max_workers=MAX_TASKS,
        initializer=init_process,
        initargs=(model_path, zero_tags)
    )


def shutdown_pool():
    """关闭进程池"""
    global global_pool
    if global_pool:
        global_pool.shutdown(wait=False)
        global_pool = None


def process_image(params):
    """单张图像处理函数（进程池工作单元）
    Args: params (tuple): (索引, 图像路径, 标签语言)
    Returns: tuple: (索引, 路径, 标签列表)
    """

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
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # 确保在进程启动前设置

    params = [(idx, path, tag_language) for idx, path in imgs_seq]
    loop = asyncio.get_event_loop()
    tasks = [
        loop.run_in_executor(global_pool, process_image, p)
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