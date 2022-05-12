import time
from pathlib import Path


def meta_template():
    return {
        "create_time": int(time.time()),
        "tree": [
            {"id": 'root',
             "type": 'root',
             "label": 'root',
             "style": "{border: '1px solid #0163f7', padding: '5px', borderRadius: '5px'}",
             "position": "{x: 250, y: 5}"}
        ]
    }


def get_meta_info(root: Path, assets: Path):
    root_labels = []
    # 获取特定文件的meta信息
    result = [
        {
            "id": "root",
            "type": "label",
            "position": {"x": 0, "y": 0},
            "data": {
                "url": root,
                "labels": root_labels
            }
        }
    ]
    # 读取crops
    CROP = root.with_suffix(".crop")
    if CROP.exists():
        for crop in CROP.glob("*.jpg"):
            # 命名规则
            # 模型_id_[增强]_结果.jpg
            # 模型_id_原图_x1_y1_x2_y2.jpg
            name = crop.name.rstrip(".jpg")
            exps = name.split("_")
            url = str(crop.relative_to(assets))
            # 读取节点 自动生成 联系
            if exps[2] == "原图":
                # 节点
                result.append(
                    # 需要保证 root labels 在返回前会变化
                    {"id": f"{exps[1]}-origin", "data": {"url": url}, "position": {"x": 0, "y": 0}},
                )
                result.append(
                    {
                        "id": f"e-root-{exps[2]}",
                        "source": "root",
                        "target": f"{exps[1]}-origin"
                    },
                )
                root_labels.append({
                    "tag": f"{exps[0]} {exps[1]}",
                    "label": exps[-4:]
                })
            else:
                result.append(
                    {"id": f"{exps[1]}-{exps[2]}", "data": {"url": url}, "position": {"x": 0, "y": 0}},
                )
                # 联系
                result.append(
                    {
                        "id": f"e-{exps[1]}-{exps[2]}",
                        "source": f"{exps[1]}-origin",
                        "target": f"{exps[1]}-{exps[2]}"
                    },
                )
    else:
        CROP.mkdir()

    return result


def search_assets_structure(path: Path, assets: Path, depth=0):
    result = []
    # 文件夹
    for index, item in enumerate(path.iterdir()):
        if item.is_file():
            continue

        # 文件夹
        if item.name.endswith(".crop"):
            #     裁剪目录
            continue
        # Children
        children = search_assets_structure(item, assets, depth + 1)
        result.append(
            {
                "label": item.name,
                "value": str(item.relative_to(assets)),
                "children": children,
            },
        )

    return result
