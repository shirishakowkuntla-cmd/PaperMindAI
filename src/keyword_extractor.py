"""
Keyword and Concept Extraction Module for PaperMind AI.
Extracts unigram, bigram, and trigram keyphrases using TF-IDF and syntactic heuristics.
"""

import re
from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


# Custom academic stop words to filter out generic scientific filler
ACADEMIC_STOPWORDS = {
    "paper", "study", "research", "results", "using", "proposed", "method", "methods", "approach",
    "based", "data", "model", "models", "presents", "show", "shows", "author", "authors", "work",
    "et", "al", "figure", "table", "section", "demonstrate", "demonstrates", "evaluated", "performance",
    "different", "various", "existing", "well", "state", "art", "significantly", "respectively", "higher",
    "compared", "following", "given", "number", "case", "order", "furthermore", "however", "therefore",
    "abstract", "introduction", "conclusion", "references", "university", "department", "journal",
    "volume", "review", "proceedings", "conference", "table", "fig", "also", "used", "discusses",
    "gathered", "explored", "collected", "participants", "interview", "interviews", "students", "findings"
}


class KeywordExtractor:
    """Extracts informative scientific keyphrases and terminology."""

    def __init__(self, top_n: int = 12):
        self.top_n = top_n

    def extract_keywords(self, text: str, title: str = "") -> List[Dict]:
        """
        Extracts scored keyphrases from the document text.

        Returns:
            List of dicts: [{"phrase": "self-attention mechanism", "score": 0.42, "type": "bigram"}, ...]
        """
        if not text or len(text.strip()) < 30:
            return []

        # Split text into paragraphs or chunks to form a true multi-document corpus
        raw_paragraphs = text.split("\n\n")
        paragraphs = [p.strip() for p in raw_paragraphs if len(p.strip().split()) >= 8]

        # If too few paragraphs, split by sentence groups
        if len(paragraphs) < 3:
            sentences = re.split(r"(?<=[.!?])\s+", text)
            paragraphs = [" ".join(sentences[i:i+3]) for i in range(0, len(sentences), 3) if len(sentences[i:i+3]) > 0]

        if not paragraphs:
            paragraphs = [text]

        # Add title as an emphasized document in corpus
        if title:
            paragraphs.append(title)
            paragraphs.append(title)

        try:
            vectorizer = TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 3),
                max_df=0.95 if len(paragraphs) > 2 else 1.0,
                min_df=1,
                token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9_\-]{2,}\b"
            )

            tfidf_matrix = vectorizer.fit_transform(paragraphs)
            feature_names = vectorizer.get_feature_names_out()

            # Aggregate scores across paragraphs (sum of TF-IDF scores)
            aggregated_scores = np.asarray(tfidf_matrix.sum(axis=0)).ravel()

            # Max score for normalization
            max_score = float(np.max(aggregated_scores)) if len(aggregated_scores) > 0 and np.max(aggregated_scores) > 0 else 1.0

            # Filter candidates
            candidates = []
            for phrase, raw_score in zip(feature_names, aggregated_scores):
                words = phrase.split()

                # Filter if all words are academic generic stopwords or single characters
                if all(w.lower() in ACADEMIC_STOPWORDS for w in words):
                    continue
                if any(len(w) < 3 for w in words):
                    continue
                # Skip if phrase starts or ends with a generic stopword
                if words[0].lower() in ACADEMIC_STOPWORDS or words[-1].lower() in ACADEMIC_STOPWORDS:
                    continue

                # Normalize score between 0.0 and 1.0
                norm_score = float(raw_score / max_score)

                # Boost multi-word keyphrases slightly as they are more informative (e.g. "language learning")
                boost = 1.0
                if len(words) == 2:
                    boost = 1.25
                elif len(words) == 3:
                    boost = 1.4

                final_score = round(min(1.0, norm_score * boost), 3)
                phrase_type = "unigram" if len(words) == 1 else ("bigram" if len(words) == 2 else "trigram")

                candidates.append({
                    "phrase": phrase.title(),
                    "score": final_score,
                    "type": phrase_type,
                    "word_count": len(words)
                })

            # Sort by score descending
            candidates.sort(key=lambda x: x["score"], reverse=True)

            # Deduplicate near-duplicates (e.g., "Neural Network" and "Convolutional Neural Network")
            deduped = []
            seen_phrases = set()

            for item in candidates:
                p_lower = item["phrase"].lower()
                is_sub = False
                for existing in seen_phrases:
                    if p_lower in existing or existing in p_lower:
                        is_sub = True
                        break
                if not is_sub and p_lower not in seen_phrases:
                    seen_phrases.add(p_lower)
                    deduped.append(item)

                if len(deduped) >= self.top_n:
                    break

            return deduped

        except Exception as e:
            # Fallback regex extraction of capitalized scientific phrases
            phrases = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b", text)
            counts = {}
            for p in phrases:
                p_clean = p.strip()
                words = p_clean.lower().split()
                if any(w in ACADEMIC_STOPWORDS for w in words):
                    continue
                counts[p_clean] = counts.get(p_clean, 0) + 1
            sorted_p = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:self.top_n]
            return [{"phrase": p, "score": 0.85, "type": "keyphrase"} for p, _ in sorted_p]
