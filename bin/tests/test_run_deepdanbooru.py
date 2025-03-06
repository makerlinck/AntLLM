import os
import warnings

from bin.utils.executor.file_manager import FileManager
from deepdanbooru.commands import evaluate
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
fm = FileManager()
work_dir = fm.work_dir

if __name__ == "__main__":
    print(work_dir)
    response = evaluate(
        target_image_paths=["D:/Project/PycharmProject/AntOllama/origin/7653224863265797761.PNG"],
        project_path="D:\Project\PycharmProject\AntOllama\deepdanbooru_v4e30",
        threshold=0.618,
        allow_gpu=True,
        compile_model=False,
        verbose=False,
    )
    print(f"\033[32m {response} \033[0m")

