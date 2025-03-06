import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Generator

import yaml as yml
class FileManager:

    def __init__(self):
        self.work_dir = os.path.dirname(os.getcwd())    # 获取主程序工作目录
        self.origin_dir = self.touch_dir("origin")
        self.origin_dir_path = Path(self.origin_dir)
        self.output_dir = self.touch_dir("output")

        print("初始化工作目录为:", self.work_dir)

    def touch_dir(self, fold_name):
        """
        获取/创建指定目录
        :param fold_name: 目标文件夹名称
        :return: 完整目录路径
        """
        target_dir = os.path.join(self.work_dir, fold_name)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)  # 自动创建多级目录
            print(f"已创建目录: {target_dir}")
        else:
            print(f"目录已存在: {target_dir}")

        return target_dir
    def get_origin_files(self, recursive: bool) -> Generator[str, None, None]:
        """
        生成器函数，递归查找指定目录下的所有文件
        :param recursive:是否递归查询该目录
        """
        pattern = "**/*.[pPjJwWgGbBtT][nNpPeEgGaAfF][gGpPeEfFmM]*" if recursive else "*.[pPjJwWgGbBtT][nNpPeEgGaAfF][gGpPeEfFmM]*"
        for path in self.origin_dir_path.glob(pattern):
            if path.is_file() and not path.name.startswith(('~$', '.')):
                yield path.resolve().as_posix()


    def move_file(self,src_path: Path, dest_dir_name: str) -> str:
        """移动文件到指定output下的路径,需提供源文件路径和目标目录名"""
        dest_path = os.path.join(self.output_dir, dest_dir_name, src_path.name)

        # 确保目标目录存在
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # 自动重命名逻辑（当目标文件已存在时）
        base_name, ext = os.path.splitext(os.path.basename(dest_path))
        counter = 1
        while os.path.exists(dest_path):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_name = f"{base_name}_{timestamp}{ext}"
            dest_path = os.path.join(dest_dir, new_name)
            counter += 1

        # 执行移动操作
        shutil.move(src_path, dest_path)
        print("文件移动成功。目标路径：" + dest_path)
        return dest_path
