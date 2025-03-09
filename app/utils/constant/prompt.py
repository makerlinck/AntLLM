from langchain_core.prompts import PromptTemplate

viewer_prompt = PromptTemplate.from_template(
    """
    You are a senior image reviewer who needs to carefully analyze the content of the image. Please strictly use the following format to describe the objective content of the image.

    "Classification": "Style of images, such as photography/illustration/screenshots (including prominent user interface edges and specific aspect ratios), memes, etc.",
    "Theme":" The theme of the image, such as people/scenery/abstraction, etc. If it cannot be recognized, please write "unknown",
    "Description":" 
        - "Composition": "Half body centered composition, with the protagonist sitting upside down in the water and the background being a swimming pool and blue sky with white clouds"
        - "Main characteristics": "Clothing/expression, etc.",
        - "Action Details(if available)": "Provide a complete description of the action details",
        - "Body description(if available)": "Provide a complete and detailed body description :Body condition/exposed organs (such as legs/genitals/breasts, etc., which will be included in the keyword list)""
    """
)
image_class = [
    ["nsfw_anime(包含明显的暴露/成人/性爱内容等)"],
    ["sexy_anime(包含性暗示或者部分裸露内容)"],
    ["sfw_anime(正常的日式插画内容)"],
    ["other(其他)"]
]
classifier_prompt = PromptTemplate.from_template(
    f"你是一位经验丰富的插画分类专家，你的任务是根据给定的类别对图片进行准确分类。请严格按照以下类别标准执行分类工作：{str(image_class)}。"
    """
    任务指令：选择合适的分类并返回，输出JSON格式结果
    请严格按照以下格式执行：
    [
        "class":    "(图片类别)"
    ]
    现在请分类以下图片，该图片关键词为:
    {query}
    """
)