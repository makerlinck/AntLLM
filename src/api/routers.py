

from fastapi import APIRouter
from src.schemas import tagger


router = APIRouter(
    prefix="/api",
    tags=["API ENTRANCE"],
)

# 图像标签识别API
@router.post("/tagger/", response_model=tagger.TaggerResponse)
async def tagging_images(body: tagger.TaggerQuery) -> tagger.TaggerResponse:
    try:
        # 确保每个URI都是有效的文件路径且不为空文件
        from src.utils.FileManager.checker import check_file
        from pathlib import Path
        uris_seq = [
            (i, Path(str(uri).strip('\u202a'))) for i,uri in enumerate(body.query_uris)
            if check_file(Path(str(uri).strip('\u202a')),file_type='image')]
        # 使用线程池执行同步函数
        from src.models.Deepmini import evaluate as eva
        eva_results = eva(
            uris_seq,
            tag_language=body.tag_language,
            is_return_path=False,
            verbose=False
        )
        # 构建响应
        return tagger.TaggerResponse(
            response=[
                tagger.TagItem(
                    img_seq=item.img_seq,
                    img_tags=item.img_tags
                )
                for item in eva_results
            ]
        )
    except OSError as e:
        # 记录错误并返回空响应
        print(f"Tagger Error: {e}")
        return tagger.TaggerResponse(response=[])


@router.post("/tag-translator/", response_model=list[str])
async def translate_tags(body: tagger.TagTranslatorQuery):
    print(body)

@router.post("/source/", response_model=tagger.TaggerResponse)
async def get_image_source(body: tagger.TagTranslatorQuery):
    print(body)