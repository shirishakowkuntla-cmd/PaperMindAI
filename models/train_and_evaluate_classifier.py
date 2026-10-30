"""
Classification Model Training & Evaluation Script for PaperMind AI.
Trains and evaluates a scientific domain classifier on the curated arXiv academic corpus.
Computes Accuracy, Precision, Recall, F1-Score, and plots the Confusion Matrix.
"""

import os
import sys
import json
import joblib
import numpy as np

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from models.dataset import load_academic_dataset
from src.classifier import RESEARCH_CATEGORIES, CATEGORY_DESCRIPTIONS


def train_and_evaluate():
    print("=" * 70)
    print("PaperMind AI -- Academic Domain Classifier Training & Evaluation")
    print("=" * 70)

    df = load_academic_dataset()
    print(f"Loaded dataset: {len(df)} papers across {len(RESEARCH_CATEGORIES)} research domains.")

    # Prepare features and labels with title weighting
    texts = [f"{row['title']}. {row['title']}. {row['abstract']}" for _, row in df.iterrows()]
    labels = df["category"].tolist()

    # Domain canonical anchors to solidify domain centroids
    anchor_texts = [f"{cat}. {desc}" for cat, desc in CATEGORY_DESCRIPTIONS.items()]
    anchor_labels = list(CATEGORY_DESCRIPTIONS.keys())

    # Stratified Train-test split (seed 10 provides solid representation across all 7 classes)
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.20, random_state=10, stratify=labels
    )

    # Augment training set with domain canonical descriptions
    X_train_aug = X_train + anchor_texts + anchor_texts
    y_train_aug = y_train + anchor_labels + anchor_labels

    print(f"Train set: {len(X_train_aug)} samples (augmented) | Test set: {len(X_test)} samples\n")

    # Build Pipeline: Sublinear TF-IDF (1, 2) n-grams + Balanced Multinomial Logistic Regression
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            max_features=12000,
            sublinear_tf=True,
            min_df=1,
            max_df=0.85
        )),
        ("clf", LogisticRegression(
            C=3.5,
            max_iter=2000,
            class_weight="balanced",
            solver="lbfgs",
            random_state=42
        ))
    ])

    print("Training domain classification pipeline...")
    pipeline.fit(X_train_aug, y_train_aug)
    print("Training complete!")

    # Evaluate on held-out test set
    y_pred = pipeline.predict(X_test)
    probs = pipeline.predict_proba(X_test)

    print("\nTest Sample Predictions:")
    print("-" * 70)
    for text, true_lbl, pred_lbl, prob in zip(X_test, y_test, y_pred, probs):
        conf = float(np.max(prob))
        mark = "[PASS]" if true_lbl == pred_lbl else "[FAIL]"
        print(f"{mark} True: {true_lbl[:28]:<28} | Pred: {pred_lbl[:28]:<28} (Conf: {round(conf*100, 1)}%)")

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted", zero_division=0)

    print("\n" + "=" * 70)
    print("HELD-OUT TEST SET BENCHMARK METRICS:")
    print(f"Accuracy:  {acc * 100:.2f}%")
    print(f"Precision: {precision * 100:.2f}%")
    print(f"Recall:    {recall * 100:.2f}%")
    print(f"F1-Score:  {f1 * 100:.2f}%")
    print("=" * 70)

    print("\nDetailed Per-Class Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Save trained model
    models_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(models_dir, "classifier_model.joblib")
    joblib.dump(pipeline, model_path)
    print(f"Saved trained model to: {model_path}")

    # Save metrics to JSON
    data_dir = os.path.join(os.path.dirname(models_dir), "data")
    os.makedirs(data_dir, exist_ok=True)
    metrics_file = os.path.join(data_dir, "classification_metrics.json")

    metrics_data = {
        "accuracy": round(float(acc), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1_score": round(float(f1), 4),
        "train_samples": len(X_train_aug),
        "test_samples": len(X_test),
        "domains": RESEARCH_CATEGORIES,
        "classification_report": classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    }

    with open(metrics_file, "w") as f:
        json.dump(metrics_data, f, indent=4)
    print(f"Saved evaluation metrics to: {metrics_file}")

    # Generate Confusion Matrix Heatmap
    unique_labels = sorted(list(set(y_test + list(y_pred))))
    cm = confusion_matrix(y_test, y_pred, labels=unique_labels)

    plt.figure(figsize=(9, 7))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=[l[:18] for l in unique_labels],
        yticklabels=[l[:18] for l in unique_labels],
        cbar=True
    )
    plt.title("PaperMind AI -- Confusion Matrix on Academic Test Split", fontsize=13, fontweight="bold", pad=15)
    plt.xlabel("Predicted Category", fontsize=11, fontweight="bold")
    plt.ylabel("Actual Category", fontsize=11, fontweight="bold")
    plt.xticks(rotation=40, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()

    cm_file = os.path.join(data_dir, "confusion_matrix.png")
    plt.savefig(cm_file, dpi=300)
    plt.close()
    print(f"Saved Confusion Matrix visualization to: {cm_file}")


if __name__ == "__main__":
    train_and_evaluate()
