"""
Paper Comparison Engine for PaperMind AI.
Compares two scientific research papers across domains, methodologies,
findings, keyword overlap, and semantic similarity.
"""

from typing import Dict, List, Set
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class PaperComparator:
    """Performs side-by-side contrastive analysis of two scientific papers."""

    def compare(self, paper_a: Dict, paper_b: Dict) -> Dict:
        """
        Compare two analyzed papers.

        Args:
            paper_a: Analysis dict from paper 1 (includes metadata, classification, summary, keywords)
            paper_b: Analysis dict from paper 2

        Returns:
            Structured comparison results.
        """
        # 1. Semantic Similarity Calculation
        similarity_score = self._compute_similarity(
            paper_a.get("full_text", "") or "",
            paper_b.get("full_text", "") or ""
        )

        # 2. Keyword Venn Analysis
        raw_kw_a = paper_a.get("keywords") or []
        raw_kw_b = paper_b.get("keywords") or []
        kw_a = {item["phrase"].lower(): item for item in raw_kw_a if isinstance(item, dict) and "phrase" in item}
        kw_b = {item["phrase"].lower(): item for item in raw_kw_b if isinstance(item, dict) and "phrase" in item}

        shared_keywords = list(set(kw_a.keys()).intersection(set(kw_b.keys())))
        unique_a = [kw_a[k]["phrase"] for k in set(kw_a.keys()) - set(kw_b.keys())]
        unique_b = [kw_b[k]["phrase"] for k in set(kw_b.keys()) - set(kw_a.keys())]
        shared_phrases = [kw_a[k]["phrase"] for k in shared_keywords]

        # 3. Domain Alignment
        cls_a = paper_a.get("classification") or {}
        cls_b = paper_b.get("classification") or {}
        domain_a = cls_a.get("predicted_category", "Unknown")
        domain_b = cls_b.get("predicted_category", "Unknown")
        same_domain = (domain_a == domain_b) and (domain_a != "Unknown")

        # 4. Comparative Synthesis Verdict
        verdict = self._generate_verdict(
            domain_a, domain_b, same_domain, similarity_score, shared_phrases
        )

        meta_a = paper_a.get("metadata") or {}
        meta_b = paper_b.get("metadata") or {}
        sum_a = paper_a.get("summary") or {}
        sum_b = paper_b.get("summary") or {}

        return {
            "similarity_score": round(similarity_score * 100, 1),
            "same_domain": same_domain,
            "domain_a": domain_a,
            "domain_b": domain_b,
            "shared_keywords": shared_phrases,
            "unique_to_paper_a": unique_a[:8],
            "unique_to_paper_b": unique_b[:8],
            "verdict": verdict,
            "paper_a_metrics": {
                "title": paper_a.get("title", "Paper A"),
                "pages": meta_a.get("page_count", 0),
                "words": meta_a.get("word_count", 0),
                "reading_time": meta_a.get("estimated_reading_time_mins", 0),
            },
            "paper_b_metrics": {
                "title": paper_b.get("title", "Paper B"),
                "pages": meta_b.get("page_count", 0),
                "words": meta_b.get("word_count", 0),
                "reading_time": meta_b.get("estimated_reading_time_mins", 0),
            },
            "section_comparison": {
                "executive_summary": {
                    "paper_a": sum_a.get("executive_summary", ""),
                    "paper_b": sum_b.get("executive_summary", "")
                },
                "problem_statement": {
                    "paper_a": sum_a.get("problem_statement", ""),
                    "paper_b": sum_b.get("problem_statement", "")
                },
                "methodology": {
                    "paper_a": sum_a.get("methodology", ""),
                    "paper_b": sum_b.get("methodology", "")
                },
                "findings": {
                    "paper_a": sum_a.get("findings", ""),
                    "paper_b": sum_b.get("findings", "")
                },
                "conclusion": {
                    "paper_a": sum_a.get("conclusion", ""),
                    "paper_b": sum_b.get("conclusion", "")
                }
            }
        }

    def _compute_similarity(self, text_a: str, text_b: str) -> float:
        """Computes TF-IDF cosine similarity between two texts."""
        if not text_a or not text_b:
            return 0.0

        try:
            vec = TfidfVectorizer(stop_words="english", max_features=3000)
            tfidf = vec.fit_transform([text_a[:8000], text_b[:8000]])
            sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            return float(max(0.0, min(1.0, sim)))
        except Exception:
            return 0.0

    def _generate_verdict(self, domain_a: str, domain_b: str, same_domain: bool,
                          similarity: float, shared_keywords: List[str]) -> str:
        """Generates an intuitive comparative summary description."""
        if same_domain:
            if similarity > 0.6:
                return (
                    f"Strong Alignment: Both papers belong to '{domain_a}' and share deep thematic and "
                    f"methodological overlap ({round(similarity*100, 1)}% textual similarity). "
                    f"Common terminology includes {', '.join(shared_keywords[:4])}."
                )
            elif similarity > 0.3:
                return (
                    f"Moderate Convergence: Both papers operate within '{domain_a}', but approach "
                    f"distinct sub-problems or utilize differing experimental frameworks "
                    f"({round(similarity*100, 1)}% similarity)."
                )
            else:
                return (
                    f"Disparate Sub-branches: While classified under the same high-level domain ('{domain_a}'), "
                    f"these papers explore different specialized areas with low direct textual overlap."
                )
        else:
            return (
                f"Cross-Domain Comparison: Paper A investigates '{domain_a}' whereas Paper B focuses on "
                f"'{domain_b}'. Textual similarity is {round(similarity*100, 1)}% with "
                f"{len(shared_keywords)} overlapping technical concepts."
            )
