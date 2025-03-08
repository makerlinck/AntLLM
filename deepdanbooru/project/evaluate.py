import os, six
from typing import Any, Iterable, List, Tuple, Union
import tensorflow as tf
import deepdanbooru as dd
def evaluate_image(
    image_input: Union[str, six.BytesIO], model: Any, tags: List[str], threshold: float
) -> Iterable[Tuple[str, float]]:
    width = model.input_shape[2]
    height = model.input_shape[1]
    image = dd.data.load_image_for_evaluate(image_input, width=width, height=height)
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
    target_image_paths, #this
    project_path,
    threshold,
    allow_gpu,
):
    if not allow_gpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    target_image_paths = dd.extra.natural_sorted(target_image_paths)
    model_path = os.path.join(project_path, "model-resnet_custom_v4.h5")
    model = tf.keras.models.load_model(model_path, compile=False)

    tags = dd.project.load_tags_from_project(project_path)
    img_tags = {str:list}
    for image_path in target_image_paths:
        print(f"Tags of {image_path}:") #yup!
        tag_list = [list[str, float]]
        for tag, score in evaluate_image(image_path, model, tags, threshold):
            print(f"({score:05.3f}) {tag}")
            tag_list.append([str(tag),float(score)])
        img_tags.update({image_path:tag_list})
    return img_tags