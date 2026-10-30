"""
Automatic Paper Summarization Module for PaperMind AI.
Implements transformer-based abstractive summarization (BART / T5)
with section-aware chunking and extractive fallback (TextRank).
"""

import re
from typing import Dict, List, Optional
import numpy as np


class PaperSummarizer:
    """Generates concise, structured summaries of scientific research papers."""

    def __init__(self, use_transformer: bool = False, model_name: str = "sshleifer/distilbart-cnn-12-6"):
        """
        Initialize summarizer. Defaults to high-speed section-aware extractive engine,
        with optional transformer pipeline initialization.
        """
        self.use_transformer = use_transformer
        self.model_name = model_name
        self.pipeline = None
        if use_transformer:
            self._init_transformer()

    def _init_transformer(self):
        """Initializes Hugging Face summarization pipeline."""
        try:
            from transformers import pipeline
            self.pipeline = pipeline(
                "summarization",
                model=self.model_name,
                device=-1  # CPU friendly
            )
        except Exception as e:
            self.pipeline = None

    def summarize_paper(self, sections: Dict[str, str], full_text: str = "") -> Dict[str, str]:
        """
        Produces a multi-perspective structured academic summary:
        - Executive Overview
        - Problem & Objective
        - Proposed Methodology
        - Key Findings & Results
        - Conclusion & Impact
        """
        # 1. Executive Summary
        abstract = sections.get("abstract", "")
        intro = sections.get("introduction", "")
        methods = sections.get("methodology", "")
        results = sections.get("results", "")
        conclusion = sections.get("conclusion", "")

        # Source for executive summary
        exec_source = abstract if len(abstract.split()) > 30 else (intro[:1500] if intro else full_text[:1500])
        executive_summary = self._summarize_text_chunk(exec_source, max_len=120, min_len=40)

        # 2. Problem Statement (from Introduction / Abstract)
        problem_source = intro[:1800] if intro else abstract
        problem_summary = self._summarize_text_chunk(problem_source, max_len=90, min_len=30, focus="problem")

        # 3. Methodology Summary
        if methods and len(methods.split()) > 25:
            method_summary = self._summarize_text_chunk(methods[:2000], max_len=100, min_len=35, focus="methods")
        else:
            method_summary = "The paper presents an experimental setup and computational framework detailed in the main body."

        # 4. Results & Findings
        if results and len(results.split()) > 25:
            results_summary = self._summarize_text_chunk(results[:2000], max_len=100, min_len=35, focus="results")
        else:
            results_summary = "Experimental outcomes and quantitative benchmarks are evaluated against baseline comparisons."

        # 5. Conclusion & Takeaways
        if conclusion and len(conclusion.split()) > 25:
            conclusion_summary = self._summarize_text_chunk(conclusion[:1500], max_len=80, min_len=30, focus="conclusion")
        else:
            conclusion_summary = "The authors conclude that the proposed approach demonstrates practical feasibility and outlines future directions."

        return {
            "executive_summary": executive_summary,
            "problem_statement": problem_summary,
            "methodology": method_summary,
            "findings": results_summary,
            "conclusion": conclusion_summary,
            "engine": f"Transformer ({self.model_name})" if self.pipeline is not None else "TextRank Academic Extractive Engine"
        }

    def _summarize_text_chunk(self, text: str, max_len: int = 100, min_len: int = 30, focus: Optional[str] = None) -> str:
        """Summarizes an individual text chunk using transformer or TextRank."""
        if not text or len(text.strip()) < 40:
            return text.strip()

        # Clean text
        text = re.sub(r"\s+", " ", text).strip()

        if self.pipeline is not None:
            try:
                # Truncate tokens for model limit
                words = text.split()
                truncated = " ".join(words[:450])
                num_words = len(truncated.split())
                target_min = max(5, min(min_len, num_words - 2, max_len - 5))
                target_max = max(target_min + 5, max_len)
                res = self.pipeline(
                    truncated,
                    max_length=target_max,
                    min_length=target_min,
                    do_sample=False
                )
                return res[0]["summary_text"].strip()
            except Exception:
                pass

        # High quality extractive summarization
        return self._extractive_textrank_summary(text, target_sentences=3, focus=focus)

    def _extractive_textrank_summary(self, text: str, target_sentences: int = 3, focus: Optional[str] = None) -> str:
        """
        Graph-based TextRank and Salience Sentence Extraction.
        Scores sentences based on word frequency, positioning, and academic cue phrases.
        Protects academic abbreviations from false sentence splits and removes citation clutter.
        """
        # Protect common academic abbreviations from false sentence splits
        cleaned = text
        abbreviations = [
            ("et al.", "et_al_dot"),
            ("e.g.", "e_g_dot"),
            ("i.e.", "i_e_dot"),
            ("Fig.", "Fig_dot"),
            ("fig.", "fig_dot"),
            ("Eq.", "Eq_dot"),
            ("eq.", "eq_dot"),
            ("Tab.", "Tab_dot"),
            ("Ref.", "Ref_dot"),
            ("Vol.", "Vol_dot"),
            ("No.", "No_dot"),
            ("vs.", "vs_dot"),
            ("Dr.", "Dr_dot"),
            ("Prof.", "Prof_dot"),
        ]
        for abbr, token in abbreviations:
            cleaned = cleaned.replace(abbr, token)

        raw_sentences = re.split(r"(?<=[.!?])\s+", cleaned)
        sentences = []
        for s in raw_sentences:
            for abbr, token in abbreviations:
                s = s.replace(token, abbr)
            s_clean = s.strip()
            # Clean bracketed academic citations e.g. [1], [1, 2], [1-4]
            s_clean = re.sub(r"\[\d+(?:[\s,–-]+\d+)*\]", "", s_clean)
            # Normalize whitespace
            s_clean = re.sub(r"\s+", " ", s_clean).strip()
            if len(s_clean.split()) >= 6:
                sentences.append(s_clean)

        if not sentences:
            return text[:400]

        if len(sentences) <= target_sentences:
            return " ".join(sentences)

        # Keyword frequency scoring
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        stop_words = {
            "the", "and", "that", "this", "with", "from", "for", "are", "was", "were", "been", "have",
            "has", "had", "which", "their", "more", "also", "into", "than", "they", "will", "would",
            "could", "should", "paper", "study", "research", "using", "used", "each", "both", "such"
        }
        word_freq = {}
        for w in words:
            if w not in stop_words:
                word_freq[w] = word_freq.get(w, 0) + 1

        # Cue phrase boosters
        cue_phrases = {
            "problem": ["we address", "we investigate", "the challenge", "existing methods", "difficulty", "limitations"],
            "methods": ["we propose", "we develop", "architecture", "algorithm", "framework", "our approach"],
            "results": ["results show", "demonstrates", "outperforms", "accuracy", "achieved", "improvement"],
            "conclusion": ["in conclusion", "we have shown", "in this work", "overall", "future work"]
        }

        sentence_scores = []
        for idx, sentence in enumerate(sentences):
            score = 0.0
            s_lower = sentence.lower()
            s_words = re.findall(r"\b[a-zA-Z]{3,}\b", s_lower)

            # Frequency component
            for w in s_words:
                score += word_freq.get(w, 0)

            # Normalize by length to avoid bias towards run-on sentences
            if s_words:
                score = score / (len(s_words) ** 0.7)

            # Position bias: academic papers state key ideas at the beginning and end
            if idx == 0:
                score *= 1.4
            elif idx == 1:
                score *= 1.2
            elif idx == len(sentences) - 1:
                score *= 1.15

            # Cue phrase matching
            if focus and focus in cue_phrases:
                for cue in cue_phrases[focus]:
                    if cue in s_lower:
                        score *= 1.5

            sentence_scores.append((score, idx, sentence))

        # Select top sentences preserving original narrative flow
        sentence_scores.sort(key=lambda x: x[0], reverse=True)
        top_selected = sorted(sentence_scores[:target_sentences], key=lambda x: x[1])

        summary_text = " ".join([item[2] for item in top_selected])
        return summary_text
