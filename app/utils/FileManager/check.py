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

# 类型与扩展名映射表
EXTENSION_MAP = {
        'img': {'bmp', 'png', 'jpg', 'jpeg', 'webp'},
        'doc': {'doc', 'docx', 'pdf', 'txt', 'md'},
        'audio': {'mp3', 'wav', 'ogg', 'flac'},
        'video': {'mp4', 'mov', 'avi', 'mkv'}
    }
def check_file(file_path: Path, file_type: str) -> bool:
    """验证文件存在性及类型匹配
    Args:
        file_path: Path 对象
        file_type: 文件类型标识符（支持img/doc/audio/video）
    Returns:
        bool: 同时满足存在性和类型匹配时返回True
    """

    # 类型有效性检查
    if file_type not in EXTENSION_MAP:
        print(f"Unsupported file type: {file_type}")
        return False

    # 存在性检查（包含文件类型验证）
    if not (check_path(file_path) and file_path.is_file()):
        return False

    # 提取并标准化扩展名
    file_ext = file_path.suffix.lstrip('.').lower()

    # 类型匹配检查
    return file_ext in EXTENSION_MAP[file_type]

