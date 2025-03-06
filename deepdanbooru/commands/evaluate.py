import os
from typing import Any, Iterable, List, Tuple, Union

import six
import tensorflow as tf

import deepdanbooru as dd

def save_txt_file(txt_path, list):
    last_index = len(list)-1
    last_tag = list[last_index]
    with open(txt_path, 'w') as writer:
        for i in list:
            if last_tag == i:
                writer.write(i)
                writer.close()
            else:
                writer.write(i + ", ")
    print("Saved text file.")

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
    compile_model,
    verbose,
):
    model_path = os.path.join(project_path, "model-resnet_custom_v4.h5")
    tags_path = os.path.join(project_path, "tags.txt")

    if not allow_gpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    target_image_paths = dd.extra.natural_sorted(target_image_paths)

    if model_path:
        if verbose:
            print(f"Loading model from {model_path} ...")
        model = tf.keras.models.load_model(model_path, compile=compile_model)
    else:
        if verbose:
            print(f"Loading model from project {project_path} ...")
        model = dd.project.load_model_from_project(
            project_path, compile_model=compile_model
        )

    if tags_path:
        if verbose:
            print(f"Loading tags from {tags_path} ...")
        tags = dd.data.load_tags(tags_path)
    else:
        if verbose:
            print(f"Loading tags from project {project_path} ...")
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