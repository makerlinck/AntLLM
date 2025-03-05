import base64
from io import BytesIO
from PIL import Image
from langchain_ollama import OllamaLLM


def vision_pipeline(image_path, prompt):
    # 1. 图像编码
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # 2. 模型初始化
    llm = OllamaLLM(
        model="mistral",
        base_url="http://127.0.0.1:11434",
        temperature=0.3
    )

    # 3. 绑定视觉上下文
    bound_llm = llm.bind(images=[img_b64])

    # 4. 执行请求
    return bound_llm.invoke(prompt)


# 使用示例
response = vision_pipeline(
    "D:/Project/PycharmProject/AntOllama/origin/7118039608968647736.JPG",
    "描述这张图片的主要内容，并指出最显著的视觉元素"
)
print(response.content)
