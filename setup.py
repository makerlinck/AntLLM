from cx_Freeze import setup, Executable

# 配置参数
script_path = "src/main.py"  # 主程序入口文件路径
build_options = {
    "build_exe": {
        "packages": ["tensorflow", "fastapi", "uvicorn", "tensorflow", "pydantic"],  # 从requirements.txt提取关键依赖
        "include_files": ["data/", "src/"],  # 包含data和src目录
        "include_msvcr": True,  # 包含Microsoft运行时库
        "excludes": []  # 排除不需要的包
    }
}

# 创建可执行文件配置
executables = [
    Executable(
        script=script_path,
        base=None,  # 使用默认基础（Windows用Win32GUI/Win32）
        target_name="antLLM-server.exe"  # 生成的可执行文件名
    )
]

setup(
    name="antLLM-server",
    version="0.1.17",
    description="AntLLM-SERVER",
    options=build_options,
    executables=executables
)