# 程序主入口
from bin.file_manager import fm
from test_run_deepmini import run_deepmini


if __name__ == "__main__":
    fix_class = {"explicit":"nsfw_anime", "questionable":"sexy_anime", "safe":"sfw_anime"}
    for content in run_deepmini():

        img_path = content["img_path"]
        img_safety_weight = content["img_tags"][-1][1]
        img_safety = content["img_tags"][-1][0].split(":")[-1]
        if img_safety == "safe":
            fm.move_file(img_path, fix_class["safe"])
        elif img_safety == "questionable":
            if img_safety_weight <= 0.82:
                fm.move_file(img_path, fix_class["questionable"])
            else:
                fm.move_file(img_path, fix_class["explicit"])
        else:
            continue
