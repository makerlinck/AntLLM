import os
from typing import Generator
from pathlib import Path
file_dir = Path("D:/Project/PycharmProject/AntOllama/origin")
def find_files(directory: Path, recursive: bool) -> Generator[Path, None, None]:
    """生成器函数，递归查找指定目录下的所有文件"""
    pattern = "**/*.*" if recursive else "*.*"
    for path in directory.glob(pattern):
        if path.is_file() and not path.name.startswith(('~$', '.')):
            yield path

print(list(find_files(file_dir,True))[0])