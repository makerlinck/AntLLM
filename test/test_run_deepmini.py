from app.utils import fm
from app.models.deepmini.image_viewer import aget_evaluation

def run_deepmini():
    imgs = []
    for img_path in fm.get_origin_files(recursive=True):
        print(f"\"{img_path}\",")
        imgs.append(img_path)
    return aget_evaluation(imgs)

if __name__ == "__main__":
    for a in run_deepmini():
        print(a["img_path"],a["img_tags"])