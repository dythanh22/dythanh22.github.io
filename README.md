# dythanh22.github.io

Ghi chú học tập theo **chuỗi có thứ tự** — nền toán, lý thuyết AI, kiến trúc mô hình, và tối ưu inference.

**Site:** [https://dythanh22.github.io](https://dythanh22.github.io)  
**Stack:** Quarto 1.9 · Bootstrap (cosmo / darkly) · GitHub Pages + Actions  
**Không backend** — toàn nội dung tĩnh.

---

## Bốn chuỗi bài học

| Chuỗi | Nội dung | Quy mô |
|---|---|---|
| **[Math Base](https://dythanh22.github.io/bai-hoc/math-base/)** | Nền toán (ưu tiên đọc trước): xác suất → thống kê → đại số tuyến tính → giải tích → tối ưu → thông tin → đồ thị | 7 chapter · ~67 bài |
| **[Theory AI](https://dythanh22.github.io/bai-hoc/theory-ai/)** | Ôn nhanh + code: xác suất → thống kê → đại số tuyến tính → features / classical ML → activations, optimizers, DL → CV / NLP / RL / time series / recommender → MLOps | 15 chapter · ~187 bài ngắn |
| **[Architecture Models](https://dythanh22.github.io/bai-hoc/architecture-models/)** | CNN → sequence → generative → embeddings → attention → U-Net; mỗi model tách theo khối xây dựng | ~15 model · ~70 chương |
| **[AI Optimization](https://dythanh22.github.io/bai-hoc/ai-optimize/)** | Artifact → production: ONNX, TensorRT, Triton, profiling, rollout, LLM serving | 10 lesson |

Pipeline: **Math Base → Theory AI → Architecture Models → AI Optimization**.

Cách đọc: chọn một chuỗi → đi theo sidebar và nút trước/sau. Trình duyệt nhớ trang đã mở (localStorage) để tiếp tục sau.

---

## Cấu trúc repo

```text
bai-hoc/
  math-base/                 # 01-probability … 07-graph-theory
  theory-ai/                 # 01-probability … 15-mlops (mỗi chapter = thư mục)
  architecture-models/       # AlexNet, VGG, ResNet, … UNet
  ai-optimize/               # lesson-01 … lesson-10 (chuỗi phẳng)
assets/
  css/custom.scss            # theme & homepage
  js/                        # progress, continue-reading
  img/                       # favicon, hero, OG cover
_partials/                   # khung mở bài / reading-modes
scripts/                     # tiện ích (self-check, SVG theme, …)
.github/workflows/           # publish Pages + Lighthouse CI
_quarto.yml                  # navbar, sidebar, render whitelist
```

Render whitelist (trong `_quarto.yml`): chỉ publish `index`, `about`, `404`, và bốn chuỗi trên. Thư mục như `du-an/`, `nghien-cuu/` bị loại.

---

## Chạy local

Cần [Quarto](https://quarto.org/docs/get-started/) **≥ 1.9** (CI dùng `1.9.37`).

```bash
quarto preview    # http://localhost:4321
# hoặc
quarto render     # xuất ra _site/
```

---

## Thêm / sửa bài

### Frontmatter tối thiểu

```yaml
title: "Tên bài (English Name)"
order: 3
date: 2026-08-26
description: "Một câu mô tả (listing / SEO)"
series: math-base          # hoặc theory-ai | architecture-models | ai-optimize
categories: [math-base, …]
```

Architecture Models thường thêm `role` (cột “Vai trò” trên bảng lộ trình). Math / Theory có thể thêm `group` theo chapter.

### Theo từng chuỗi

| Chuỗi | Cách thêm |
|---|---|
| **Math Base** | Thêm `.qmd` vào đúng thư mục chapter (`01-probability/`, …). Sidebar dùng `auto: …/*.qmd` + `order`. `title` dạng Việt (English). |
| **Theory AI** | Thêm `.qmd` vào đúng thư mục chapter (`01-probability/`, …). Sidebar dùng `auto: …/*.qmd` + `order`. Không cần sửa YAML trừ khi thêm **chapter mới**. |
| **Architecture Models** | Trong model đã có: thêm `.qmd` với `order`. Model mới: tạo thư mục + một dòng `auto:` trong section phù hợp ở `_quarto.yml`. |
| **AI Optimization** | Thêm `lesson-NN-….qmd` và khai báo tường minh trong sidebar `ai-optimize` của `_quarto.yml`. |

Khung mở đầu / “Đọc nhanh · Đọc đủ”: `_partials/reading-modes.md`  
```markdown
{{< include /_partials/reading-modes.md >}}
```

---

## Deploy (GitHub Pages)

1. Push nhánh `main` (hoặc chạy workflow thủ công).
2. Repo **Settings → Pages → Source = GitHub Actions**.
3. Workflow **Publish Quarto site** render rồi publish `_site`.
4. Mở [https://dythanh22.github.io](https://dythanh22.github.io).

RSS listing: `/bai-hoc/index.xml` (footer site cũng có link RSS).

Lighthouse (không chặn deploy): workflow **Lighthouse CI** — chạy tay hoặc theo lịch.

---

## Ghi chú cho contributor

- Giữ `order` liên tục trong từng model / chapter / chuỗi.
- Hình minh họa ưu tiên SVG; nền sơ đồ do CSS site xử lý (dark/light).
- File ghi chú nội bộ (`check-ui-2.md`, `build-math-lesson.md`, …) nằm trong `.gitignore` — không đưa lên Pages.

---

## Liên hệ

- Tác giả: [dythanh22](https://github.com/dythanh22)
- Repo site: [dythanh22/dythanh22.github.io](https://github.com/dythanh22/dythanh22.github.io)
- Giới thiệu trên site: [/about.html](https://dythanh22.github.io/about.html)
