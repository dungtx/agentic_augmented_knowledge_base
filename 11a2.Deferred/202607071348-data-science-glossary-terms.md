---
status: deferred
kind: idea
captured_at: 2026-07-07T13:48:00+07:00
tags: []
needs_review: false
triaged_at: 2026-07-23T09:00:00+07:00
---

# Data Science Glossary — Vietnamese Terms to English

**mô hình → Model** — A trained algorithm or mathematical representation that maps inputs to outputs based on learned patterns from data. In ML, the output of a training process.

**metrics → Metrics** — Quantitative measures of model performance. Examples: accuracy, precision, recall, F1, RMSE, MAE. Choice depends on problem type and business goal.

**xử lý dữ liệu → Data processing** — The general pipeline of converting raw data into usable format through collection, transformation, storage, and analysis.

**xử lý dữ liệu → Data wrangling (munging)** — Mapping and transforming raw data from one format into another suitable for downstream analysis. Includes parsing, reshaping, merging, enriching.

**xử lý dữ liệu → Data preprocessing / cleaning** — Detecting and correcting corrupt, inaccurate, or missing data before modeling. Includes nulls, outliers, duplicates, normalization, encoding.

**feature quan trọng → Feature importance** — ML-specific scores for each input feature indicating contribution to predictions. Methods: permutation importance, SHAP, coefficient magnitude, tree-based gain. Used for interpretability and selection.

**có tác động lớn → High-impact / influential feature** — General notion: a feature whose value strongly drives model output. Identified via domain knowledge, EDA, or engineering intuition, not necessarily formal scoring.

**feature (data science context) → Feature** — An individual measurable property used as input variable to an ML model. Also called predictor or independent variable. The columns the model learns from.

**feature selection (ML context) → Feature selection** — Selecting a subset of relevant predictor variables for model construction. Reduces overfitting, improves accuracy, decreases training time. Methods: filter (correlation, chi-square), wrapper (RFE), embedded (Lasso, tree importance).

**Tổng feature (interview/sales context) → Total product features** — The complete set of capabilities, functions, and characteristics of a software system. In an interview, the question gauges scope awareness and ability to articulate the system's full surface area.

**feature chọn lọc (sales context) → Selected product features** — A curated subset of product features pitched to a specific customer. Emphasizes value proposition over completeness — lead with what solves their pain points.

**Poor fit → Poor fit / Underfitting** — Model fails to capture the underlying training pattern, resulting in high bias and poor performance on both training and test sets. Often from a model too simple for the data.

**classification → Classification** — Supervised learning task predicting a categorical label. Binary (2 classes) or multi-class (3+). Outputs are typically class probabilities.

**Imbalance → Class imbalance** — One class significantly outnumbers another in training data. Common in fraud, rare disease, etc. Requires special handling (resampling, weighted loss, synthetic data) to avoid trivial majority-class prediction.
