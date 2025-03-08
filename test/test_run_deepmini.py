from app.file_manager import fm
from app.image_viewer import get_evaluation

def run_deepmini():
    imgs = []
    for img_path in fm.get_origin_files(recursive=True):
        print(f"{img_path}")
        imgs.append(img_path)
    return get_evaluation(imgs)

if __name__ == "__main__":
    for a in run_deepmini():
        print(a["img_path"],a["img_tags"])