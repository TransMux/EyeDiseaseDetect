import json
import time
from pathlib import Path

disease_detection_template = {
    "model": None,
    "status": None,
    "x1": None,
    "y1": None,
    "x2": None,
    "y2": None,
    "confidence": None
}

risk_evaluate_template = {
    "model": None,
    "status": None,
    "disease": None,
    "confidence": None
}


def meta_template():
    return {
        "create_time": int(time.time()),
        "result": {}
    }


def load_meta(path, base) -> dict:
    file = path / f"{base}.json"
    if file.exists():
        # 如果文件存在
        with file.open("r") as f:
            meta = json.load(f)
        return meta
    else:
        print(f"Warning: {file} 的meta信息不存在,为其创建默认meta文件")
        content = meta_template()
        with file.open("a") as f:
            json.dump(content, f)
        return content


def search_assets_structure(path: Path, assets: Path, depth=0):
    result = []
    # 文件夹
    for index, item in enumerate(path.iterdir()):
        if item.is_file():
            # 校验文件拓展名
            base, ext = item.name.rsplit(".", 1)
            if ext in ["jpg", "png"]:
                meta = load_meta(path, base)

                result.append(
                    {
                        "label": item.name,
                        "value": str(item.relative_to(assets)),
                        "children": None,
                        "meta": meta
                    },
                )
            elif ext == "json":
                # ini 将会在加载图片的时候自动引入
                continue
            else:
                print(f"Warning: {item} 的拓展名无法识别，将不会被录入进系统")
                pass
        else:
            # 文件夹
            children = search_assets_structure(item, assets, depth + 1)
            result.append(
                {
                    "label": item.name,
                    "value": str(item.relative_to(assets)),
                    "children": children,
                    "meta": None
                },
            )

    return result
