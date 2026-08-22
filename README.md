# dythanh22.github.io

Ghi chú học tập: kiến trúc mô hình và tối ưu inference. Hosted on [GitHub Pages](https://dythanh22.github.io).

## Cấu trúc

```text
bai-hoc/
  architecture-models/     → chuỗi có nhóm (mỗi model = 1 thư mục)
    AlexNet/               → các bài thành phần (.qmd + order)
  ai-optimize/             → chuỗi phẳng (mỗi file = 1 bài)
assets/                    → CSS / JS
.github/workflows/         → Deploy Pages
```

## Local

```bash
quarto preview          # http://localhost:4321
```

## Thêm bài (không sửa `_quarto.yml`)

1. Tạo file `.qmd` trong đúng thư mục chuỗi (hoặc thư mục nhóm, ví dụ `AlexNet/`).
2. Frontmatter tối thiểu:

```yaml
title: "Tên bài"
order: 3
date: 2026-08-22
description: "Một câu mô tả"
role: "Vai trò ngắn trên bảng lộ trình"
# categories / series / group kế thừa từ _metadata.yml
```

3. Sidebar, breadcrumb, listing và bảng lộ trình tự cập nhật theo `order`.

## GitHub Pages

1. Push nhánh `main`.
2. Repo **Settings → Pages → Source = GitHub Actions**.
3. Đợi workflow *Publish Quarto site* (1–3 phút).
4. Mở `https://dythanh22.github.io`.
