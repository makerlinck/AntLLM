import asyncio
from pathlib import Path
from src.models.Deepmini import evaluate


async def run_test_evaluation():
    from src.models.Deepmini.data_loader import PACKAGE_PATH
    print("Input test or dir of image to run test_demo")
    while input_ := input("Press Enter to Quit: "):

        path = PACKAGE_PATH.joinpath("test/test.jpg") if input_ == "test" else Path(input_)
        if not (path.exists() and path.suffix in [".jpg", ".png", ".webp"]):
            print(f"Invalid path of {path}")
            continue
        async for item in evaluate(
            [(0,path)],
            tag_language="zh-cn",
            is_return_uri_as_path=True,
        ):
            print(item)

if __name__ == "__main__":
    asyncio.run(run_test_evaluation())


