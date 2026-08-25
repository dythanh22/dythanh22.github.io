#!/usr/bin/env python3
"""Convert ResNet/DenseNet .md lessons to .qmd with site frontmatter."""

from __future__ import annotations

from pathlib import Path

ROOT = Path("/home/iast-xeon-4/PycharmProjects/my_docs/bai-hoc/architecture-models")

RESNET = [
    {
        "src": "index.md",
        "dest": "index.qmd",
        "title": "ResNet",
        "subtitle": "Tổng quan pipeline residual: skip, stage, GAP",
        "order": 0,
        "role": "Mental model cả pipeline",
        "description": "Tổng quan ResNet: y = F(x)+x, identity/projection, bottleneck và ResNet-18.",
    },
    {
        "src": "1_Identity_Block.md",
        "dest": "identity-block.qmd",
        "title": "Identity Block",
        "order": 1,
        "role": "Residual khi chiều khớp — shortcut identity",
        "description": "Identity block: y = ReLU(F(x)+x), skip không tham số, ReLU sau phép cộng.",
    },
    {
        "src": "2_Convolutional_Block_Projection.md",
        "dest": "projection-block.qmd",
        "title": "Projection Block",
        "order": 2,
        "role": "Shortcut Ws khi đổi chiều hoặc stride",
        "description": "Convolutional/projection block: y = F(x)+Ws x tại chuyển tiếp stage ResNet.",
    },
    {
        "src": "3_Bottleneck_Block.md",
        "dest": "bottleneck-block.qmd",
        "title": "Bottleneck Block",
        "order": 3,
        "role": "1×1–3×3–1×1 cho ResNet-50+",
        "description": "Bottleneck residual: nén–xử lý–mở rộng channel, giữ skip connection.",
    },
    {
        "src": "4_Skip_Connections.md",
        "dest": "skip-connections.qmd",
        "title": "Skip Connections",
        "order": 4,
        "role": "Đường identity và dòng gradient",
        "description": "Residual connection y = F(x)+x: học residual, tránh suy thoái mạng sâu.",
    },
    {
        "src": "5_Batch_Normalization.md",
        "dest": "batch-normalization.qmd",
        "title": "Batch Normalization",
        "order": 5,
        "role": "Conv → BN → ReLU trong ResNet",
        "description": "BatchNorm: chuẩn hóa theo batch/channel, affine học được, ổn định huấn luyện sâu.",
    },
    {
        "src": "6_Full_ResNet.md",
        "dest": "full-resnet.qmd",
        "title": "Full ResNet",
        "order": 6,
        "role": "ResNet-18 đầu-cuối theo stage",
        "description": "Lắp ResNet-18: Conv1+pool, bốn stage BasicBlock, GAP và FC logits.",
    },
]

DENSENET = [
    {
        "src": "index.md",
        "dest": "index.qmd",
        "title": "DenseNet",
        "subtitle": "Tổng quan concat skip, growth rate và transition",
        "order": 0,
        "role": "Mental model cả pipeline",
        "description": "Tổng quan DenseNet: concat theo channel, growth rate k, compression θ, DenseNet-BC.",
    },
    {
        "src": "1_Channel_Growth.md",
        "dest": "channel-growth.qmd",
        "title": "Channel Growth",
        "order": 1,
        "role": "Đếm channel: k và compression θ",
        "description": "Lịch channel DenseNet: mỗi lớp thêm k map, transition nén bằng θ.",
    },
    {
        "src": "2_Composite_Layer.md",
        "dest": "composite-layer.qmd",
        "title": "Composite Layer",
        "order": 2,
        "role": "Hℓ = BN → ReLU → Conv 3×3",
        "description": "Composite layer DenseNet: pre-activation BN-ReLU-Conv3×3, xuất k feature map.",
    },
    {
        "src": "3_Bottleneck_Layer.md",
        "dest": "bottleneck-layer.qmd",
        "title": "Bottleneck Layer",
        "order": 3,
        "role": "DenseNet-B: 1×1 (4k) rồi 3×3 (k)",
        "description": "Bottleneck DenseNet-B: BN-ReLU-Conv1×1 4k rồi BN-ReLU-Conv3×3 k.",
    },
    {
        "src": "4_Dense_Block.md",
        "dest": "dense-block.qmd",
        "title": "Dense Block",
        "order": 4,
        "role": "Mọi lớp nối mọi lớp trước (concat)",
        "description": "Dense block: xℓ = Hℓ([x0,…,xℓ−1]), đầu ra C + L·k channel.",
    },
    {
        "src": "5_Transition_Layer.md",
        "dest": "transition-layer.qmd",
        "title": "Transition Layer",
        "order": 5,
        "role": "Nén channel và AvgPool giữa các block",
        "description": "Transition: Conv 1×1 nén θ·C rồi average pool 2×2 downsample.",
    },
    {
        "src": "6_Full_DenseNet.md",
        "dest": "full-densenet.qmd",
        "title": "Full DenseNet",
        "order": 6,
        "role": "Stem → block/transition → GAP → logits",
        "description": "Forward DenseNet đầy đủ: stem, dense block, transition, GAP và classifier.",
    },
]


def strip_first_h1(body: str) -> str:
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        if lines and lines[0].strip() == "":
            lines = lines[1:]
    return "\n".join(lines).rstrip() + "\n"


def yaml_block(lesson: dict, group: str, tag: str, src_name: str) -> str:
    extra = ""
    if lesson.get("subtitle"):
        extra += f'subtitle: "{lesson["subtitle"]}"\n'
    old_html = src_name.replace(".md", ".html")
    return f"""---
title: "{lesson["title"]}"
{extra}date: 2026-08-22
order: {lesson["order"]}
categories: [architecture-models, architecture, cnn, {tag}]
series: architecture-models
group: {group}
role: "{lesson["role"]}"
description: "{lesson["description"]}"
aliases:
  - /bai-hoc/architecture-models/{group}/{src_name}
  - /bai-hoc/architecture-models/{group}/{old_html}
---
"""


def convert(folder: str, group: str, tag: str, lessons: list[dict]) -> None:
    base = ROOT / folder
    for lesson in lessons:
        src = base / lesson["src"]
        body = strip_first_h1(src.read_text(encoding="utf-8"))
        qmd = yaml_block(lesson, group, tag, lesson["src"]) + "\n" + body
        dest = base / lesson["dest"]
        dest.write_text(qmd, encoding="utf-8")
        if dest.resolve() != src.resolve():
            src.unlink()
        print(f"wrote {dest.relative_to(ROOT)}")


def main() -> None:
    convert("ResNet", "ResNet", "resnet", RESNET)
    convert("DenseNet", "DenseNet", "densenet", DENSENET)


if __name__ == "__main__":
    main()
