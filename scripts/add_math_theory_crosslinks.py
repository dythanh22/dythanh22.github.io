#!/usr/bin/env python3
"""Phase 5: append light Math ↔ Theory cross-link callouts (build-math-lesson.md)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- CROSSLINK_MATH_THEORY -->"

# (path relative to bai-hoc/, callout body markdown without outer marker)
MATH_CALLOUTS: dict[str, str] = {
    "math-base/01-probability/conditional-probability.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
Phân phối rời rạc + code: [Bernoulli](../../theory-ai/01-probability/bernoulli-pmf-moments.qmd) · [Binomial](../../theory-ai/01-probability/binomial-pmf.qmd) · [Expected value](../../theory-ai/01-probability/expected-value-discrete.qmd).
:::
""",
    "math-base/01-probability/probability-distributions.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
PMF / moment từng phân phối: [Bernoulli](../../theory-ai/01-probability/bernoulli-pmf-moments.qmd) · [Binomial](../../theory-ai/01-probability/binomial-pmf.qmd) · [Poisson](../../theory-ai/01-probability/poisson-pmf-cdf.qmd) · [Geometric](../../theory-ai/01-probability/geometric-pmf-mean.qmd).
:::
""",
    "math-base/01-probability/random-variables-and-expectation.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
Kỳ vọng rời rạc + snippet: [Expected value](../../theory-ai/01-probability/expected-value-discrete.qmd).
:::
""",
    "math-base/02-statistics/descriptive-statistics-study-guide.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
Xu hướng trung tâm + code ngắn: [Mean / Median / Mode](../../theory-ai/02-statistics/mean-median-mode.qmd) · [Sample variance](../../theory-ai/02-statistics/sample-variance-and-standard-deviation.qmd).
:::
""",
    "math-base/02-statistics/one-sample-t-test.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
Cùng chủ đề, bài atom + ví dụ số: [One-sample t-test](../../theory-ai/02-statistics/one-sample-t-test.qmd).
:::
""",
    "math-base/02-statistics/correlation-and-covariance.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
Ma trận tương quan Pearson: [Pearson correlation matrix](../../theory-ai/02-statistics/pearson-correlation-matrix.qmd).
:::
""",
    "math-base/03-linear-algebra/dot-product-vector-norms.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
Norm / khoảng cách / cosine trên vector 3D: [Norm 3D](../../theory-ai/03-linear-algebra/3d-vector-norm.qmd) · [Euclidean](../../theory-ai/03-linear-algebra/euclidean-distance.qmd) · [Cosine](../../theory-ai/03-linear-algebra/cosine-similarity.qmd).
:::
""",
    "math-base/03-linear-algebra/eigenvalues-eigenvectors.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
Tính trị riêng trên ma trận nhỏ: [Calculate eigenvalues](../../theory-ai/03-linear-algebra/calculate-eigenvalues-of-a-matrix.qmd).
:::
""",
    "math-base/03-linear-algebra/determinants-inverses.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
Nghịch đảo ma trận (ví dụ số): [Matrix inverse](../../theory-ai/03-linear-algebra/matrix-inverse.qmd).
:::
""",
    "math-base/04-calculus/the-chain-rule.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
Sau chain rule: tối ưu dùng gradient — [Nesterov](../../theory-ai/08-optimizers/nesterov-momentum-nag.qmd) · [Adam](../../theory-ai/08-optimizers/adam-optimizer-step.qmd).
:::
""",
    "math-base/05-optimization/momentum-nesterov-accelerated-gradient.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
Bước cập nhật NAG + code: [Nesterov momentum](../../theory-ai/08-optimizers/nesterov-momentum-nag.qmd).
:::
""",
    "math-base/05-optimization/adaptive-learning-rates.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
Adam / AdamW từng bước: [Adam](../../theory-ai/08-optimizers/adam-optimizer-step.qmd) · [AdamW](../../theory-ai/08-optimizers/adamw-decoupled-weight-decay.qmd).
:::
""",
    "math-base/06-information-theory/shannon-entropy.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
Entropy trên node cây quyết định + KL loss: [Entropy for a node](../../theory-ai/05-classical-ml/entropy-for-a-node.qmd) · [KL Divergence](../../theory-ai/07-activations-losses/kl-divergence.qmd).
:::
""",
    "math-base/06-information-theory/kullback-leibler-divergence.qmd": """
::: {.callout-tip}
## Ôn nhanh (Theory AI)
KL trong loss / VAE: [KL Divergence](../../theory-ai/07-activations-losses/kl-divergence.qmd).
:::
""",
}

THEORY_CALLOUTS: dict[str, str] = {
    "theory-ai/01-probability/bernoulli-pmf-moments.qmd": """
::: {.callout-tip}
## Nền đầy đủ (Math Base)
Phân phối & xác suất có điều kiện: [Phân phối xác suất](../../math-base/01-probability/probability-distributions.qmd) · [Conditional Probability](../../math-base/01-probability/conditional-probability.qmd).
:::
""",
    "theory-ai/01-probability/expected-value-discrete.qmd": """
::: {.callout-tip}
## Nền đầy đủ (Math Base)
Biến ngẫu nhiên & kỳ vọng (chiều sâu): [Random Variables and Expectation](../../math-base/01-probability/random-variables-and-expectation.qmd).
:::
""",
    "theory-ai/02-statistics/mean-median-mode.qmd": """
::: {.callout-tip}
## Nền đầy đủ (Math Base)
Thống kê mô tả đầy đủ: [Descriptive Statistics](../../math-base/02-statistics/descriptive-statistics-study-guide.qmd).
:::
""",
    "theory-ai/02-statistics/one-sample-t-test.qmd": """
::: {.callout-tip}
## Nền đầy đủ (Math Base)
Cùng kiểm định, bài nền dài hơn: [One-Sample T-Test](../../math-base/02-statistics/one-sample-t-test.qmd).
:::
""",
    "theory-ai/02-statistics/pearson-correlation-matrix.qmd": """
::: {.callout-tip}
## Nền đầy đủ (Math Base)
Tương quan & hiệp phương sai: [Correlation and Covariance](../../math-base/02-statistics/correlation-and-covariance.qmd).
:::
""",
    "theory-ai/03-linear-algebra/3d-vector-norm.qmd": """
::: {.callout-tip}
## Nền đầy đủ (Math Base)
Dot product & các chuẩn: [Dot Product & Vector Norms](../../math-base/03-linear-algebra/dot-product-vector-norms.qmd).
:::
""",
    "theory-ai/03-linear-algebra/cosine-similarity.qmd": """
::: {.callout-tip}
## Nền đầy đủ (Math Base)
Tích vô hướng / chuẩn / góc: [Dot Product & Vector Norms](../../math-base/03-linear-algebra/dot-product-vector-norms.qmd).
:::
""",
    "theory-ai/03-linear-algebra/calculate-eigenvalues-of-a-matrix.qmd": """
::: {.callout-tip}
## Nền đầy đủ (Math Base)
Trị riêng & vector riêng: [Eigenvalues & Eigenvectors](../../math-base/03-linear-algebra/eigenvalues-eigenvectors.qmd).
:::
""",
    "theory-ai/03-linear-algebra/matrix-inverse.qmd": """
::: {.callout-tip}
## Nền đầy đủ (Math Base)
Định thức & nghịch đảo: [Determinants & Inverses](../../math-base/03-linear-algebra/determinants-inverses.qmd).
:::
""",
    "theory-ai/07-activations-losses/kl-divergence.qmd": """
::: {.callout-tip}
## Nền đầy đủ (Math Base)
Entropy & KL (chiều sâu): [Shannon Entropy](../../math-base/06-information-theory/shannon-entropy.qmd) · [KL Divergence](../../math-base/06-information-theory/kullback-leibler-divergence.qmd).
:::
""",
    "theory-ai/08-optimizers/nesterov-momentum-nag.qmd": """
::: {.callout-tip}
## Nền đầy đủ (Math Base)
Momentum & NAG (lý thuyết): [Momentum & Nesterov](../../math-base/05-optimization/momentum-nesterov-accelerated-gradient.qmd).
:::
""",
    "theory-ai/08-optimizers/adam-optimizer-step.qmd": """
::: {.callout-tip}
## Nền đầy đủ (Math Base)
Adaptive learning rates: [Adaptive Learning Rates](../../math-base/05-optimization/adaptive-learning-rates.qmd).
:::
""",
}


def apply_callout(rel: str, body: str) -> str:
    path = ROOT / "bai-hoc" / rel
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return "skip"
    block = "\n" + MARKER + "\n" + body.strip() + "\n"

    insert_at = None
    for needle in ("<!-- auto-self-check -->", "<!-- SELFCHECK_", "<!-- CROSSLINK_"):
        idx = text.find(needle)
        if idx >= 0:
            insert_at = idx
            break

    if insert_at is not None:
        text = text[:insert_at] + block + "\n" + text[insert_at:]
        path.write_text(text, encoding="utf-8")
        return "insert"
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block, encoding="utf-8")
    return "append"


def main() -> None:
    stats = {"ok": 0, "skip": 0}
    for rel, body in {**MATH_CALLOUTS, **THEORY_CALLOUTS}.items():
        status = apply_callout(rel, body)
        print(f"{status:28s}  {rel}")
        if status == "skip":
            stats["skip"] += 1
        else:
            stats["ok"] += 1
    print(f"Done: {stats['ok']} added, {stats['skip']} skipped")


if __name__ == "__main__":
    main()
