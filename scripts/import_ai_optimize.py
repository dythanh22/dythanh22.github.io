#!/usr/bin/env python3
"""Extract lesson bodies from standalone Quarto HTML into site-themed .qmd files."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path("/home/iast-xeon-4/PycharmProjects/my_docs/bai-hoc/ai-optimize")
INCLUDE = ROOT / "_include"
SOURCE_HTML = ROOT / "_html"

LESSONS = [
    {
        "src": "index.html",
        "qmd": "index.qmd",
        "include": "index-body.html",
        "title": "AI Optimization for Inference Systems",
        "subtitle": "From ONNX and TensorRT to Triton, LLM Serving, and Production Operations",
        "date": "2026-05-14",
        "order": 0,
        "description": "Chuỗi 10 bài: từ model artifact đến production inference service.",
    },
    {
        "src": "lesson_1_modern_gpu_inference_architecture.html",
        "qmd": "lesson-01-modern-gpu-inference-architecture.qmd",
        "include": "lesson-01.html",
        "title": "Modern GPU Inference Architecture",
        "subtitle": "AI Optimization — Bài 1",
        "date": "2026-05-14",
        "order": 1,
        "description": "Mental model: GPU inference, latency, throughput, batching và bottleneck.",
    },
    {
        "src": "lesson_2_onnx_fundamentals.html",
        "qmd": "lesson-02-onnx-fundamentals.qmd",
        "include": "lesson-02.html",
        "title": "ONNX Fundamentals",
        "subtitle": "AI Optimization — Bài 2",
        "date": "2026-05-15",
        "order": 2,
        "description": "ONNX graph, operators, opset và export — IR cho runtime/compiler.",
    },
    {
        "src": "lesson_3_onnx_runtime_deep_dive.html",
        "qmd": "lesson-03-onnx-runtime-deep-dive.qmd",
        "include": "lesson-03.html",
        "title": "ONNX Runtime Deep Dive",
        "subtitle": "AI Optimization — Bài 3",
        "date": "2026-05-16",
        "order": 3,
        "description": "Execution Providers, graph optimization và I/O Binding.",
    },
    {
        "src": "lesson_4_tensorrt_internals.html",
        "qmd": "lesson-04-tensorrt-internals.qmd",
        "include": "lesson-04.html",
        "title": "TensorRT Internals",
        "subtitle": "AI Optimization — Bài 4",
        "date": "2026-05-17",
        "order": 4,
        "description": "Engine, tactics, profiles, FP16/INT8 — TensorRT như inference compiler.",
    },
    {
        "src": "lesson_5_quantization_deep_dive.html",
        "qmd": "lesson-05-quantization-deep-dive.qmd",
        "include": "lesson-05.html",
        "title": "Quantization Deep Dive",
        "subtitle": "AI Optimization — Bài 5",
        "date": "2026-05-18",
        "order": 5,
        "description": "PTQ, QAT, calibration, Q/DQ, INT8/FP8 — giảm memory/compute.",
    },
    {
        "src": "lesson_6_nvidia_triton_inference_server.html",
        "qmd": "lesson-06-nvidia-triton-inference-server.qmd",
        "include": "lesson-06.html",
        "title": "NVIDIA Triton Inference Server",
        "subtitle": "AI Optimization — Bài 6",
        "date": "2026-05-19",
        "order": 6,
        "description": "Model repository, backends, dynamic batching và production serving.",
    },
    {
        "src": "lesson_7_profiling_and_benchmarking_inference_systems.html",
        "qmd": "lesson-07-profiling-and-benchmarking.qmd",
        "include": "lesson-07.html",
        "title": "Profiling and Benchmarking Inference Systems",
        "subtitle": "AI Optimization — Bài 7",
        "date": "2026-05-20",
        "order": 7,
        "description": "trtexec, Perf Analyzer, Nsight Systems, tail latency và bottleneck.",
    },
    {
        "src": "lesson_8_safe_model_rollouts_and_production_operations.html",
        "qmd": "lesson-08-safe-model-rollouts.qmd",
        "include": "lesson-08.html",
        "title": "Safe Model Rollouts and Production Operations",
        "subtitle": "AI Optimization — Bài 8",
        "date": "2026-05-21",
        "order": 8,
        "description": "Canary, A/B, shadow, monitoring, autoscaling, SLO và incident response.",
    },
    {
        "src": "lesson_9_advanced_inference_systems_for_llms.html",
        "qmd": "lesson-09-llm-inference-systems.qmd",
        "include": "lesson-09.html",
        "title": "Advanced Inference Systems for LLMs",
        "subtitle": "AI Optimization — Bài 9",
        "date": "2026-05-22",
        "order": 9,
        "description": "KV cache, continuous batching, PagedAttention, vLLM, TensorRT-LLM.",
    },
    {
        "src": "lesson_10_end_to_end_capstone_project.html",
        "qmd": "lesson-10-end-to-end-capstone.qmd",
        "include": "lesson-10.html",
        "title": "End-to-End Capstone Project",
        "subtitle": "AI Optimization — Bài 10",
        "date": "2026-05-23",
        "order": 10,
        "description": "Build, optimize, benchmark và vận hành một production inference service.",
    },
]

LINK_MAP = [
    ("lesson_10_end_to_end_capstone_project.html", "lesson-10-end-to-end-capstone.qmd"),
    ("lesson_10_end_to_end_capstone_project.md", "lesson-10-end-to-end-capstone.qmd"),
    ("lesson_9_advanced_inference_systems_for_llms.html", "lesson-09-llm-inference-systems.qmd"),
    ("lesson_9_advanced_inference_systems_for_llms.md", "lesson-09-llm-inference-systems.qmd"),
    ("lesson_8_safe_model_rollouts_and_production_operations.html", "lesson-08-safe-model-rollouts.qmd"),
    ("lesson_8_safe_model_rollouts_and_production_operations.md", "lesson-08-safe-model-rollouts.qmd"),
    ("lesson_7_profiling_and_benchmarking_inference_systems.html", "lesson-07-profiling-and-benchmarking.qmd"),
    ("lesson_7_profiling_and_benchmarking_inference_systems.md", "lesson-07-profiling-and-benchmarking.qmd"),
    ("lesson_6_nvidia_triton_inference_server.html", "lesson-06-nvidia-triton-inference-server.qmd"),
    ("lesson_5_quantization_deep_dive.html", "lesson-05-quantization-deep-dive.qmd"),
    ("lesson_4_tensorrt_internals.html", "lesson-04-tensorrt-internals.qmd"),
    ("lesson_3_onnx_runtime_deep_dive.html", "lesson-03-onnx-runtime-deep-dive.qmd"),
    ("lesson_2_onnx_fundamentals.html", "lesson-02-onnx-fundamentals.qmd"),
    ("lesson_1_modern_gpu_inference_architecture.html", "lesson-01-modern-gpu-inference-architecture.qmd"),
    ("./index.html", "index.qmd"),
]


def extract_body(html: str) -> str:
    main = re.search(
        r'<main class="content"[^>]*id="quarto-document-content">(.*?)</main>',
        html,
        re.S,
    )
    if not main:
        raise SystemExit("Could not find main content")
    body = main.group(1)
    body = re.sub(
        r'<header id="title-block-header".*?</header>',
        "",
        body,
        count=1,
        flags=re.S,
    )
    body = re.sub(
        r'<h1 class="unnumbered">AI Optimization for Inference Systems</h1>\s*',
        "",
        body,
        count=1,
    )
    for old, new in LINK_MAP:
        body = body.replace(f'href="./{old}"', f"href=\"{new}\"")
        body = body.replace(f'href="{old}"', f"href=\"{new}\"")
    return body.strip() + "\n"


def write_qmd(lesson: dict, body: str) -> None:
    extra = ""
    if lesson["order"] == 0:
        extra = "toc: true\npage-layout: article\n"
    if "```" in body:
        fence = "````"
    else:
        fence = "```"
    yaml = f"""---
title: "{lesson['title']}"
subtitle: "{lesson['subtitle']}"
date: {lesson['date']}
categories: [ai-optimize, inference]
series: ai-optimize
series-order: {lesson['order']}
description: "{lesson['description']}"
{extra}---

{fence}{{=html}}
{body.rstrip()}
{fence}
"""
    (ROOT / lesson["qmd"]).write_text(yaml, encoding="utf-8")


def main() -> None:
    INCLUDE.mkdir(exist_ok=True)
    SOURCE_HTML.mkdir(exist_ok=True)

    for lesson in LESSONS:
        src = ROOT / lesson["src"]
        if not src.exists():
            src = SOURCE_HTML / lesson["src"]
        html = src.read_text(encoding="utf-8")
        body = extract_body(html)
        (INCLUDE / lesson["include"]).write_text(body, encoding="utf-8")
        write_qmd(lesson, body)
        dest = SOURCE_HTML / lesson["src"]
        if src != dest:
            shutil.move(str(src), str(dest))
        print(f"wrote {lesson['qmd']}")


if __name__ == "__main__":
    main()
