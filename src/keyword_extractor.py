"""
Keyword and Concept Extraction Module for PaperMind AI.
Extracts unigram, bigram, and trigram keyphrases using TF-IDF and syntactic heuristics.
"""

import re
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer


# Custom academic stop words to filter out generic scientific filler
ACADEMIC_STOPWORDS = {
    "paper", "study", "research", "results", "using", "proposed", "method", "methods", "approach",
    "based", "data", "model", "models", "presents", "show", "shows", "author", "authors", "work",
    "et", "al", "figure", "table", "section", "demonstrate", "demonstrates", "evaluated", "performance",
    "different", "various", "existing", "well", "state", "art", "significantly", "respectively", "higher",
    "compared", "following", "given", "number", "case", "order", "furthermore", "however", "therefore"
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

        # Combine title (given higher weight by repeating) and main text
        weighted_corpus = f"{title} {title} {text}"

        try:
            vectorizer = TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 3),
                max_df=0.85,
                min_df=1,
                token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9_\-]{2,}\b"
            )

            tfidf_matrix = vectorizer.fit_transform([weighted_corpus])
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]

            # Filter candidates
            candidates = []
            for phrase, score in zip(feature_names, scores):
                words = phrase.split()

                # Filter if all words are academic generic stopwords
                if all(w in ACADEMIC_STOPWORDS for w in words):
                    continue

                # Filter single letter words or purely numeric tokens
                if any(len(w) < 3 for w in words):
                    continue

                # Boost multi-word keyphrases slightly as they are more informative (e.g. "convolutional neural network")
                boost = 1.0
                if len(words) == 2:
                    boost = 1.25
                elif len(words) == 3:
                    boost = 1.35

                final_score = float(score * boost)
                phrase_type = "unigram" if len(words) == 1 else ("bigram" if len(words) == 2 else "trigram")

                candidates.append({
                    "phrase": phrase.title(),
                    "score": round(final_score, 4),
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
                # Check for direct overlap with already chosen
                is_sub = False
                for existing in seen_phrases:
                    if p_lower in existing or existing in p_lower:
                        # Allow if score is close, otherwise skip redundant shorter variant
                        if item["score"] < 0.7 * [x["score"] for x in deduped if x["phrase"].lower() == existing][0]:
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
                counts[p] = counts.get(p, 0) + 1
            sorted_p = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:self.top_n]
            return [{"phrase": p, "score": 1.0, "type": "phrase"} for p, _ in sorted_p]
