import os.path

from bin.utils.executor.file_manager import FileManager
from deepdanbooru.project import evaluate

alice = FileManager()
work_dir = alice.work_dir
print(os.path.join(work_dir,"deepdanbooru_v4e30"))
def get_evaluation(target_paths:list[str]):
    return evaluate(
        target_image_paths=target_paths,
        project_path=os.path.join(work_dir,"data/deepdanbooru_v4e30"),
        threshold=0.62,
        allow_gpu=False,
    )