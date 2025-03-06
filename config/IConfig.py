class ISettings:
    version: str
    using_gui: bool
    working_dir_url: str
    as_service: bool
    ollama_api_url: str
    viewer_llm: str
    classifier_llm: str

class IDirFormat:
    output_dir_name: str
    fix_dirs: list[str]
