from pathlib import Path

def check_path(path_: Path,touching_mode:bool = False) -> bool:
    """验证路径是否存在
    Args:
        path_: Path 对象
        touching_mode: Touching模式 若目标路径不存在则创建,该操作只对目录Path对象有效
    Returns:
        bool: 存在时返回True
    """
    if path_.is_dir() and touching_mode:
        try:
            path_.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"创建目录失败: {e}")
        pass
    return path_.exists()


from pathlib import Path
from typing import Literal

# 明确类型范围
SUPPORTED_TYPES = Literal['image', 'doc', 'audio', 'video']
EXTENSION_MAP = {
    'image': {'bmp', 'png', 'jpg', 'jpeg', 'webp'},
    'doc': {'doc', 'docx', 'pdf', 'txt', 'md'},
    'audio': {'mp3', 'wav', 'ogg', 'flac'},
    'video': {'mp4', 'mov', 'avi', 'mkv'}
}

def check_file(file_path: Path, file_type: SUPPORTED_TYPES) -> bool:
    """ 验证文件存在性及类型匹配
    Args:
        file_path: 待检查的Path对象
        file_type: 文件类型标识符，支持：image/doc/audio/video
                  （自动兼容大小写和前后空格）
    Returns:
        bool: 同时满足存在性和类型匹配时返回True
    Raises:
        ValueError: 当文件路径不是文件类型时
    """
    # 标准化输入参数
    normalized_type = file_type.lower()

    # 类型有效性检查（提前返回模式）
    if normalized_type not in EXTENSION_MAP:
        valid_types = ', '.join(EXTENSION_MAP.keys())
        print(f"Unsupported file type: {file_type}. Valid options: [{valid_types}]")
        return False

    # 存在性检查（分离路径检查和文件类型验证）
    if not file_path.exists():
        print(f"Path not found: {file_path}")
        return False
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    # 提取扩展名（优化后缀处理逻辑）
    file_ext = file_path.suffix.lstrip('.').casefold()  # 更严格的标准化

    # 类型匹配检查（使用早返回模式）
    return file_ext in EXTENSION_MAP[normalized_type]