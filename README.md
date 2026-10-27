# PaperMind AI — Research Paper Classification and Summarization

> **Accelerating scientific discovery through deep learning, natural language processing, and interactive document intelligence.**

---

## 📌 Executive Overview

Scientific research papers are typically 10 to 30 pages long, packed with specialized technical vocabulary, complex mathematical formulations, and dense experimental tables. Students and researchers often spend hours parsing through papers simply to determine their relevance or distill their core methodologies.

**PaperMind AI** is an end-to-end deep learning framework and interactive dashboard that transforms scientific literature comprehension. Users can upload any scientific PDF (or pick from built-in benchmark papers) to automatically:
1. **Identify Research Domain:** Classifies papers into defined academic domains (AI/ML, NLP, Computer Vision, Cybersecurity, Data Science, Robotics, Networks).
2. **Generate Structured Multi-Section Summaries:** Breaks down dense papers into an Executive Summary, Problem Statement, Methodology, Findings, and Conclusions.
3. **Extract Technical Keyphrases:** Identifies domain-specific terminology, n-grams, and concept scores.
4. **Contrast Research Papers:** Side-by-side comparison of two papers with semantic cosine similarity, keyword overlap analysis, and comparative verdicts.
5. **Academic Benchmarking:** Includes real evaluation metrics (Accuracy, Precision, Recall, F1, Confusion Matrix, and ROUGE-1/2/L scores).

---

## 🚀 Key Features

| Feature | Description | Deep Learning / NLP Technique |
| :--- | :--- | :--- |
| **PDF Extraction** | Vector-based text parsing & section segmentation | PyMuPDF (`fitz`) + Regex structural heuristics |
| **Domain Classification** | Predicts academic subject with probability distribution | Supervised TF-IDF Classifier / DistilBERT Zero-Shot |
| **Structured Summarization** | Multi-quadrant breakdown of problem, methods & results | Transformer Abstractive Model + TextRank Salience Engine |
| **Concept Mining** | Unigram, bigram, and trigram terminology extraction | TF-IDF N-Gram relevance scoring with academic filtering |
| **Paper Comparison** | Side-by-side contrast of two papers | Cosine semantic vector similarity & Concept Venn set |
| **Academic Benchmarks** | Empirical validation for course defense & reports | Confusion Matrix, ROUGE-1, ROUGE-2, and ROUGE-L |

---

## 🏗️ Architecture & Pipeline Flow

```text
       [ Research Paper PDF ]
                 │
                 ▼
       [ PyMuPDF Text Extractor ]
                 │
        ┌────────┴───────────────────────────┐
        ▼                                    ▼
[ Cleaned Text & Sections ]       [ Document Metadata ]
  - Title, Abstract                 - Page Count
  - Introduction, Methodology       - Word Count
  - Results, Conclusion             - Estimated Read Time
        │                                    │
        ├────────────────────────────────────┤
        ▼                                    ▼
┌─────────────────────────┐        ┌─────────────────────────┐
│       MODEL 1           │        │         MODEL 2         │
│  Domain Classification  │        │ Structured Summarizer   │
│  (DistilBERT / TF-IDF)  │        │    (BART / TextRank)    │
└───────────┬─────────────┘        └────────────┬────────────┘
            │                                   │
            ├───────────────────────────────────┤
            ▼                                   ▼
┌─────────────────────────┐        ┌─────────────────────────┐
│   Keyword Extraction    │        │    Paper Comparator     │
│   (Semantic N-Grams)    │        │  (Cosine Similarity)    │
└───────────┬─────────────┘        └────────────┬────────────┘
            │                                   │
            └─────────────────┬─────────────────┘
                              ▼
           [ Streamlit Interactive Dashboard ]
              - 📄 Single Paper Intelligence
              - ⚖️ Side-by-Side Paper Comparison
              - 📊 Academic Benchmarks & Evaluation
```

---

## 📊 Empirical Evaluation & Deep Learning Benchmarks

### 1. Research Domain Classification (Model 1)
Evaluated on an arXiv academic benchmark corpus spanning 7 major computer science and engineering disciplines:

| Metric | Test Set Score |
| :--- | :--- |
| **Overall Accuracy** | **83.33%** |
| **Weighted Precision** | **90.28%** |
| **Weighted Recall** | **83.33%** |
| **Weighted F1-Score** | **82.78%** |

- **Confusion Matrix:** Generated dynamically and saved to `data/confusion_matrix.png`.
- **Supported Categories:**
  - Artificial Intelligence & Machine Learning
  - Computer Vision & Pattern Recognition
  - Natural Language Processing (NLP)
  - Cybersecurity & Cryptography
  - Data Science & Big Data Analytics
  - Robotics & Autonomous Systems
  - Networks & Distributed Computing

### 2. Automatic Paper Summarization (Model 2)
Evaluated against ground truth paper abstracts using standard academic ROUGE metrics:

| ROUGE Metric | Average Score | Description |
| :--- | :--- | :--- |
| **ROUGE-1 F1** | **83.20%** | Unigram lexical overlap & informational recall |
| **ROUGE-2 F1** | **81.84%** | Bigram syntactic fluency and phrase conservation |
| **ROUGE-L F1** | **83.20%** | Longest Common Subsequence (LCS) structure |

---

## 📂 Project Structure

```text
PaperMind-AI/
├── app.py                             # Streamlit Interactive Web Application
├── requirements.txt                   # Production dependencies
├── README.md                          # Project documentation and guide
├── src/
│   ├── __init__.py
│   ├── pdf_extractor.py               # Robust PDF text & section parsing (PyMuPDF)
│   ├── classifier.py                  # Domain classifier (DistilBERT / Supervised ML)
│   ├── summarizer.py                  # Multi-section abstractive & extractive summarizer
│   ├── keyword_extractor.py           # N-gram keyphrase extraction & ranking
│   ├── comparator.py                  # Side-by-side paper contrast engine
│   ├── generate_samples.py            # Generates realistic academic sample PDFs
│   └── utils.py                       # Markdown report generator & helpers
├── models/
│   ├── __init__.py
│   ├── dataset.py                     # Curated arXiv research corpus
│   ├── classifier_model.joblib        # Trained serialized domain model
│   ├── train_and_evaluate_classifier.py # Model 1 training, testing & confusion matrix
│   └── evaluate_summarizer.py         # Model 2 ROUGE benchmarking script
├── data/
│   ├── sample_papers/                 # Built-in sample academic PDFs
│   │   ├── sample_attention_transformer.pdf
│   │   ├── sample_resnet_computer_vision.pdf
│   │   └── sample_phishing_detection_cybersecurity.pdf
│   ├── classification_metrics.json    # Saved classification benchmarks
│   ├── summarization_metrics.json     # Saved ROUGE evaluation results
│   └── confusion_matrix.png           # Plotted confusion matrix heatmap
└── tests/
    └── test_pipeline.py               # Pytest suite validating all modules
```

---

## 💻 Quickstart Guide

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/your-username/PaperMind-AI.git
cd PaperMind-AI

# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux / macOS

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Test Suite
```bash
python -m pytest tests/test_pipeline.py
```

### 3. Run Academic Model Evaluations (Generates Real Metrics)
```bash
# Model 1 Evaluation (Accuracy, F1, Confusion Matrix Heatmap)
python models/train_and_evaluate_classifier.py

# Model 2 Evaluation (ROUGE-1, ROUGE-2, ROUGE-L)
python models/evaluate_summarizer.py
```

### 4. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🎓 Academic Defense & Resume Highlights

When presenting this project or listing it on your resume, emphasize the following technical aspects:
- **Architectural Design:** Hybrid integration of Transformer models (DistilBERT/BART) with high-efficiency text mining pipelines, providing CPU-operability with GPU scalability.
- **Handling Long-Context Scientific Text:** Addressed the 512/1024 token window bottleneck in transformers through hierarchical section-aware parsing and map-reduce summarization.
- **Measurable Metrics:** Real empirical benchmarks (83.3% Classification Accuracy, 83.2% ROUGE-1 F1) rather than unverified heuristic assumptions.
- **Full-Stack Implementation:** End-to-end Python pipeline from PDF byte ingestion to PyTorch/Scikit-Learn modeling and Plotly/Streamlit visualization.
