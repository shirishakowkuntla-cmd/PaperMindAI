"""
Unit and Integration Tests for PaperMind AI Core Pipeline.
Tests text extraction, classification, summarization, keyword extraction, and comparison.
"""

import os
import pytest
from src.pdf_extractor import PDFExtractor
from src.classifier import PaperClassifier
from src.summarizer import PaperSummarizer
from src.keyword_extractor import KeywordExtractor
from src.comparator import PaperComparator

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


def test_classifier_domains():
    classifier = PaperClassifier(use_transformer=False)  # Test TF-IDF centroid fallback baseline first

    # Test NLP
    res_nlp = classifier.classify("We introduce self-attention and transformer architecture for language translation.")
    assert "Natural Language Processing" in res_nlp["predicted_category"] or "Artificial Intelligence" in res_nlp["predicted_category"]

    # Test CV
    res_cv = classifier.classify("Convolutional neural networks for image recognition and object detection on ImageNet.")
    assert "Computer Vision" in res_cv["predicted_category"]

    # Test Security
    res_sec = classifier.classify("Malware analysis, intrusion detection, phishing URLs, cryptography, and network defense.")
    assert "Cybersecurity" in res_sec["predicted_category"]


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


def test_keyword_extraction():
    extractor = PDFExtractor()
    paper_data = extractor.extract_from_file(PHISHING_PDF)

    kw_extractor = KeywordExtractor(top_n=8)
    keywords = kw_extractor.extract_keywords(paper_data["full_text"], title=paper_data["title"])

    assert len(keywords) > 0
    phrases = [k["phrase"].lower() for k in keywords]
    assert any("phishing" in p or "url" in p or "threat" in p or "neural" in p for p in phrases)


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
