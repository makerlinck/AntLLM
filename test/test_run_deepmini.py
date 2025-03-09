from app.models import vision_pipeline
from app.utils import fm

def run_deepmini():
    imgs = []
    for img_path in fm.get_origin_files(recursive=True):
        print(f"\"{img_path}\",")
        imgs.append(img_path)
    return vision_pipeline.evaluate(imgs,verbose=True)

if __name__ == "__main__":
    for i in run_deepmini():
        pass