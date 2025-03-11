from langchain.output_parsers import ResponseSchema

response_schemas = [
    ResponseSchema(
        name="class",
        description="图片类别",
    ),
]