import asyncio
import time
from fastapi import APIRouter
from starlette.websockets import WebSocket
from src.schemas import tagger
router_ws = APIRouter(
    prefix="/ws",
    tags=["WS CONNECTION ENTRANCE"],
)


# 图像标签识别API
@router_ws.websocket("/tagger")
async def tagging_images(websocket: WebSocket):
    await websocket.accept()  # 接受连接
    try:
        # 接收客户端发送的数据
        data = await websocket.receive_json()
        body = tagger.TaggerQuery(**data)  # 手动解析请求体
        # 确保每个URI都是有效的文件路径且不为空文件
        from src.utils.FileManager.checker import check_file
        from pathlib import Path

        uris_seq = [(i, uris) for i, uri in enumerate(body.query_uris)
                    if (uris := Path(str(uri).strip('\u202a'))) and check_file(uris, file_type='image')]

        from src.models.Deepmini import evaluate
        async for item in evaluate(
            uris_seq,
            tag_language=body.tag_language,
            is_return_uri_as_path=False
        ):
            await websocket.send_json({
                "status": "progressing",
                "progress": item.img_seq[0],
                "content": tagger.TagItem(
                    img_seq=item.img_seq,
                    img_tags=item.img_tags
                ).model_dump()
            })

        await websocket.send_json({
            "status": "done",
            "timestamp": time.time()
        })
        await websocket.close()
    except Exception as e:
        try:
            await websocket.send_json({"error": str(e)})
        except Exception as e:
            print(e)
            await websocket.close()

router_api = APIRouter(
    prefix="/api",
    tags=["API ENTRANCE"],
)


@router_api.post("/tag-translator", response_model=list[str])
async def translate_tags(body: tagger.TagTranslatorQuery):
    print(body)

@router_api.post("/source", response_model=tagger.TaggerResponse)
async def get_image_source(body: tagger.TagTranslatorQuery):
    print(body)