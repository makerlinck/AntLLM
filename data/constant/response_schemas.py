from langchain.output_parsers import ResponseSchema

response_schemas = [
    ResponseSchema(
        name="think",
        description="分析图片内容并选择最适合分类",
    ),
    ResponseSchema(
        name="class",
        description="图片类别",
    ),
]