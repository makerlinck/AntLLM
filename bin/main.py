# 程序主入口
from langchain.output_parsers import StructuredOutputParser
from data.constant.response_schemas import response_schemas
from data.constant.prompt import classifier_prompt
from dd_viewer import get_evaluation
from bin.utils.model_provider import initialize_classifier_llm
from bin.utils.executor.file_manager import FileManager

alice = FileManager()
work_dir = alice.work_dir
orig_dir = alice.origin_dir
output_dir = alice.output_dir

parser = StructuredOutputParser.from_response_schemas(response_schemas)
chain = classifier_prompt | initialize_classifier_llm | parser

if __name__ == "__main__":
    imgs = []
    for img_path in alice.get_origin_files(recursive=True):
        print(f"{img_path}")
        imgs.append(img_path)
    img_keywords = get_evaluation(imgs)
    # response = chain.invoke({"query": f"图片内容描述关键词:{img_keywords}"})
    # print(response.get("think"))
    # print(response.get("class"))
    # print(response.get("keyword"))
    # alice.move_file(Path(img_path), response.get("class", "other"))

