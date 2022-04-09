from pathlib import Path


def search_assets_structure(assets: Path, depth=0):
    result = []
    # 文件夹
    for index, item in enumerate(assets.iterdir()):
        key = f"{depth}>{index}"
        if item.is_file():
            # 校验文件拓展名
            assert item.name.split(".")[-1] in ["jpg", "png"]
            result.append(
                {
                    "label": item.name,
                    "value": key,
                    "children": None
                },
            )
        else:
            # 文件夹
            children = search_assets_structure(item, depth + 1)
            result.append(
                {
                    "label": item.name,
                    "value": key,
                    "children": children
                },
            )

    return result
