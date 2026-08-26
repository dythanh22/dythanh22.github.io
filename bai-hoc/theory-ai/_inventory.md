# Theory AI — Inventory (Pha 1)

**Trạng thái:** đóng pha 1 — sẵn sàng làm pha 2 (tooling), **chưa** rename/convert file.
**Nguồn máy:** `_inventory.csv` (187 dòng, cùng thư mục).
**Ngày:** 2026-08-26

---

## 0. Tóm tắt

| Metric | Giá trị |
|---|---|
| Chapters | 15 |
| Bài `.md` | 187 |
| Slug trùng trong chapter | 0 |
| File MUST_FIX tên | 6 |
| SVG ≈ bài (hầu hết 1:1) | có; xem §3 |

**Quyết định order:** sắp **sư phạm trong từng chapter**, không theo ID nguồn (`59`, `143`, …). `source_id` giữ trong CSV để truy vết.

**Quyết định slug:** ASCII `a-z0-9-`; bỏ tiền tố `implement-`/`compute-` khi rút gọn; file truncated/hỏng dùng slug tường minh (vd. `gelu-activation`, `bleu-score`).

---

## 1. Map `group` / `categories` (đóng băng)

| Chapter folder | `group` | `categories` | Mô tả ngắn |
|---|---|---|---|
| `01-probability` | `probability` | `['theory-ai', 'probability']` | Phân phối rời rạc & bootstrap CI (5 bài) |
| `02-statistics` | `statistics` | `['theory-ai', 'statistics']` | Mô tả, tương quan, kiểm định (7 bài) |
| `03-linear-algebra` | `linear-algebra` | `['theory-ai', 'linear-algebra']` | Khoảng cách, chuẩn, ma trận, biến đổi (12 bài) |
| `04-features` | `features` | `['theory-ai', 'features']` | Scale, encode, feature eng, split (20 bài) |
| `05-classical-ml` | `classical-ml` | `['theory-ai', 'classical-ml']` | Hồi quy, cây, clustering, PCA, NB (11 bài) |
| `06-metrics` | `metrics` | `['theory-ai', 'metrics']` | Classification, ranking, calibration (13 bài) |
| `07-activations-losses` | `activations-losses` | `['theory-ai', 'activations-losses']` | Hàm kích hoạt và hàm mất mát (20 bài) |
| `08-optimizers` | `optimizers` | `['theory-ai', 'optimizers']` | Adaptive opts, clip, LR schedule (12 bài) |
| `09-deep-learning` | `deep-learning` | `['theory-ai', 'deep-learning']` | Layer, init, pool, RNN, attention primitives (16 bài) |
| `10-computer-vision` | `computer-vision` | `['theory-ai', 'computer-vision']` | Xử lý ảnh → detection primitives (13 bài) |
| `11-nlp` | `nlp` | `['theory-ai', 'nlp']` | BoW → ranking → evaluation (10 bài) |
| `12-reinforcement-learning` | `reinforcement-learning` | `['theory-ai', 'reinforcement-learning']` | Returns → TD/Q → policy gradient (12 bài) |
| `13-time-series` | `time-series` | `['theory-ai', 'time-series']` | Lag, smoothing, seasonal (13 bài) |
| `14-recommender` | `recommender` | `['theory-ai', 'recommender']` | CF, MF, ranking metrics (13 bài) |
| `15-mlops` | `mlops` | `['theory-ai', 'mlops']` | ETL → drift → deploy/retrain (10 bài) |

YAML tối thiểu mỗi bài (pha 2 sẽ chèn):

```yaml
---
title: "…"
date: 2026-08-26
order: N
categories: [theory-ai, <group>]
series: theory-ai
group: <group>
description: "…"
---
```

Sidebar sections (pha 3+): nhãn hiển thị dùng cột label (`1. Probability`, …).

---

## 2. MUST_FIX — tên file (100% danh sách)

Bắt buộc xử lý khi rename ở pha 2/3 (không để path có `...` / ngoặc lệch / thiếu dấu chấm):

| path cũ | issues | slug đích | title YAML |
|---|---|---|---|
| `01-probability/61. Poisson Probability Mass Function & Cumulative...md` | truncated;ampersand;spaces | `poisson-pmf-cdf` | PMF & CDF Poisson |
| `01-probability/83_Bootstrap-Mean-Confidence-Interval.md` | underscore-id | `bootstrap-mean-ci` | Bootstrap: trung bình và khoảng tin cậy |
| `06-metrics/30. Implement R² Score (Coefficient of Determinati...md` | truncated;unbalanced-paren;special-char;spaces | `r2-score` | R² Score (hệ số xác định) |
| `06-metrics/116. NDCG (Normalized Discounted Cumulative Gain.md` | unbalanced-paren;spaces | `ndcg` | NDCG (Normalized Discounted Cumulative Gain) |
| `07-activations-losses/35. Implement GELU Activation (Gaussian Error Line...md` | truncated;unbalanced-paren;spaces | `gelu-activation` | GELU Activation |
| `11-nlp/157 BLUE Score.md` | missing-dot-after-id;spaces | `bleu-score` | BLEU Score |

Các file còn lại hầu hết chỉ có `spaces` (và đôi khi `ampersand`/`special-char`) — xử lý hàng loạt bằng slug, không cần case đặc biệt.

---

## 3. Ghi chú nội dung / asset (không chặn pha 1)

| Mục | Chi tiết | Khi xử lý |
|---|---|---|
| `02-statistics/67…t-Test.md` | `src` hình bị lỗi paste: chuỗi `figures/![67-…](figures/67-…)67-…svg` trước thẻ `<img>` đúng | Pha 2/3: sửa thành `figures/67-t-statistic.svg` |
| `13-time-series` orphan SVG | `189-holt-des.svg`, `191-seasonal-average.svg` — bài đang trỏ `189-holt.svg` / `191-seasonal-avg.svg` | Pha 2: xác nhận; không xóa orphan trừ khi chắc dư |
| `05-classical-ml` / Expected Value | Taxonomy lệch → probability | Pha 6: move + `aliases` |
| `04-features` Min-Max ×2 | `min-max-normalization` vs `min-max-scaling` | Giữ cả hai; description phân biệt |

---

## 4. Inventory theo chapter

Cột `#` = `order` đề xuất trong chapter (→ front-matter).

### 01-probability — Probability

*group:* `probability` · *categories:* `['theory-ai', 'probability']` · *Phân phối rời rạc & bootstrap CI*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `bernoulli-pmf-moments` | PMF Bernoulli và các moment | 1 |  |
| 2 | `binomial-pmf` | PMF nhị thức (Binomial) | 1 |  |
| 3 | `geometric-pmf-mean` | PMF hình học (Geometric) và kỳ vọng | 1 |  |
| 4 | `poisson-pmf-cdf` | PMF & CDF Poisson | 1 | MUST_FIX filename |
| 5 | `bootstrap-mean-ci` | Bootstrap: trung bình và khoảng tin cậy | 1 | MUST_FIX filename |

### 02-statistics — Statistics

*group:* `statistics` · *categories:* `['theory-ai', 'statistics']` · *Mô tả, tương quan, kiểm định*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `mean-median-mode` | Mean, Median, Mode | 1 |  |
| 2 | `sample-variance-and-standard-deviation` | Phương sai mẫu & độ lệch chuẩn | 1 |  |
| 3 | `percentiles-quantiles` | Percentile / Quantile | 1 |  |
| 4 | `pearson-correlation-matrix` | Ma trận tương quan Pearson | 1 |  |
| 5 | `silhouette-score` | Điểm silhouette | 1 |  |
| 6 | `chi-square-test` | Kiểm định Chi-Square | 1 |  |
| 7 | `one-sample-t-test` | Kiểm định t một mẫu | 2 |  |

### 03-linear-algebra — Linear Algebra

*group:* `linear-algebra` · *categories:* `['theory-ai', 'linear-algebra']` · *Khoảng cách, chuẩn, ma trận, biến đổi*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `manhattan-distance` | Manhattan Distance | 1 |  |
| 2 | `euclidean-distance` | Euclidean Distance | 1 |  |
| 3 | `3d-vector-norm` | Norm vector 3D | 1 |  |
| 4 | `normalize-3d-vectors` | Chuẩn hóa vector 3D | 1 |  |
| 5 | `angle-between-3d-vectors` | Góc giữa hai vector 3D | 1 |  |
| 6 | `cosine-similarity` | Cosine Similarity | 1 |  |
| 7 | `matrix-normalization` | Chuẩn hóa ma trận | 1 |  |
| 8 | `make-diagonal-matrix` | Ma trận đường chéo | 1 |  |
| 9 | `matrix-inverse` | Nghịch đảo ma trận | 1 |  |
| 10 | `calculate-eigenvalues-of-a-matrix` | Trị riêng của ma trận | 1 |  |
| 11 | `apply-4x4-homogeneous-transform` | Áp dụng biến đổi đồng nhất 4×4 | 1 |  |
| 12 | `rotate-3d-point-around-z-axis` | Quay điểm 3D quanh trục Z | 1 |  |

### 04-features — Features

*group:* `features` · *categories:* `['theory-ai', 'features']` · *Scale, encode, feature eng, split*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `min-max-normalization` | Min-Max Normalization | 1 | gần với min-max-scaling (185) — giữ cả hai; phân biệt normalization vs scaling trong description |
| 2 | `min-max-scaling` | Min-Max Scaling | 1 | xem note ở min-max-normalization |
| 3 | `z-score-standardization` | z-Score Standardization | 1 |  |
| 4 | `robust-scaling` | Robust Scaling | 1 |  |
| 5 | `rank-transform` | Rank Transform | 1 |  |
| 6 | `log-transform` | Log Transform | 1 |  |
| 7 | `winsorization` | Winsorization | 1 |  |
| 8 | `streaming-min-max-normalization` | Streaming Min-Max Normalization | 1 |  |
| 9 | `impute-missing-values` | Impute Missing Values (mean/median) | 1 |  |
| 10 | `one-hot-encoding-multi-class` | One-Hot Encoding (đa lớp) | 1 |  |
| 11 | `ordinal-encoding` | Ordinal Encoding | 1 |  |
| 12 | `frequency-encoding` | Frequency Encoding | 1 |  |
| 13 | `target-encoding` | Target Encoding | 1 |  |
| 14 | `cyclic-encoding` | Cyclic Encoding | 1 |  |
| 15 | `polynomial-features` | Polynomial Features | 1 |  |
| 16 | `binning` | Binning | 1 |  |
| 17 | `interaction-features` | Interaction Features | 1 |  |
| 18 | `stratified-train-test-split` | Stratified Train/Test Split | 1 |  |
| 19 | `k-fold-split-indices-only` | K-Fold Split (chỉ chỉ số) | 1 |  |
| 20 | `batch-shuffling-and-mini-batch-generator` | Batch Shuffling & Mini-Batch Generator | 1 |  |

### 05-classical-ml — Classical ML

*group:* `classical-ml` · *categories:* `['theory-ai', 'classical-ml']` · *Hồi quy, cây, clustering, PCA, NB*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `linear-regression-closed-form` | Linear Regression dạng đóng | 1 |  |
| 2 | `ridge-regression` | Ridge Regression | 1 |  |
| 3 | `logistic-regression-training-loop` | Vòng lặp huấn luyện Logistic Regression | 1 |  |
| 4 | `entropy-for-a-node` | Entropy của một node | 1 |  |
| 5 | `decision-tree-best-split` | Chia tốt nhất Decision Tree | 1 |  |
| 6 | `random-forest-majority-vote` | Bình chọn đa số Random Forest | 1 |  |
| 7 | `k-means-assignment-step` | Bước gán cụm K-Means | 1 |  |
| 8 | `k-means-centroid-update` | Bước cập nhật centroid K-Means | 1 |  |
| 9 | `pca-projection` | Chiếu PCA | 1 |  |
| 10 | `gaussian-naive-bayes` | Gaussian Naive Bayes | 1 |  |
| 11 | `expected-value-discrete` | Kỳ vọng (phân phối rời rạc) | 1 | taxonomy: gần probability hơn classical-ml — giữ nguyên folder pha 1; move+aliases ở pha 6 |

### 06-metrics — Metrics

*group:* `metrics` · *categories:* `['theory-ai', 'metrics']` · *Classification, ranking, calibration*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `accuracy-precision-recall-f1` | Accuracy, Precision, Recall, F1 | 1 |  |
| 2 | `micro-f1` | Micro-F1 | 1 |  |
| 3 | `cross-entropy-loss` | Cross-Entropy Loss | 1 |  |
| 4 | `log-loss-per-sample` | Log Loss (từng mẫu) | 1 |  |
| 5 | `mean-squared-error-mse` | Mean Squared Error (MSE) | 1 |  |
| 6 | `r2-score` | R² Score (hệ số xác định) | 1 | MUST_FIX filename |
| 7 | `roc-curve-from-scores` | Đường ROC từ score | 1 |  |
| 8 | `auc-area-under-roc` | AUC (diện tích dưới ROC) | 1 |  |
| 9 | `precision-and-recall-at-k` | Precision và Recall at K | 1 |  |
| 10 | `ndcg` | NDCG (Normalized Discounted Cumulative Gain) | 1 | MUST_FIX filename |
| 11 | `cohens-kappa` | Cohen's Kappa | 1 |  |
| 12 | `expected-calibration-error` | Expected Calibration Error | 1 |  |
| 13 | `isotonic-regression-calibration` | Isotonic Regression Calibration | 1 |  |

### 07-activations-losses — Activations & Losses

*group:* `activations-losses` · *categories:* `['theory-ai', 'activations-losses']` · *Hàm kích hoạt và hàm mất mát*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `relu-activation` | ReLU Activation | 1 |  |
| 2 | `leaky-relu` | Leaky ReLU (với α) | 1 |  |
| 3 | `tanh-activation` | Tanh Activation | 1 |  |
| 4 | `softmax-function` | Softmax | 1 |  |
| 5 | `gelu-activation` | GELU Activation | 1 | MUST_FIX filename |
| 6 | `swish-activation` | Swish Activation | 1 |  |
| 7 | `elu-activation` | ELU Activation | 1 |  |
| 8 | `selu-activation` | SELU Activation | 1 |  |
| 9 | `hinge-loss-binary-svm` | Hinge Loss (SVM nhị phân) | 1 |  |
| 10 | `huber-loss` | Huber Loss | 1 |  |
| 11 | `contrastive-loss-siamese` | Contrastive Loss (Siamese) | 1 |  |
| 12 | `triplet-loss` | Triplet Loss | 1 |  |
| 13 | `infonce-loss` | InfoNCE Loss | 1 |  |
| 14 | `focal-loss` | Focal Loss | 1 |  |
| 15 | `binary-focal-loss` | Binary Focal Loss | 1 |  |
| 16 | `dice-loss` | Dice Loss | 1 |  |
| 17 | `kl-divergence` | KL Divergence | 1 |  |
| 18 | `wasserstein-critic-loss` | Wasserstein Critic Loss | 1 |  |
| 19 | `label-smoothing-loss` | Label Smoothing Loss | 1 |  |
| 20 | `cosine-embedding-loss` | Cosine Embedding Loss | 1 |  |

### 08-optimizers — Optimizers

*group:* `optimizers` · *categories:* `['theory-ai', 'optimizers']` · *Adaptive opts, clip, LR schedule*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `adagrad-optimizer` | AdaGrad Optimizer | 1 |  |
| 2 | `rmsprop-optimizer-single-update-step` | RMSProp Optimizer | 1 |  |
| 3 | `adadelta-update-step` | AdaDelta Update Step | 1 |  |
| 4 | `nesterov-momentum-nag` | Nesterov Momentum (NAG) | 1 |  |
| 5 | `adam-optimizer-step` | Adam Optimizer Step | 1 |  |
| 6 | `adamw-decoupled-weight-decay` | AdamW (Decoupled Weight Decay) | 1 |  |
| 7 | `nadam-nesterov-plus-adam` | Nadam (Nesterov + Adam) | 1 |  |
| 8 | `gradient-clipping-global-norm` | Gradient Clipping (Global Norm) | 1 |  |
| 9 | `learning-rate-scheduler-linear-decay` | Learning Rate Scheduler (Linear Decay) | 1 |  |
| 10 | `warmup-plus-linear-decay-lr-schedule` | Warmup + Linear Decay LR Schedule | 1 |  |
| 11 | `cosine-annealing-lr-scheduler` | Cosine Annealing LR Scheduler | 1 |  |
| 12 | `l-bfgs-two-loop-recursion` | L-BFGS Two-Loop Recursion | 1 |  |

### 09-deep-learning — Deep Learning

*group:* `deep-learning` · *categories:* `['theory-ai', 'deep-learning']` · *Layer, init, pool, RNN, attention primitives*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `linear-layer-forward` | Linear Layer Forward | 1 |  |
| 2 | `xavier-initialization` | Xavier Initialization | 1 |  |
| 3 | `he-initialization` | He Initialization | 1 |  |
| 4 | `dropout-training-mode` | Dropout (chế độ huấn luyện) | 1 |  |
| 5 | `batch-normalization-forward` | Batch Normalization (Forward) | 1 |  |
| 6 | `max-pooling-forward` | Max Pooling Forward | 1 |  |
| 7 | `max-pooling-2d` | Max Pooling 2D | 1 |  |
| 8 | `average-pooling-2d` | Average Pooling 2D | 1 |  |
| 9 | `global-average-pooling` | Global Average Pooling | 1 |  |
| 10 | `a-simple-cnn-layer-numpy` | CNN Layer (NumPy) | 1 |  |
| 11 | `pad-sequences` | Pad Sequences | 1 |  |
| 12 | `rnn-step-forward-tanh-cell` | RNN Step Forward (Tanh Cell) | 1 |  |
| 13 | `rnn-step-backward-vanilla-rnn` | RNN Step Backward (Vanilla RNN) | 1 |  |
| 14 | `build-a-mini-gru-cell-forward-pass` | Mini GRU Cell (forward) | 1 |  |
| 15 | `positional-encoding` | Positional Encoding (sin/cos) | 1 |  |
| 16 | `causal-masking-for-attention` | Causal Masking cho Attention | 1 |  |

### 10-computer-vision — Computer Vision

*group:* `computer-vision` · *categories:* `['theory-ai', 'computer-vision']` · *Xử lý ảnh → detection primitives*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `color-to-grayscale` | Color to Grayscale | 1 |  |
| 2 | `image-histogram` | Image Histogram | 1 |  |
| 3 | `histogram-equalization` | Histogram Equalization | 1 |  |
| 4 | `gaussian-blur-kernel` | Gaussian Blur Kernel | 1 |  |
| 5 | `sobel-edge-detection` | Sobel Edge Detection | 1 |  |
| 6 | `morphological-erosion-and-dilation` | Morphological Erosion and Dilation | 1 |  |
| 7 | `image-rotation-nearest-neighbor` | Image Rotation (Nearest Neighbor) | 1 |  |
| 8 | `bilinear-interpolation` | Bilinear Interpolation | 1 |  |
| 9 | `2d-convolution-image-filtering` | 2D Convolution (lọc ảnh) | 1 |  |
| 10 | `anchor-box-generation` | Anchor Box Generation | 1 |  |
| 11 | `intersection-over-union-iou` | Intersection over Union (IoU) | 1 |  |
| 12 | `non-maximum-suppression` | Non-Maximum Suppression | 1 |  |
| 13 | `roi-pooling` | ROI Pooling | 1 |  |

### 11-nlp — NLP

*group:* `nlp` · *categories:* `['theory-ai', 'nlp']` · *BoW → ranking → evaluation*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `word-count-dictionary` | Word Count Dictionary | 1 |  |
| 2 | `remove-stopwords` | Remove Stopwords | 1 |  |
| 3 | `bag-of-words-vector` | Bag-of-Words Vector | 1 |  |
| 4 | `tf-idf-vectorizer` | TF-IDF Vectorizer | 1 |  |
| 5 | `bigram-probabilities-add-1-smoothing` | Bigram Probabilities (Add-1 Smoothing) | 1 |  |
| 6 | `bm25-ranking-score` | BM25 Ranking Score | 1 |  |
| 7 | `edit-distance` | Edit Distance | 1 |  |
| 8 | `text-chunking` | Text Chunking | 1 |  |
| 9 | `perplexity-computation` | Perplexity | 1 |  |
| 10 | `bleu-score` | BLEU Score | 1 | MUST_FIX filename |

### 12-reinforcement-learning — Reinforcement Learning

*group:* `reinforcement-learning` · *categories:* `['theory-ai', 'reinforcement-learning']` · *Returns → TD/Q → policy gradient*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `discounted-returns` | Discounted Returns | 1 |  |
| 2 | `value-iteration-step` | Value Iteration Step | 1 |  |
| 3 | `monte-carlo-policy-evaluation` | Monte Carlo Policy Evaluation | 1 |  |
| 4 | `one-step-td-value-update` | One-Step TD Value Update | 1 |  |
| 5 | `epsilon-greedy` | ε-Greedy Action Selection | 1 |  |
| 6 | `tabular-q-learning-single-update` | Tabular Q-Learning (Single Update) | 1 |  |
| 7 | `sarsa-update` | SARSA Update | 1 |  |
| 8 | `advantage-computation` | Advantage Computation | 1 |  |
| 9 | `generalized-advantage-estimation` | Generalized Advantage Estimation | 1 |  |
| 10 | `policy-gradient-loss` | Policy Gradient Loss | 1 |  |
| 11 | `replay-buffer-sample` | Replay Buffer Sample | 1 |  |
| 12 | `prioritized-experience-replay` | Prioritized Experience Replay | 1 |  |

### 13-time-series — Time Series

*group:* `time-series` · *categories:* `['theory-ai', 'time-series']` · *Lag, smoothing, seasonal*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `lag-features` | Lag Features | 1 |  |
| 2 | `differencing` | Differencing | 1 |  |
| 3 | `simple-moving-average` | Simple Moving Average | 1 |  |
| 4 | `weighted-moving-average` | Weighted Moving Average | 1 |  |
| 5 | `exponential-moving-average` | Exponential Moving Average | 1 |  |
| 6 | `rolling-standard-deviation` | Rolling Standard Deviation | 1 |  |
| 7 | `moving-median` | Moving Median | 1 |  |
| 8 | `percent-change` | Percent Change | 1 |  |
| 9 | `cumulative-returns` | Cumulative Returns | 1 |  |
| 10 | `seasonal-average` | Seasonal Average | 1 | SVG orphan liên quan: figures/191-seasonal-average.svg (kiểm tra ref pha 2) |
| 11 | `double-exponential-smoothing` | Double Exponential Smoothing | 1 | SVG orphan liên quan: figures/189-holt-des.svg (kiểm tra ref pha 2) |
| 12 | `autocorrelation` | Autocorrelation | 1 |  |
| 13 | `linear-interpolation` | Linear Interpolation | 1 |  |

### 14-recommender — Recommender

*group:* `recommender` · *categories:* `['theory-ai', 'recommender']` · *CF, MF, ranking metrics*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `mean-rating-imputation` | Mean Rating Imputation | 1 |  |
| 2 | `rating-normalization` | Rating Normalization | 1 |  |
| 3 | `popularity-ranking` | Popularity Ranking | 1 |  |
| 4 | `baseline-predictor` | Baseline Predictor | 1 |  |
| 5 | `jaccard-similarity` | Jaccard Similarity | 1 |  |
| 6 | `adjusted-cosine-similarity` | Adjusted Cosine Similarity | 1 |  |
| 7 | `user-based-cf-prediction` | User-Based CF Prediction | 1 |  |
| 8 | `item-based-cf-prediction` | Item-Based CF Prediction | 1 |  |
| 9 | `matrix-factorization-sgd-step` | Matrix Factorization SGD Step | 1 |  |
| 10 | `top-k-recommendations` | Top-K Recommendations | 1 |  |
| 11 | `hit-rate-at-k` | Hit Rate at K | 1 |  |
| 12 | `catalog-coverage` | Catalog Coverage | 1 |  |
| 13 | `novelty-score` | Novelty Score | 1 |  |

### 15-mlops — MLOps

*group:* `mlops` · *categories:* `['theory-ai', 'mlops']` · *ETL → drift → deploy/retrain*

| # | slug → `.qmd` | title | figs | notes |
|---:|---|---|---:|---|
| 1 | `etl-schema-validation` | ETL Schema Validation | 1 |  |
| 2 | `etl-deduplication` | ETL Deduplication | 1 |  |
| 3 | `etl-dependency-orchestration` | ETL Dependency Orchestration | 1 |  |
| 4 | `feature-store-lookup` | Feature Store Lookup | 1 |  |
| 5 | `detect-train-serving-skew` | Detect Train-Serving Skew | 1 |  |
| 6 | `data-drift-detection` | Data Drift Detection | 1 |  |
| 7 | `monitoring-metrics-selection` | Monitoring Metrics Selection | 1 |  |
| 8 | `model-versioning` | Model Versioning | 1 |  |
| 9 | `shadow-deployment-evaluation` | Shadow Deployment Evaluation | 1 |  |
| 10 | `retraining-trigger-design` | Retraining Trigger Design | 1 |  |

---

## 5. Verify pha 1

- [x] Đủ **187** dòng inventory (`_inventory.csv` + bảng trên).
- [x] **0** trùng slug trong cùng chapter.
- [x] Danh sách MUST_FIX tên đóng **6/6**.
- [x] Map `group`/`categories` 15 chapter đóng băng.
- [x] `order` sư phạm ghi rõ theo chapter (không phụ thuộc ID nguồn).

**Cửa ra:** không rename/convert hàng loạt cho đến khi bạn xác nhận inventory (hoặc chỉnh order/slug tại đây). Tiếp theo = **Pha 2 — tooling** (`scripts/normalize_theory_ai.py`, đã sẵn sàng).
