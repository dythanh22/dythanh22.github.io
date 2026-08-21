# dythanh22.github.io

Website cá nhân — ghi chú học tập, dự án và nghiên cứu. **v1 hiện tại: trang chủ hoàn chỉnh, chưa có bài viết.** Built with [Quarto](https://quarto.org), hosted on [GitHub Pages](https://dythanh22.github.io).

## Cấu trúc

```text
bai-hoc/       → Bài học, chuỗi ghi chú theo chủ đề
du-an/         → Dự án thực hành end-to-end
nghien-cuu/    → Paper notes, survey chủ đề
legacy/        → HTML cũ (copy nguyên vẹn, không render)
assets/        → CSS, hình ảnh dùng chung
```

## Phát triển local

```bash
# Cần cài Quarto: https://quarto.org/docs/get-started/
quarto preview
```

Site chạy tại `http://localhost:4321`.

## Thêm bài mới

1. Tạo file `.qmd` trong `bai-hoc/`, `du-an/` hoặc `nghien-cuu/`.
2. Đặt tên: `{số}-{slug-kebab}.qmd` (ví dụ `03-vong-lap.qmd`).
3. Thêm frontmatter (`title`, `date`, `categories`, ...).
4. Push lên `main` — GitHub Actions tự render và deploy.

Sidebar tự cập nhật nhờ cấu hình `auto:` — **không cần sửa `_quarto.yml`**.

## Deploy

Push lên nhánh `main`. Workflow `.github/workflows/publish.yml` sẽ:

1. `quarto render` → tạo `_site/`
2. Deploy artifact lên GitHub Pages

**Lần đầu:** vào repo Settings → Pages → Source = **GitHub Actions**.

## Quy ước đặt tên

| Quy tắc | Ví dụ |
|---------|-------|
| Slug kebab-case, không dấu | `01-bien-va-kieu-du-lieu.qmd` |
| Prefix số cho chuỗi có thứ tự | `01-`, `02-`, ... |
| Ưu tiên `.qmd` | Hỗ trợ code chunk Python/R |
| Draft | `draft: true` trong frontmatter |

## Legacy HTML

Copy HTML cũ vào `legacy/{ten}/` — giữ nguyên cấu trúc file. Quarto copy sang output mà không render lại.

## License

Nội dung cá nhân — học tập và tham khảo.
