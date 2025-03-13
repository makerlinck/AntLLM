import os, multiprocessing as mp
from pathlib import Path
from typing import Literal, Generator
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


def init_pool():
    """ 应用启动时初始化进程池 """
    global global_pool
    model_path = get_model_path()
    zero_tags = get_tags("zero")
    global_pool = mp.Pool(
        processes=MAX_TASKS,
        initializer=init_process,
        initargs=(model_path, zero_tags)
    )


def shutdown_pool():
    """ 关闭进程池 """
    global global_pool
    if global_pool:
        global_pool.close()  # 禁止新任务
        global_pool.join()  # 等待现有任务完成
        global_pool = None


def process_image(params):
    """ 接收图片路径和语言参数 """
    image_path_str, tag_language = params
    image_path = Path(image_path_str)
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
    return image_path, img_tags


def evaluate(
        image_paths: list[str],
        tag_language: Literal[*SUPPORTED_LANGUAGES],
        is_return_path: bool = False,
        verbose: bool = False
) -> Generator[TagItem, None, None]:
    if not ALLOW_GPU:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    # 使用全局进程池处理任务
    params = [(path, tag_language) for path in image_paths]
    results = global_pool.map(process_image, params)  # 非阻塞式调用

    for res in results:
        if res is None:
            continue
        img_path, img_tags = res
        if not is_return_path:
            img_path = str(img_path)
        if verbose:
            print(f"Tags of {img_path}:")
        yield TagItem(img_path=img_path, img_tags=img_tags)


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
