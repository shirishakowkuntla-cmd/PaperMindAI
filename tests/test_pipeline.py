"""
Unit and Integration Tests for PaperMind AI Core Pipeline.
Tests text extraction, classification, summarization, keyword extraction,
paper comparison, markdown reporting, and boundary edge cases.
"""

import os
import pytest
from src.pdf_extractor import PDFExtractor
from src.classifier import PaperClassifier, RESEARCH_CATEGORIES
from src.summarizer import PaperSummarizer
from src.keyword_extractor import KeywordExtractor
from src.comparator import PaperComparator
from src.utils import generate_markdown_report

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_papers")
ATTENTION_PDF = os.path.join(SAMPLE_DIR, "sample_attention_transformer.pdf")
RESNET_PDF = os.path.join(SAMPLE_DIR, "sample_resnet_computer_vision.pdf")
PHISHING_PDF = os.path.join(SAMPLE_DIR, "sample_phishing_detection_cybersecurity.pdf")


def test_pdf_extractor_attention():
    extractor = PDFExtractor()
    result = extractor.extract_from_file(ATTENTION_PDF)

    assert result["page_count"] == 2
    assert result["metadata"]["word_count"] > 200
    assert "Transformer" in result["full_text"] or "attention" in result["full_text"].lower()
    assert len(result["sections"]["abstract"]) > 50
    assert len(result["sections"]["methodology"]) > 50
    assert "Attention Is All You Need" in result["title"]


def test_pdf_extractor_clean_ligatures():
    extractor = PDFExtractor()
    # Test ligature decomposition and unicode normalization
    raw = "classi\ufb01cation of \ufb02oating-point \u00adweights with soft-hyphens"
    cleaned = extractor._clean_text(raw)
    assert "classification" in cleaned
    assert "floating-point" in cleaned
    assert "\u00ad" not in cleaned


def test_classifier_all_domains():
    classifier = PaperClassifier(use_transformer=False)
    assert classifier.local_model is not None

    test_queries = [
        ("Proximal policy optimization and deep reinforcement learning", "Artificial Intelligence & Machine Learning"),
        ("Convolutional neural networks for semantic image segmentation on ImageNet", "Computer Vision & Pattern Recognition"),
        ("Transformers and language models for machine translation and text generation", "Natural Language Processing (NLP)"),
        ("Malware detection, intrusion detection systems and cryptography against zero-day exploits", "Cybersecurity & Cryptography"),
        ("Large-scale time series anomaly detection and exploratory data analysis on big data clusters", "Data Science & Big Data Analytics"),
        ("Simultaneous localization and mapping (SLAM) and motion planning for quadruped robots", "Robotics & Autonomous Systems"),
        ("Distributed consensus using Raft and low-latency packet routing across 5G networks", "Networks & Distributed Computing"),
    ]

    for query, expected_domain in test_queries:
        res = classifier.classify(query, title=query[:30])
        assert res["predicted_category"] == expected_domain, f"Query '{query}' predicted {res['predicted_category']} instead of {expected_domain}"
        assert res["confidence"] > 0.15
        assert len(res["all_scores"]) == len(RESEARCH_CATEGORIES)


def test_classifier_empty_input():
    classifier = PaperClassifier(use_transformer=False)
    res = classifier.classify("", title="")
    assert res["predicted_category"] == "Unknown"
    assert res["confidence"] == 0.0


def test_summarizer_structure():
    extractor = PDFExtractor()
    paper_data = extractor.extract_from_file(RESNET_PDF)

    summarizer = PaperSummarizer(use_transformer=False)
    summary = summarizer.summarize_paper(paper_data["sections"], paper_data["full_text"])

    assert len(summary["executive_summary"]) > 20
    assert len(summary["problem_statement"]) > 20
    assert len(summary["methodology"]) > 20
    assert len(summary["findings"]) > 20
    assert len(summary["conclusion"]) > 20
    assert "TextRank" in summary["engine"]


def test_summarizer_abbreviation_handling():
    summarizer = PaperSummarizer(use_transformer=False)
    # Test that abbreviations like et al. and e.g. don't break sentences into fragments
    text = (
        "According to Vaswani et al. the transformer replaces recurrent networks entirely. "
        "Furthermore, e.g. on English-to-German translation tasks, it establishes superior results. "
        "The experiments demonstrate high BLEU scores and rapid convergence during distributed training."
    )
    summary = summarizer._extractive_textrank_summary(text, target_sentences=2)
    assert "Vaswani et al." in summary
    assert len(summary.split()) > 10


def test_keyword_extraction():
    extractor = PDFExtractor()
    paper_data = extractor.extract_from_file(PHISHING_PDF)

    kw_extractor = KeywordExtractor(top_n=8)
    keywords = kw_extractor.extract_keywords(paper_data["full_text"], title=paper_data["title"])

    assert len(keywords) > 0
    phrases = [k["phrase"].lower() for k in keywords]
    assert any("phishing" in p or "url" in p or "threat" in p or "neural" in p for p in phrases)
    # Ensure scores are normalized between 0.0 and 1.0
    for k in keywords:
        assert 0.0 <= k["score"] <= 1.0


def test_comparator():
    extractor = PDFExtractor()
    classifier = PaperClassifier(use_transformer=False)
    summarizer = PaperSummarizer(use_transformer=False)
    kw_extractor = KeywordExtractor(top_n=8)

    # Process Paper A (Attention)
    data_a = extractor.extract_from_file(ATTENTION_PDF)
    data_a["classification"] = classifier.classify(data_a["sections"]["abstract"], data_a["title"])
    data_a["summary"] = summarizer.summarize_paper(data_a["sections"], data_a["full_text"])
    data_a["keywords"] = kw_extractor.extract_keywords(data_a["full_text"], data_a["title"])

    # Process Paper B (ResNet)
    data_b = extractor.extract_from_file(RESNET_PDF)
    data_b["classification"] = classifier.classify(data_b["sections"]["abstract"], data_b["title"])
    data_b["summary"] = summarizer.summarize_paper(data_b["sections"], data_b["full_text"])
    data_b["keywords"] = kw_extractor.extract_keywords(data_b["full_text"], data_b["title"])

    comparator = PaperComparator()
    diff = comparator.compare(data_a, data_b)

    assert "similarity_score" in diff
    assert "section_comparison" in diff
    assert "verdict" in diff
    assert diff["paper_a_metrics"]["pages"] == 2
    assert diff["paper_b_metrics"]["pages"] == 2


def test_comparator_none_handling():
    comparator = PaperComparator()
    # Ensure empty or malformed inputs do not crash comparator
    diff = comparator.compare({}, {})
    assert diff["similarity_score"] == 0.0
    assert diff["domain_a"] == "Unknown"
    assert diff["domain_b"] == "Unknown"
    assert isinstance(diff["shared_keywords"], list)


def test_markdown_report_generation():
    paper_data = {
        "title": "Sample Neural Architecture",
        "metadata": {"page_count": 5, "word_count": 2500, "estimated_reading_time_mins": 12},
        "classification": {"predicted_category": "Artificial Intelligence & Machine Learning", "confidence": 0.95},
        "summary": {"executive_summary": "Test executive summary.", "problem_statement": "Problem", "methodology": "Method", "findings": "Findings", "conclusion": "Conclusion"},
        "keywords": [{"phrase": "Neural Network", "score": 0.9, "type": "bigram"}]
    }
    report = generate_markdown_report(paper_data)
    assert "# PaperMind AI" in report
    assert "2,500 words" in report
    assert "Sample Neural Architecture" in report
