# dythanh22.github.io

Ghi chú học tập: kiến trúc mô hình và tối ưu inference. Hosted on [GitHub Pages](https://dythanh22.github.io).

## Cấu trúc

```text
bai-hoc/
  architecture-models/     → chuỗi có nhóm (mỗi model = 1 thư mục)
    AlexNet/ VGG/ ResNet/ DenseNet/
    RNN/ LSTM/ GRU/
    VAE/ GAN/
    Word2Vec/
    Transformer/ BERT/ Vision-Transformer/
    UNet/
  ai-optimize/             → chuỗi phẳng (mỗi file = 1 bài)
assets/                    → CSS / JS
.github/workflows/         → Deploy Pages
```

## Local

```bash
quarto preview          # http://localhost:4321
```

## Thêm bài

Trong **một model đã có**: thêm file `.qmd` với `order` — `auto` trong sidebar tự nhận.

**Model mới**: thêm thư mục nhóm, rồi một dòng `auto:` đúng phần trong `_quarto.yml` (CNN / Sequence / …).

Frontmatter tối thiểu:

```yaml
title: "Tên bài"
order: 3
date: 2026-08-22
description: "Một câu mô tả"
role: "Vai trò ngắn trên bảng lộ trình"
# categories / series / group kế thừa từ _metadata.yml
```

## GitHub Pages

1. Push nhánh `main`.
2. Repo **Settings → Pages → Source = GitHub Actions**.
3. Đợi workflow *Publish Quarto site* (1–3 phút).
4. Mở `https://dythanh22.github.io`.
