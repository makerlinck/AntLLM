# 程序主入口
from pathlib import Path

from langchain.output_parsers import StructuredOutputParser
from bin.file_manager import fm
from data.constant.response_schemas import response_schemas
from data.constant.prompt import classifier_prompt
from data.constant.model_provider import initialize_classifier_llm
from test_run_deepmini import run_deepmini

parser = StructuredOutputParser.from_response_schemas(response_schemas)
chain = classifier_prompt | initialize_classifier_llm | parser

if __name__ == "__main__":
    for content in run_deepmini():

        response = chain.invoke({"query": f"图片内容描述关键词:{content}"})
        print(response.get("think"))
        print(response.get("class"))
        img_path = content["img_path"]
        type(img_path)
        img_keywords = content["img_tags"]
        fm.move_file(img_path, response.get("class", "other"))
        print(type(img_path))
#