"""
Summarization Model Evaluation Script for PaperMind AI.
Evaluates generated summaries against target reference abstracts using ROUGE scores
(ROUGE-1, ROUGE-2, ROUGE-L).
"""

import os
import sys
import json

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rouge_score import rouge_scorer
from src.pdf_extractor import PDFExtractor
from src.summarizer import PaperSummarizer


def evaluate_summarization():
    print("=" * 70)
    print("PaperMind AI -- Summarization Quality Evaluation (ROUGE Metrics)")
    print("=" * 70)

    sample_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_papers")
    test_files = [
        ("sample_attention_transformer.pdf", "Attention / Transformer Architecture"),
        ("sample_resnet_computer_vision.pdf", "Deep Residual Learning (ResNet)"),
        ("sample_phishing_detection_cybersecurity.pdf", "CyberGuard Phishing Detection")
    ]

    extractor = PDFExtractor()
    summarizer = PaperSummarizer(use_transformer=False)
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    rouge1_f_scores = []
    rouge2_f_scores = []
    rougel_f_scores = []
    results_list = []

    for filename, label in test_files:
        filepath = os.path.join(sample_dir, filename)
        if not os.path.exists(filepath):
            continue

        print(f"\nProcessing paper: {label} ({filename})...")
        doc_data = extractor.extract_from_file(filepath)
        reference_abstract = doc_data["sections"]["abstract"]

        # Generate summary
        summary_dict = summarizer.summarize_paper(doc_data["sections"], doc_data["full_text"])
        generated_summary = summary_dict["executive_summary"]

        scores = scorer.score(reference_abstract, generated_summary)

        r1 = scores['rouge1'].fmeasure
        r2 = scores['rouge2'].fmeasure
        rl = scores['rougeL'].fmeasure

        rouge1_f_scores.append(r1)
        rouge2_f_scores.append(r2)
        rougel_f_scores.append(rl)

        print(f"  ROUGE-1 F1: {r1 * 100:.2f}%")
        print(f"  ROUGE-2 F1: {r2 * 100:.2f}%")
        print(f"  ROUGE-L F1: {rl * 100:.2f}%")

        results_list.append({
            "paper": label,
            "filename": filename,
            "rouge1_f1": round(r1, 4),
            "rouge2_f1": round(r2, 4),
            "rougeL_f1": round(rl, 4),
            "reference_abstract_length": len(reference_abstract.split()),
            "summary_length": len(generated_summary.split())
        })

    avg_r1 = sum(rouge1_f_scores) / len(rouge1_f_scores) if rouge1_f_scores else 0
    avg_r2 = sum(rouge2_f_scores) / len(rouge2_f_scores) if rouge2_f_scores else 0
    avg_rl = sum(rougel_f_scores) / len(rougel_f_scores) if rougel_f_scores else 0

    print("\n" + "=" * 70)
    print("AVERAGE ROUGE BENCHMARK SUMMARY:")
    print(f"Average ROUGE-1 F1: {avg_r1 * 100:.2f}% (Word overlap / Informational coverage)")
    print(f"Average ROUGE-2 F1: {avg_r2 * 100:.2f}% (Bigram fluency & phrasal coherence)")
    print(f"Average ROUGE-L F1: {avg_rl * 100:.2f}% (Longest Common Subsequence structure)")
    print("=" * 70)

    # Save metrics
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    metrics_file = os.path.join(data_dir, "summarization_metrics.json")

    metrics_payload = {
        "average_rouge1_f1": round(avg_r1, 4),
        "average_rouge2_f1": round(avg_r2, 4),
        "average_rougeL_f1": round(avg_rl, 4),
        "evaluated_papers_count": len(results_list),
        "detailed_results": results_list
    }

    with open(metrics_file, "w") as f:
        json.dump(metrics_payload, f, indent=4)
    print(f"Saved summarization evaluation metrics to: {metrics_file}")


if __name__ == "__main__":
    evaluate_summarization()
