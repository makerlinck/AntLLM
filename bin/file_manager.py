import shutil
from pathlib import Path
from typing import Generator

import yaml as yml

class FileManager:

    def __init__(self):
        self.work_dir = Path(__file__).resolve().parent.parent
        self.user_dir = Path.home()
        self.origin_dir = self.touch_dir("origin")
        self.output_dir = self.touch_dir("output")

        print(f"初始化工作目录为:{self.work_dir}")

    def touch_dir(self, fold_name:str):
        """
        获取/创建指定目录
        :param fold_name: 目标文件夹名称
        :return: 完整目录路径
        """
        target_dir = self.work_dir / fold_name
        if not target_dir.exists():
            print(f"DEBUG:源目录为:{target_dir}")
            target_dir.mkdir(parents=True)
        return target_dir
    def get_origin_files(self, recursive: bool) -> Generator[str, None, None]:
        """
        生成器函数，递归查找指定目录下的所有文件
        :param recursive:是否递归查询该目录
        """
        pattern = "**/*.[pPjJwWgGbBtT][nNpPeEgGaAfF][gGpPeEfFmM]*" if recursive else "*.[pPjJwWgGbBtT][nNpPeEgGaAfF][gGpPeEfFmM]*"
        for path in self.origin_dir.glob(pattern):
            if path.is_file() and not path.name.startswith(('~$', '.')):
                yield path.resolve().as_posix()


    def move_file(self,src_path: Path, dest_dir: str) -> bool:
        """移动文件到指定output下的路径,需提供源文件路径和目标目录名"""
        dest_dir_path = self.output_dir / dest_dir

        # 确保目标目录存在
        if not dest_dir_path.exists():
            dest_dir_path.mkdir(parents=True)
            print(f"目标目录不存在，已创建:{dest_dir_path}")

        # 执行移动操作
        shutil.move(src_path, dest_dir)
        print("文件移动成功。目标路径：" + str(dest_dir_path))
        return True

fm = FileManager()