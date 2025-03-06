import os

from langchain_core.tools import tool
from bin.utils.executor.file_manager import alice
from bin.utils.executor.image_viewer import get_image_content


@tool
def move_file_tool(src_file_name: str, dest_dir_name: str) -> str:
    """移动文件到指定路径,需提供<源文件名称.后缀>和目标文件<目录名>"""
    print("工具调用:MOVE_FILE_TOOL")
    return alice.move_file(src_file_name, dest_dir_name)