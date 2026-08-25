
# UI/UX Audit — dythanh22.github.io

**Phạm vi:** Website Quarto (GitHub Pages) gồm 2 chuỗi bài học — *Architecture Models* (12 model, ~70+ trang con) và *AI Optimization* (10 lesson).
**Phương pháp:** Audit dựa trên mã nguồn thực tế của repo `dythanh22/dythanh22.github.io` — `_quarto.yml`, `assets/css/custom.scss`, `assets/js/lesson-progress.html`, và nội dung `.qmd` của nhiều trang đại diện (homepage, about, index của 2 chuỗi, AlexNet, GRU, lesson-01/02/09 của AI Optimization). Đây là audit **cấp mã nguồn + cấu trúc render**, không phải audit từ ảnh chụp màn hình trình duyệt thật — những điểm cần xác nhận bằng mắt được ghi rõ là **"cần kiểm tra trực quan"**.
**Ràng buộc tôn trọng khi đề xuất:** Không đổi kiến trúc/framework, chỉ dùng Quarto/Markdown/YAML/SCSS/HTML/JS thuần, giữ khả năng build bằng `quarto render` và deploy GitHub Pages/Actions hiện tại.

---

## 0. Tóm tắt nhanh (executive summary)

Đây là một site Quarto được cấu hình **tốt hơn mặt bằng chung** của các blog cá nhân: có search built-in, breadcrumb, prev/next, reader-mode, front-matter schema nhất quán (`order`, `series`, `group`, `role`, `categories`), SVG có `alt`/`title`/`role="img"`. Vấn đề lớn nhất **không phải** là thiếu tính năng, mà là **thiếu tính nhất quán giữa 2 chuỗi bài** (được viết bằng 2 quy trình khác nhau) và **thiếu vòng lặp quay lại học** (không có progress lưu lại, không RSS, không trang "hoàn thành chuỗi"). Có 1 lỗi kỹ thuật cụ thể, có bằng chứng rõ ràng: **biểu đồ SVG không đồng bộ với nút chuyển dark/light mode thủ công của site**.

---

## 1. Audit UI/UX các trang bài học

### 1.1 Visual hierarchy, typography, màu sắc, spacing, layout, consistency

**Bằng chứng từ `_quarto.yml` + `custom.scss`:**
```scss
$font-family-sans-serif: "Inter", system-ui, ...
$font-family-monospace: "JetBrains Mono", ui-monospace, ...
$headings-font-weight: 600;
$link-color: #1d4ed8;
#quarto-document-content { max-width: 52rem; }         // trang lesson
.page-layout-full #quarto-document-content { max-width: 64rem; } // homepage
```

- **Tốt:** Inter + JetBrains Mono là cặp font hợp lý cho nội dung kỹ thuật (số liệu, code, LaTeX). `max-width: 52rem` (~832px) cho trang bài học tương đương ~75–85 ký tự/dòng ở cỡ chữ mặc định — nằm trong khoảng đọc thoải mái theo khuyến nghị typography (45–90 ký tự).
- **Vấn đề — không nhất quán numbering:** Trang chỉ mục mỗi chuỗi tự đánh số thủ công ("1. CNN", "2. Sequence"…) và bảng "Lộ trình chi tiết" có cột `#` (order), nhưng **trong sidebar thực tế, các mục con không có số thứ tự hiển thị** (chỉ có tên: "AlexNet", "Các lớp tích chập của AlexNet"…). Người học phải dựa vào badge "Chương X/Y" được JS inject (xem 1.3) để biết vị trí — nghĩa là có **3 hệ thống đánh số khác nhau** (mục lục trang chủ chuỗi, order trong front-matter, badge JS) không map 1:1 với nhau về mặt hiển thị.
- **Vấn đề — 2 "giọng" trình bày khác nhau giữa 2 chuỗi:** Kiểm tra trực tiếp source cho thấy `bai-hoc/ai-optimize/lesson-02-onnx-fundamentals.qmd` chứa **22 khối HTML thô** dạng:
  ```html
  <div class="callout callout-style-default callout-note no-icon callout-titled">...</div>
  ```
  trong khi các bài `architecture-models` (VGG, AlexNet, GRU…) **không dùng callout nào** — chỉ có heading + đoạn văn + công thức + figure. Hệ quả: chuỗi *AI Optimization* có khung "Mục tiêu bài học", "Lộ trình bài học", "Đọc nhanh/Đọc đủ" rất scaffolded, còn *Architecture Models* đọc như một bài báo khoa học thuần túy — trải nghiệm đọc thay đổi hẳn tùy chuỗi, dù cùng một site, cùng một tác giả.

### 1.2 Khả năng đọc hiểu, tập trung, tiếp thu

- **Chênh lệch độ dài rất lớn giữa các "chương":** so sánh trực tiếp số từ:
  | Trang | Số từ |
  |---|---|
  | `AlexNet/convolution.qmd` | ~2.819 |
  | `ai-optimize/lesson-09-llm-inference-systems.qmd` | ~10.161 |

  Chênh lệch **3.6 lần** giữa hai "đơn vị đọc" được trình bày ngang hàng nhau trong sidebar (cùng là 1 mục, cùng 1 cấp). Người học không có cách nào biết trước một mục sẽ mất 8 phút hay 40 phút để đọc, trừ lesson-01 của AI Optimization vốn tự khai báo bảng thời lượng (10+15+20+15+15+30 phút) — **nhưng chỉ lesson đó có**, các lesson khác và toàn bộ Architecture Models thì không.
- **Điểm tốt — cơ chế "Đọc nhanh / Đọc đủ":** `lesson-01` có block:
  > *Đọc nhanh (~15–20 phút): chỉ các callout Ý chính + bảng + sơ đồ.* / *Đọc đủ: mở các tip "Con số cụ thể/Đào sâu", làm Mini-lab và Checkpoint.*

  Đây là progressive disclosure tốt cho một site có nội dung dài — nhưng **không được áp dụng lại** ở các bài khác đã kiểm tra (kể cả trong cùng chuỗi ai-optimize, class `.reading-modes` được định nghĩa generic trong CSS nhưng cách dùng có vẻ không phải mặc định mọi trang).
- **Thiếu tóm tắt cuối bài (TL;DR):** không thấy pattern "Tóm tắt" / "Điểm chính cần nhớ" ở cuối các trang đã kiểm tra — với nội dung dày đặc công thức, một khối tóm tắt 3–5 gạch đầu dòng cuối bài sẽ hỗ trợ ghi nhớ đáng kể.
- **Điểm tốt:** AlexNet/index có mục "Ký hiệu được sử dụng trong phần này" liệt kê rõ ký hiệu toán học trước khi vào nội dung — thực hành tốt, giảm tải nhận thức khi đọc công thức phía sau.

### 1.3 Navigation, progress, breadcrumbs, wayfinding

**Bằng chứng — `_quarto.yml`:**
```yaml
website:
  reader-mode: true
  page-navigation: true
  bread-crumbs: true
  back-to-top-navigation: true
```
Đây là nền tảng tốt: mọi trang đều có breadcrumb, nút trang trước/sau theo đúng thứ tự sidebar, nút "về đầu trang", và chế độ đọc không xao nhãng (reader-mode) — 4 tính năng wayfinding cơ bản đã bật sẵn, nhiều site Quarto thực tế bỏ quên các cờ này.

**Bằng chứng — `assets/js/lesson-progress.html`:** một script tự chèn badge kiểu "Chương 2/6" ngay dưới tiêu đề, dựa vào việc dò `li.sidebar-item.active` trong DOM.
- **Vấn đề cụ thể trong chính script:**
  ```js
  if (/tổng quan chuỗi/i.test(label)) return;
  ```
  Script **chủ động bỏ qua** trang tổng quan của mỗi chuỗi (trang đầu tiên người mới chạm vào) — nghĩa là đúng trang mà người học *mới* landing vào đầu tiên lại là trang **duy nhất không có tín hiệu định hướng "bạn đang ở đâu"**, tín hiệu này chỉ xuất hiện từ chương thứ 2 trở đi.
- **2 sidebar tách biệt, không giao nhau:** `_quarto.yml` định nghĩa 2 sidebar riêng (`id: architecture-models`, `id: ai-optimize`), mỗi trang chỉ thấy sidebar của chuỗi mình đang đọc. Không có cross-link nào giữa nội dung liên quan (ví dụ trang *Transformer* của Architecture Models và lesson *LLM Inference Systems* của AI Optimization — hai chủ đề nối tiếp nhau về mặt kiến thức — không tham chiếu nhau ở bất kỳ trang nào đã kiểm tra).
- **Cần xác minh trực quan — khả năng khớp thứ tự trong bảng roadmap:** Khi trích xuất bảng "Lộ trình chi tiết → GRU" trên trang `architecture-models/index.qmd` (bảng này được Quarto `listing` sinh tự động từ `order` trong front-matter của từng file `GRU/*.qmd`), thứ tự cột `#` đọc được là `1, 2, 4, 5, 6` — **thiếu số 3**. Kiểm tra ngược lại front-matter thì `GRU/candidate.qmd` có `order: 3` hợp lệ, cùng `categories`/`series` như các file khác — không có lý do rõ ràng để bị loại khỏi listing. Đây có thể là lỗi build/listing thật, hoặc là artifact của công cụ trích xuất — **khuyến nghị build lại và kiểm tra bằng mắt bảng này** vì nếu là lỗi thật, nó nằm đúng ở nơi người học dùng để xác định thứ tự đọc.

### 1.4 Code block, hình ảnh, biểu đồ, công thức, bảng, callout, tương tác

- **Code block:** `code-copy: true`, `code-overflow: wrap`, highlight `github`/`github-dark` theo light/dark — cấu hình chuẩn, ổn. Lưu ý: `code-overflow: wrap` phù hợp với đoạn văn nhưng với lệnh CLI dài (`trtexec --onnx=... --fp16 --shapes=...` kiểu nội dung ở AI Optimization) wrap có thể làm khó copy-paste chính xác hơn là scroll ngang — nên cân nhắc `code-overflow: scroll` riêng cho code block CLI/JSON dài, giữ `wrap` cho code Python ngắn.
- **Hình ảnh/SVG — điểm mạnh về accessibility:** SVG được viết tay có `role="img"`, `<title>`, `aria-labelledby`, và `fig-alt` mô tả rõ ràng ở cấp Quarto figure. Đây là mức accessibility tốt hơn hẳn phần lớn blog kỹ thuật (thường chỉ dùng `<img>` trơn).
- **🔴 Lỗi kỹ thuật xác nhận được — biểu đồ không đồng bộ dark mode thủ công:** Trích xuất trực tiếp 1 file SVG (`AlexNet/figures/01-pipeline-overview.svg`):
  ```css
  .fig-bg { fill: #F7F8FA; }
  @media (prefers-color-scheme: dark) { .fig-bg { fill: #1B1F24; } }
  ```
  SVG đổi màu nền dựa vào **`prefers-color-scheme`, tức cài đặt hệ điều hành**, còn nút "Toggle dark mode" của Quarto trên site lại chuyển theme bằng cách gắn `data-bs-theme`/class vào `<html>` — **hai cơ chế độc lập, không liên quan nhau**. Hậu quả thực tế: nếu OS đang ở light mode nhưng người dùng bấm nút chuyển site sang dark, mọi biểu đồ SVG vẫn giữ nền xám sáng `#F7F8FA` giữa một trang nền tối — ngược lại OS dark + site light thì biểu đồ tối giữa nền sáng. Đây không phải giả định — là đọc trực tiếp từ CSS trong file SVG.
- **Làm nặng thêm vấn đề trên:** `custom.scss` còn ép cứng:
  ```scss
  .quarto-figure img, .figure img, main img {
    background: #f7f8fa;
    border-radius: 0.5rem;
  }
  ```
  tức là **mọi ảnh trên site** (kể cả các SVG đã tự xử lý dark mode ở trên, kể cả ảnh raster tương lai) đều bị gán nền xám sáng cố định ở cấp container, bất kể theme — một lớp light-leak thứ hai chồng lên lớp thứ nhất.
- **Bảng:** các bảng nội dung nhiều cột (bảng "Lộ trình bài học" 4 cột của lesson-01, các bảng "Lộ trình chi tiết" 3 cột) dùng `colgroup` với width cố định theo % (ví dụ `7%/15%/44%/31%`). `custom.scss` **không có** rule `overflow-x`/`table-responsive` cho bảng trong nội dung bài — trên viewport hẹp (điện thoại dọc, ~360–390px) các bảng nhiều chữ tiếng Việt này nhiều khả năng vỡ layout hoặc bị nén khó đọc — **cần kiểm tra trực quan trên mobile thật**.
- **Callout:** dùng nhiều ở AI Optimization (Mục tiêu bài học, Lộ trình, Ghi chú/Cảnh báo/Mẹo — đã map tiếng Việt đầy đủ trong `_quarto.yml` phần `language:`), **không dùng** ở Architecture Models. Xem thêm 1.1.
- **Quiz/tương tác:** Không tìm thấy bất kỳ thành phần quiz, flashcard, hay "kiểm tra nhanh" nào trong toàn bộ source đã kiểm tra (`custom.scss`, `lesson-progress.html`, các `.qmd` mẫu). Với khối lượng nội dung kỹ thuật lớn (70+ trang Architecture Models, 10 lesson dài AI Optimization), việc hoàn toàn thiếu cơ chế tự kiểm tra hiểu bài là một khoảng trống rõ với một site tự nhận là "học tập".

### 1.5 Responsive (desktop/mobile/tablet)

Toàn bộ `custom.scss` chỉ có **một** breakpoint tường minh:
```scss
@media (max-width: 768px) {
  .home-hero, .home-more, .series-grid { grid-template-columns: 1fr; }
  .home-hero { padding-top: 1.25rem; }
}
```
- Breakpoint này **chỉ áp dụng cho homepage** (hero + 2 grid). Các thành phần khác (bảng roadmap nhiều cột, `.lessons-guide-item`, `.reading-modes`, sidebar) hoàn toàn dựa vào default của Bootstrap/Quarto — không sai, nhưng cũng không được tinh chỉnh, nên **chưa được kiểm chứng riêng** cho các thành phần custom.
- **Không có breakpoint tablet riêng** (dải ~768–992px). `.series-grid`/`.home-more` chỉ có 2 trạng thái nhị phân (2 cột hoặc 1 cột tại đúng 768px) — một tablet dọc ở 780–820px vẫn sẽ nhận 2 cột, có thể chật với nội dung tiếng Việt dài hơn tiếng Anh trung bình ~15–20%.
- **Cần kiểm tra trực quan:** công thức LaTeX dài (ví dụ khối "Ký hiệu" nhiều dòng `\begin{aligned}` trong AlexNet) trên màn hình hẹp — MathJax mặc định có scroll ngang cho công thức quá khổ nhưng chưa xác nhận trải nghiệm này có mượt trên mobile hay không.

### 1.6 Accessibility

**Điểm mạnh (xác nhận từ source):**
- `lang: vi` trên toàn site → trình đọc màn hình phát âm đúng tiếng Việt.
- SVG có `role="img"` + `<title>` + `aria-labelledby`; figure có `fig-alt` mô tả nội dung sơ đồ chứ không phải tên file.
- Nút copy-code có `aria-label`/tooltip tiếng Việt riêng ("Sao chép mã vào clipboard") thay vì để mặc định tiếng Anh.

**Rủi ro cần rà soát:**
- Rất nhiều link bỏ gạch chân mặc định, chỉ hiện khi hover:
  ```scss
  .series-card > a { text-decoration: none; }
  .series-card > a:hover { text-decoration: underline; }
  ```
  Lặp lại pattern này ở `.home-more-item a`, `.series-highlight h3 a`… Đây là rủi ro WCAG 1.4.1 (không chỉ dùng màu sắc để phân biệt link) — người dùng low-vision hoặc dùng bàn phím không có tín hiệu hover sẽ khó nhận biết đâu là link nếu chỉ dựa vào màu `#1d4ed8`.
- Text phụ (caption, eyebrow label, badge "Chương X/Y", instruction "Đọc nhanh/Đọc đủ") dùng đồng loạt `var(--bs-secondary-color)` — cần đo tương phản thực tế so với nền, vì đây không chỉ là text trang trí mà còn mang thông tin điều hướng quan trọng (progress badge).
- 12 khối `listing` roadmap + 2 listing ở `/bai-hoc/index.qmd` đều có phần tử fallback rỗng gắn với text `"Không có bài phù hợp"` (định nghĩa trong `language.listing-page-no-matches`). Về mặt hiển thị bình thường các phần tử này nên bị ẩn (`display:none`) khi danh sách có dữ liệu, nhưng **nên xác nhận** chúng có `aria-hidden`/ẩn đúng cách để tránh trình đọc màn hình đọc nhầm "Không có bài phù hợp" ngay sau một bảng có đầy đủ nội dung.

### 1.7 Tổng hợp điểm tốt / điểm yếu — trang bài học

| Đang tốt | Đang yếu | Nguyên nhân gốc |
|---|---|---|
| Search, breadcrumb, prev/next, reader-mode bật sẵn | Không có tín hiệu "vị trí hiện tại" ở trang tổng quan mỗi chuỗi | Regex bỏ qua trong `lesson-progress.html` |
| SVG có alt/title/role đầy đủ | Biểu đồ sai màu nền khi chuyển dark mode thủ công | SVG dùng `prefers-color-scheme` thay vì theo class site |
| Front-matter schema nhất quán (order/series/group) | 2 chuỗi có "giọng" đọc khác hẳn nhau (callout vs không) | Viết bằng 2 quy trình khác nhau (markdown thuần vs HTML dán sẵn) |
| Có cơ chế "Đọc nhanh/Đọc đủ" | Không áp dụng nhất quán mọi bài | Chưa có template/partial dùng chung |
| max-width nội dung hợp lý cho đọc dài | Không có ước lượng thời gian đọc ở đa số bài | Chỉ 1 lesson tự khai báo thủ công |
| Không có quiz/self-check nào | | Chưa xây dựng |

---

## 2. Audit toàn bộ website

### 2.1 Homepage

`index.qmd` là hero tối giản: dòng chào + 2 nút CTA + panel "Cách đọc" + 2 series-card. **Điểm cộng:** homepage chủ động nói rõ giới hạn của chính nó — *"Homepage chỉ hiện chuỗi, không trộn từng chương"* — quản lý kỳ vọng người dùng tốt, tránh nhồi nhét. **Rủi ro mở rộng:** `.series-grid` cứng 2 cột trong CSS; nếu thêm chuỗi thứ 3 trong tương lai, layout 2 cột sẽ lệch (3 card trong lưới 2 cột) — cần rule `auto-fit`/`minmax` thay vì cột cố định.

### 2.2 Navigation / Header

Navbar có dropdown "Bài học" (Tất cả chuỗi / 2 chuỗi con), search bật (`search: true`) — **đây là search full-site thật, chạy client-side, không cần backend, tương thích 100% với GitHub Pages** — một điểm cộng lớn và đã đúng ràng buộc kỹ thuật của bạn (nhiều site tưởng cần Algolia mới có search, ở đây Quarto tự lo). Tools icon dẫn GitHub cá nhân.

### 2.3 Sidebar

2 sidebar `docked` tách biệt theo từng chuỗi (`collapse-level: 2`) — hợp lý cho 70+ trang Architecture Models, tránh dump toàn bộ cây lên màn hình cùng lúc. Nhưng nghĩa là **các chương con (6 mục dưới mỗi model) mặc định thu gọn**, người mới có thể không nhận ra có sub-chapters cho tới khi bấm vào model — nên có 1 dòng gợi ý ("mỗi model có N chương con") ở trang tổng quan chuỗi.

### 2.4 Footer

Rất tối giản: © + 2 link + icon GitHub. **Thiếu RSS** dù Quarto listing hỗ trợ sẵn `feed: true` gần như miễn phí về effort — đây là kênh "quay lại đọc tiếp" kinh điển cho một site tự mô tả là "đọc lại theo thứ tự", hiện đang hoàn toàn vắng mặt.

### 2.5 Information Architecture

Front-matter có schema nhất quán và **thực sự được dùng**, không chỉ trang trí: `order` điều khiển sidebar + roadmap listing; `categories` được nối vào bảng lọc `/bai-hoc/index.qmd` (`filter-ui: true`, `categories: true`); `series`/`group` phân nhóm rõ ràng. Đây là kỷ luật dữ liệu tốt hơn phần lớn Quarto blog cá nhân — nền tảng vững để làm thêm tính năng (progress, cross-link) mà không cần đổi cấu trúc.

### 2.6 Search & Discovery

Xác nhận có: (1) search built-in toàn site, đã localize tiếng Việt đầy đủ trong `_quarto.yml` (`search.placeholder: "Tìm kiếm bài học..."` …); (2) trang `/bai-hoc/index.qmd` có 2 listing — grid chọn chuỗi + bảng filter/sort toàn bộ chương theo `order`/`series`/`categories`. **Điểm yếu:** search không có facet theo chuỗi (không lọc được "chỉ tìm trong Architecture Models"), và không có gợi ý nội dung liên quan cross-series (xem 2.7).

### 2.7 Consistency giữa các trang/component — vấn đề lớn nhất của site

Bằng chứng trực tiếp: `ai-optimize/lesson-02-onnx-fundamentals.qmd` chứa 22 khối `<div class="callout ...">` HTML thô dán sẵn (khả năng cao được render 1 lần rồi paste ngược vào `.qmd`), trong khi các trang `architecture-models` được viết bằng cú pháp Quarto thuần (`::: {#fig-id}`, `$$...$$`). Hệ quả cụ thể:
- Muốn đổi style callout toàn site (màu, icon, spacing) → phải sửa tay HTML lặp lại trong từng file `ai-optimize/*.qmd` thay vì chỉ sửa 1 chỗ trong `custom.scss`.
- "Edit this page" (link GitHub tự động của Quarto) dẫn contributor tới các block HTML dài dòng, khó đọc/khó sửa hơn nhiều so với markdown gốc — cản trở đúng thứ mà `repo-actions: [edit, issue]` được bật ra để khuyến khích.
- Trải nghiệm đọc không đồng nhất giữa 2 chuỗi dù cùng domain, cùng nav, cùng author.

### 2.8 Onboarding & hành trình người dùng

Luồng hiện tại: Trang chủ → `/bai-hoc/` (chọn chuỗi) → trang tổng quan chuỗi (roadmap + nút "Bắt đầu X →") → lesson 1 → prev/next theo sidebar → … → lesson cuối.

**Khoảng trống rõ:**
- **Không có trạng thái "hoàn thành".** Tới lesson cuối cùng của một chuỗi, nút "next" chỉ dừng lại (hoặc không xuất hiện) — không có trang tổng kết, không gợi ý "đã xong Architecture Models, thử AI Optimization?", dù về nội dung 2 chuỗi có liên hệ tự nhiên (Transformer → LLM serving).
- **Không có gì được lưu giữa các lần ghé thăm.** Badge "Chương X/Y" chỉ phản ánh *vị trí trên sidebar tại trang hiện tại*, không phải *đã đọc bao nhiêu trong tổng thể*. Một người quay lại sau 1 tuần không có cách nào tự nhận ra "mình đọc tới đâu rồi" ngoài trí nhớ cá nhân — trong khi `about.qmd` xác định rõ mục đích site là *"đăng chuỗi bài học để đọc lại theo thứ tự"* — đây chính là use-case chính của site nhưng chưa được hỗ trợ bằng công cụ.
- **Không RSS** → không có kênh passive để biết site có bài mới (xem 2.4).

### 2.9 Performance

- Google Fonts load qua `preconnect` trước khi gọi stylesheet — đúng best practice, giảm round-trip.
- Site tĩnh trên GitHub Pages, ảnh minh họa là SVG viết tay (nhẹ) thay vì ảnh chụp màn hình raster — tốt cho tải trang.
- Không phát hiện thư viện JS nặng nào ngoài 1 script inline nhỏ (`lesson-progress.html`).
- **Giới hạn của audit:** không đo được LCP/CLS/TBT thực tế vì không chạy được Lighthouse trong phạm vi audit này — khuyến nghị chạy `lighthouse` hoặc PageSpeed Insights thực tế để có con số, nhưng dựa trên cấu trúc mã nguồn, rủi ro performance là **thấp**.

### 2.10 Accessibility (cấp site)

`reader-mode: true` là một tính năng Quarto tốt và ít site tận dụng — cho phép ẩn sidebar/TOC để đọc tập trung, hữu ích đặc biệt cho các lesson dài 10.000 từ. Các rủi ro khác đã liệt kê ở mục 1.6 áp dụng toàn site (không riêng trang lesson) vì đến từ `custom.scss` dùng chung.

---

## 3. Đề xuất nâng cấp

Mỗi đề xuất theo format: **Vấn đề → Nguyên nhân → Giải pháp (Quarto/SCSS/JS) → Lợi ích → Priority (Impact/Effort)**.

### 🟢 Quick wins (giờ–vài ngày, không đổi kiến trúc)

**QW1 — Sửa biểu đồ sai màu nền khi đổi dark mode thủ công**
- *Vấn đề:* SVG dùng `prefers-color-scheme` (OS-level) trong khi site chuyển theme bằng nút bấm (site-level) → 2 cơ chế lệch nhau.
- *Nguyên nhân:* SVG tự quyết định màu nền độc lập với theme của trang chứa nó.
- *Giải pháp:* Bỏ background cứng trong `custom.scss`, để container theo biến theme của Bootstrap (tự đổi theo `cosmo`/`darkly`):
  ```scss
  // Thay vì:
  // main img { background: #f7f8fa; }
  main img { background: var(--bs-tertiary-bg); }
  ```
  Về lâu dài (xem MT-lớn) nên bỏ hẳn `rect.fig-bg` + media query trong SVG, để SVG nền trong suốt, giao toàn bộ việc tô nền cho CSS của trang — 1 nguồn sự thật duy nhất về màu nền theo theme.
- *Lợi ích:* Xoá ngay hiện tượng "khung xám lạc màu" giữa trang tối/sáng — sửa 1 dòng CSS, không đụng tới nội dung `.qmd`.
- *Priority:* **P0 — Impact cao / Effort rất thấp.**

**QW2 — Bật RSS cho listing bài học**
- *Vấn đề:* Không có kênh "quay lại học" thụ động.
- *Nguyên nhân:* Chưa bật, dù Quarto hỗ trợ sẵn.
- *Giải pháp:* Thêm vào listing ở `bai-hoc/index.qmd`:
  ```yaml
  listing:
    - id: danh-sach-bai
      feed: true
      ...
  ```
  và thêm `<link rel="alternate" type="application/rss+xml">` (Quarto tự sinh khi `feed: true`).
- *Lợi ích:* Người học có thể theo dõi bài mới qua RSS reader mà không cần quay lại site thủ công.
- *Priority:* **P0 — Impact trung bình-cao / Effort rất thấp.**

**QW3 — Bọc bảng dài để tránh vỡ layout mobile**
- *Vấn đề:* Bảng nhiều cột (roadmap, "Lộ trình bài học") không có wrapper responsive.
- *Giải pháp:* thêm vào `custom.scss`:
  ```scss
  @media (max-width: 576px) {
    #quarto-document-content table {
      display: block;
      overflow-x: auto;
      white-space: nowrap;
    }
  }
  ```
- *Lợi ích:* Bảng scroll ngang gọn thay vì vỡ chữ/tràn trang trên điện thoại.
- *Priority:* **P0 — Impact trung bình / Effort thấp.**

**QW4 — Khôi phục tín hiệu link không chỉ dựa vào màu**
- *Vấn đề:* Nhiều link bỏ gạch chân mặc định (`text-decoration: none`), chỉ hiện khi hover — rủi ro WCAG 1.4.1.
- *Giải pháp:* giữ `text-decoration:none` cho card/heading link nhưng thêm chỉ báo phụ khi có `:focus-visible`, và cân nhắc giữ underline mặc định cho link trong đoạn văn (prose), chỉ bỏ ở heading/card:
  ```scss
  .series-card > a:focus-visible,
  .home-more-item a:focus-visible {
    outline: 2px solid var(--bs-primary);
    outline-offset: 2px;
  }
  ```
- *Lợi ích:* Đảm bảo người dùng bàn phím/low-vision vẫn nhận diện được link.
- *Priority:* **P1 — Impact trung bình / Effort thấp.**

**QW5 — Thêm badge cho trang tổng quan chuỗi**
- *Vấn đề:* `lesson-progress.html` chủ động `return` sớm khi gặp trang "Tổng quan chuỗi" → trang đầu tiên người mới thấy lại không có tín hiệu định hướng nào.
- *Giải pháp:* sửa nhánh xử lý overview đã có sẵn trong script (nó đã tính `nested.length` — chỉ cần bỏ điều kiện early-return và luôn hiển thị dòng `"Tổng quan · N chương"`).
- *Lợi ích:* Nhất quán trải nghiệm "bạn đang ở đâu" ngay từ trang đầu tiên.
- *Priority:* **P1 — Impact trung bình / Effort rất thấp (sửa vài dòng JS có sẵn).**

**QW6 — Xác minh & vá listing GRU thiếu order 3**
- *Vấn đề:* Bảng roadmap GRU đọc được thiếu dòng order=3 dù front-matter đúng.
- *Giải pháp:* `quarto render` lại cục bộ, kiểm tra `_site/bai-hoc/architecture-models/index.html` bằng mắt; nếu lỗi thật, kiểm tra cache `.quarto/` hoặc listing `contents: "GRU/*.qmd"` có bị glob loại trừ nhầm không.
- *Priority:* **P1 — Impact thấp (1 bảng) nhưng Effort rất thấp, ảnh hưởng niềm tin vào lộ trình đọc.**

---

### 🟡 Cải tiến trung hạn (vài tuần, vẫn thuần Quarto/JS/SCSS)

**MT1 — Chuẩn hoá callout: chuyển HTML thô sang shortcode Quarto**
- *Vấn đề:* 2 chuỗi được viết bằng 2 cú pháp khác nhau (xem 2.7).
- *Giải pháp:* Từng file trong `ai-optimize/`, thay:
  ```html
  <div class="callout callout-style-default callout-note ...">...Mục tiêu bài học...</div>
  ```
  bằng:
  ```markdown
  ::: {.callout-note title="Mục tiêu bài học"}
  Nội dung mục tiêu...
  :::
  ```
  Có thể làm dần từng lesson, không cần "big bang".
- *Lợi ích:* Dễ sửa qua "Edit this page", dễ đổi style toàn site từ 1 chỗ, giảm rủi ro lệch HTML khi Quarto/Bootstrap nâng version.
- *Priority:* **P1 — Impact trung bình / Effort trung bình (editorial, không kỹ thuật khó).**

**MT2 — Partial dùng chung cho khung mở đầu bài học**
- *Vấn đề:* "Mục tiêu bài học"/"Đọc nhanh-Đọc đủ" chỉ có ở một số bài, không đồng bộ.
- *Giải pháp:* Dùng include của Quarto để tái sử dụng:
  ```markdown
  {{< include /_partials/reading-modes.md >}}
  ```
  và một partial mẫu chuẩn cho mọi lesson mới, đảm bảo mọi bài — dù chuỗi nào — đều có cùng khung mở đầu.
- *Lợi ích:* Giải quyết đồng thời vấn đề nhất quán (2.7) và thiếu progressive disclosure (1.2) bằng 1 cơ chế.
- *Priority:* **P1 — Impact cao / Effort trung bình.**

**MT3 — Progress đọc lưu bằng localStorage (không cần backend)**
- *Vấn đề:* Không gì được ghi nhớ giữa các lần ghé thăm (2.8).
- *Giải pháp:* mở rộng `lesson-progress.html` sẵn có:
  ```js
  const key = 'read:' + location.pathname;
  localStorage.setItem(key, '1');
  document.querySelectorAll('.sidebar-link').forEach(a => {
    if (localStorage.getItem('read:' + new URL(a.href).pathname)) {
      a.classList.add('is-read'); // CSS: dấu ✓ nhỏ hoặc đổi màu nhạt
    }
  });
  ```
  Thuần client-side, không backend, không vi phạm ràng buộc GitHub Pages.
- *Lợi ích:* Người học quay lại sau nhiều ngày thấy ngay đã đọc tới đâu — giải quyết đúng use-case chính mà `about.qmd` mô tả.
- *Priority:* **P0/P1 — Impact rất cao / Effort trung bình.**

**MT4 — Cross-link nội dung liên quan giữa 2 chuỗi**
- *Vấn đề:* Transformer (Architecture Models) và LLM Inference (AI Optimization) không tham chiếu nhau dù liền mạch về kiến thức.
- *Giải pháp:* thêm callout "Xem thêm" cuối các trang liên quan, ví dụ cuối `Transformer/multi-head.qmd`:
  ```markdown
  ::: {.callout-tip title="Học tiếp"}
  Khi Multi-Head Attention chạy ở production scale, xem [KV cache & continuous batching](/bai-hoc/ai-optimize/lesson-09-llm-inference-systems.qmd).
  :::
  ```
- *Lợi ích:* Biến 2 "silo" nội dung thành một đồ thị kiến thức có định hướng, tăng thời gian đọc & giá trị sư phạm.
- *Priority:* **P2 — Impact trung bình-cao / Effort thấp-trung bình (chủ yếu editorial).**

**MT5 — Ước lượng thời gian đọc tự động**
- *Vấn đề:* Chỉ 1 lesson tự khai báo thời lượng; phần còn lại không ai biết trước độ dài.
- *Giải pháp:* thêm vào script include-after-body, đếm từ trong `#quarto-document-content` và chèn cạnh badge "Chương X/Y":
  ```js
  const words = document.querySelector('#quarto-document-content').innerText.trim().split(/\s+/).length;
  const mins = Math.max(1, Math.round(words / 180)); // ~180 từ/phút tiếng Việt kỹ thuật
  badge.textContent += ` · ~${mins} phút đọc`;
  ```
- *Lợi ích:* Người học tự quyết định "đọc ngay" hay "để dành" dựa trên thời gian có sẵn — đặc biệt quan trọng khi độ dài bài chênh nhau 3.6 lần (1.2).
- *Priority:* **P1 — Impact trung bình-cao / Effort thấp.**

**MT6 — Self-check cuối bài bằng `<details>` thuần HTML**
- *Vấn đề:* Không có cơ chế kiểm tra hiểu bài nào trên toàn site.
- *Giải pháp:* thêm khối chuẩn cuối mỗi lesson, không cần JS phức tạp:
  ```markdown
  ::: {.callout-note title="Kiểm tra nhanh"}
  <details><summary>Vì sao AlexNet dùng stride 4 ở Conv1?</summary>
  Để giảm mạnh kích thước không gian ngay từ đầu, phù hợp giới hạn bộ nhớ GPU năm 2012.
  </details>
  :::
  ```
  Có thể nâng cấp dần thành mini-quiz JS thuần (không framework) nếu muốn tương tác hơn.
- *Lợi ích:* Tăng khả năng ghi nhớ, biến trang từ "tài liệu để đọc" thành "bài học để học".
- *Priority:* **P2 — Impact trung bình / Effort trung bình (cần viết câu hỏi cho 70+ trang).**

---

### 🔴 Cải tiến lớn / dài hạn (nhiều tuần, vẫn trong khuôn khổ Quarto)

**LT1 — Trang/khoảnh khắc "hoàn thành chuỗi"**
- *Vấn đề:* Không có điểm kết thúc rõ ràng, không gợi ý bước tiếp theo (2.8).
- *Giải pháp:* Trang cuối mỗi chuỗi (`.../UNet/complete-unet.qmd`, `.../lesson-10-end-to-end-capstone.qmd`) thêm block "Bạn đã hoàn thành chuỗi X" + link chuỗi còn lại, kết hợp với trạng thái đã đọc từ `localStorage` (MT3) để hiển thị % hoàn thành thực tế, ví dụ "Bạn đã đọc 41/45 chương của Architecture Models".
- *Lợi ích:* Đóng vòng lặp "học xong → quay lại/học tiếp" — đúng như mục tiêu chính của site.
- *Priority:* **P1 (impact) / P2 (effort, phụ thuộc MT3 xong trước).**

**LT2 — Loại bỏ hẳn nền cứng trong SVG, chuẩn hoá theo `.light-content`/`.dark-content` của Quarto**
- *Vấn đề:* QW1 là bản vá tạm; về gốc rễ, SVG vẫn tự vẽ nền theo `prefers-color-scheme` — vẫn có thể lệch nếu sau này site đổi cách toggle theme.
- *Giải pháp:* Xuất mỗi diagram thành SVG nền trong suốt (bỏ hẳn `rect.fig-bg` + media query), rồi để 100% CSS của site quyết định nền (biến `--bs-tertiary-bg`). Nếu cần 2 phiên bản màu chữ/đường nét khác nhau giữa light/dark, dùng đúng tính năng Quarto có sẵn:
  ```markdown
  ![Sơ đồ AlexNet](figures/01-pipeline-overview-light.svg){.light-content}
  ![Sơ đồ AlexNet](figures/01-pipeline-overview-dark.svg){.dark-content}
  ```
- *Lợi ích:* Một nguồn sự thật duy nhất về theme, không phụ thuộc OS, khớp 100% với site dù người dùng chuyển theme bao nhiêu lần.
- *Priority:* **P2 — Impact trung bình / Effort cao (phải xử lý lại toàn bộ ~70+ SVG).**

**LT3 — Chuẩn hoá độ dài bài học**
- *Vấn đề:* Chênh lệch 3.6 lần giữa các "chương" cùng cấp trong sidebar (1.2).
- *Giải pháp:* Rà soát các lesson AI Optimization dài (~10k từ), tách theo đúng pattern 6-chương/model đã áp dụng thành công ở Architecture Models (mỗi lesson dài chia thành 2–3 file `.qmd` con với `order` kế tiếp).
- *Lợi ích:* Trải nghiệm đọc dự đoán được, đồng nhất giữa 2 chuỗi, dễ ước lượng thời gian (hỗ trợ MT5).
- *Priority:* **P2 — Impact trung bình / Effort cao (editorial nặng, cần viết lại cấu trúc 10 lesson).**

**LT4 — Đưa kiểm tra accessibility/hiệu năng vào GitHub Actions**
- *Vấn đề:* Hiện không có cách nào tự động phát hiện regression về a11y/performance khi thêm bài mới.
- *Giải pháp:* Thêm step vào workflow deploy hiện có (không đổi hosting/kiến trúc):
  ```yaml
  - name: Lighthouse CI
    uses: treosh/lighthouse-ci-action@v11
    with:
      urls: |
        https://dythanh22.github.io/
        https://dythanh22.github.io/bai-hoc/architecture-models/
  ```
- *Lợi ích:* Giữ chất lượng UX không suy giảm khi site scale lên hàng trăm trang.
- *Priority:* **P2 — Impact dài hạn cao / Effort trung bình, không ảnh hưởng runtime của site.**

**LT5 — Trang "Design system" nội bộ**
- *Vấn đề:* Các class custom (`.eyebrow`, `.series-card`, `.reading-modes`, quy ước callout…) chỉ tồn tại trong đầu tác giả và rải rác trong `custom.scss`.
- *Giải pháp:* Một trang `.qmd` liệt kê toàn bộ pattern UI kèm ví dụ dùng, dùng làm "nguồn sự thật" khi viết bài mới hoặc nếu có người đóng góp qua "Edit this page".
- *Lợi ích:* Duy trì nhất quán khi nội dung tiếp tục scale, giảm phụ thuộc vào trí nhớ cá nhân của tác giả.
- *Priority:* **P3 — Impact trung bình dài hạn / Effort thấp-trung bình.**

---

## 4. Roadmap tổng hợp theo ưu tiên

| # | Hạng mục | Impact | Effort | Priority | Phụ thuộc |
|---|---|---|---|---|---|
| QW1 | Sửa nền SVG lệch dark mode | Cao | Rất thấp | **P0** | — |
| QW2 | Bật RSS | Trung bình–Cao | Rất thấp | **P0** | — |
| QW3 | Bảng responsive mobile | Trung bình | Thấp | **P0** | — |
| QW6 | Vá/xác minh listing GRU order 3 | Thấp | Rất thấp | **P1** | — |
| QW5 | Badge cho trang tổng quan chuỗi | Trung bình | Rất thấp | **P1** | — |
| QW4 | Chỉ báo link ngoài màu sắc | Trung bình | Thấp | **P1** | — |
| MT3 | Progress đọc qua localStorage | Rất cao | Trung bình | **P0/P1** | — |
| MT2 | Partial khung mở đầu bài học | Cao | Trung bình | **P1** | — |
| MT5 | Ước lượng thời gian đọc | Trung bình–Cao | Thấp | **P1** | — |
| MT1 | Chuẩn hoá callout → shortcode | Trung bình | Trung bình | **P1** | — |
| MT4 | Cross-link 2 chuỗi | Trung bình–Cao | Thấp–Trung bình | **P2** | — |
| MT6 | Self-check cuối bài | Trung bình | Trung bình | **P2** | MT2 (nên) |
| LT1 | Trang "hoàn thành chuỗi" | Cao | Trung bình | **P1/P2** | MT3 |
| LT4 | Lighthouse CI trong Actions | Cao (dài hạn) | Trung bình | **P2** | — |
| LT2 | Chuẩn hoá SVG theo `.light/.dark-content` | Trung bình | Cao | **P2** | QW1 |
| LT3 | Chuẩn hoá độ dài bài học | Trung bình | Cao | **P2** | — |
| LT5 | Trang design system | Trung bình (dài hạn) | Thấp–Trung bình | **P3** | — |

**Gợi ý trình tự triển khai thực tế:**
1. **Tuần 1:** QW1, QW2, QW3, QW5, QW6 (toàn bộ CSS/YAML/JS nhỏ, có thể làm trong 1 buổi).
2. **Tuần 2–4:** MT3 (progress localStorage) + MT5 (thời gian đọc) — cùng chạm vào `lesson-progress.html`, nên làm chung một đợt.
3. **Tháng 2:** MT2 (partial mở đầu) + MT1 (chuẩn hoá callout) — dọn nợ kỹ thuật nội dung, làm nền cho LT3 sau này.
4. **Tháng 2–3:** MT4 (cross-link), LT1 (trang hoàn thành chuỗi, phụ thuộc MT3 đã xong).
5. **Khi có thời gian rảnh dài hơi:** LT2, LT3, LT4, LT5.

---

## 5. Giới hạn của audit này

Audit được thực hiện qua đọc trực tiếp mã nguồn (`_quarto.yml`, `.scss`, `.js`, nhiều file `.qmd` đại diện) thay vì render trực tiếp trong trình duyệt/công cụ đo (Lighthouse, axe, ảnh chụp responsive thật). Các kết luận về **hành vi/logic** (route dark-mode, listing config, JS progress) có độ tin cậy cao vì đọc thẳng từ code. Các kết luận về **hiển thị trực quan cuối cùng** (độ tương phản chính xác, bảng có vỡ layout mobile hay không, MathJax tràn dòng hay không) được đánh dấu rõ là "cần kiểm tra trực quan" và nên xác nhận bằng DevTools responsive mode + Lighthouse/axe DevTools trước khi coi là kết luận cuối cùng.
