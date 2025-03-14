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

        uris_seq = [
            (i, Path(str(uri).strip('\u202a'))) for i,uri in enumerate(body.query_uris)
            if check_file(Path(str(uri).strip('\u202a')),file_type='image')]
        # 使用线程池执行同步函数
        from src.models.Deepmini import evaluate
        eva_results = evaluate(
            uris_seq,
            tag_language=body.tag_language,
            is_return_path=False,
            verbose=False
        )
        # 构建响应
        print(f"Tagger Response at {time.time()}")
        response = tagger.TaggerResponse(
            response=[
                tagger.TagItem(
                    img_seq=item.img_seq,
                    img_tags=item.img_tags
                )
                for item in eva_results
            ])
        await websocket.send_json(response.model_dump())  # 确保发送完成
        await asyncio.sleep(0.1)                    # 延迟0.1秒后关闭连接
    except Exception as e:
        try:
            await websocket.send_json({"error": str(e)})
        except Exception as send_err:
            print(f"Failed to send error response: {send_err}")
    finally:
        await websocket.close()

router_api = APIRouter(
    prefix="/api",
    tags=["API ENTRANCE"],
)


@router_api.post("/tag-translator/", response_model=list[str])
async def translate_tags(body: tagger.TagTranslatorQuery):
    print(body)

@router_api.post("/source/", response_model=tagger.TaggerResponse)
async def get_image_source(body: tagger.TagTranslatorQuery):
    print(body)