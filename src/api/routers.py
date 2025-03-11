from fastapi import APIRouter

from src.models.Deepmini import vision_pipeline
from src.schemas import tagger

router = APIRouter(
    prefix="/api",
    tags=["API ENTRANCE"],
)

# 图像标签识别API
@router.post("/tagger/", response_model=tagger.TaggerResponse)
async def tagging_images(body: tagger.TaggerQuery) -> tagger.TaggerResponse:
    uri_list = [uri.strip('\u202a') for uri in body.query_uris]
    return tagger.TaggerResponse(
        response=[
            tagger.TagItem(img_path=item.img_path,img_tags=item.img_tags) for item in vision_pipeline.evaluate(uri_list, is_return_path=False)
        ])

@router.post("/tag-translator/", response_model=list[str])
async def translate_tags(body: tagger.TagTranslatorQuery):
    print(body)

@router.post("/source/", response_model=tagger.TaggerResponse)
async def get_image_source(body: tagger.TagTranslatorQuery):
    print(body)