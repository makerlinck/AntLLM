import base64
from io import BytesIO
from pathlib import Path
from PIL import Image
from data.constant.prompt import viewer_prompt
from bin.utils.model_provider import initialize_viewer_llm
def vision_pipeline(image_path:Path):
    # 1. 图像编码
    with Image.open(image_path) as img:
        width, height = img.size
        # 格式验证
        if img.format not in {'GIF', 'JPEG', 'PNG', 'WEBP'}:
            return "Unsupported image format"
        buffered = BytesIO()
        # 动态保存原始格式
        img.save(buffered, format=img.format or 'PNG',quality=70)
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    bound_llm = initialize_viewer_llm.bind(images=[img_b64])
    chain = viewer_prompt | bound_llm
    img_info = f"$DEBUG INFO$\n图片尺寸:{width}*{height}\n图片名称:{image_path.name}\n图片格式:{img.format}\n图片路径:{image_path.absolute()}\n"
    print(f"\033[32m {img_info} \033[0m")
    # 4. 执行请求
    return chain.invoke({"input": "START"})
def get_image_content(image_path:Path) -> str:
    """
    获取图像内容的文字描述
    :param image_path: 图像文件路径:Path
    """
    response = vision_pipeline(
        image_path=image_path,
    )
    print(f"\033[32m {response} \033[0m")
    return response

