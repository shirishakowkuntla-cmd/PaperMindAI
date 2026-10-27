"""
Research Paper Domain Classification Module for PaperMind AI.
Implements deep learning transformer classification (DistilBERT / Zero-Shot)
with lightweight fallback for low-resource environments.
"""

import os
from typing import Dict, List, Tuple, Optional
import numpy as np


# Predefined academic domains aligned with arXiv / IEEE taxonomy
RESEARCH_CATEGORIES = [
    "Artificial Intelligence & Machine Learning",
    "Computer Vision & Pattern Recognition",
    "Natural Language Processing (NLP)",
    "Cybersecurity & Cryptography",
    "Data Science & Big Data Analytics",
    "Robotics & Autonomous Systems",
    "Networks & Distributed Computing"
]

# Domain keywords for semantic centroid alignment and zero-shot labeling
CATEGORY_DESCRIPTIONS = {
    "Artificial Intelligence & Machine Learning": "deep learning, neural networks, reinforcement learning, optimization, supervised learning, transformers, loss function, gradient descent",
    "Computer Vision & Pattern Recognition": "image segmentation, object detection, convolutional neural networks, CNN, visual recognition, video tracking, facial recognition, image classification",
    "Natural Language Processing (NLP)": "language models, text classification, sentiment analysis, translation, word embeddings, tokenization, semantic parsing, summarization, prompt engineering",
    "Cybersecurity & Cryptography": "malware detection, encryption, network security, vulnerability, intrusion detection, cryptography, phishing, blockchain, threat intelligence, penetration testing",
    "Data Science & Big Data Analytics": "data mining, time series analysis, feature engineering, clustering, statistical modeling, database, regression, data visualization, predictive analytics",
    "Robotics & Autonomous Systems": "motion planning, kinematics, trajectory, unmanned vehicles, sensors, SLAM, mobile robots, control theory, actuators, reinforcement learning for robotics",
    "Networks & Distributed Computing": "cloud computing, internet of things, edge computing, wireless networks, 5G, distributed consensus, routing protocols, latency, network traffic"
}


class PaperClassifier:
    """Classifies research papers into academic domains using transformer models."""

    def __init__(self, use_transformer: bool = False, model_name: str = "typeform/distilbert-base-uncased-mnli"):
        self.categories = RESEARCH_CATEGORIES
        self.use_transformer = use_transformer
        self.model_name = model_name
        self.pipeline = None
        self.local_model = self._load_local_model()
        self._init_classifier()

    def _load_local_model(self):
        """Attempts to load pre-trained scikit-learn academic classifier."""
        import joblib
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "classifier_model.joblib")
        if os.path.exists(model_path):
            try:
                return joblib.load(model_path)
            except Exception:
                return None
        return None

    def _init_classifier(self):
        """Attempts to initialize transformer pipeline; falls back gracefully if unavailable."""
        if self.use_transformer:
            try:
                from transformers import pipeline
                # Use a fast, lightweight zero-shot classification pipeline
                self.pipeline = pipeline(
                    "zero-shot-classification",
                    model=self.model_name,
                    device=-1  # CPU-friendly
                )
            except Exception as e:
                # If model download fails or offline, fallback to local/centroid classifier
                self.pipeline = None
                self._init_tfidf_classifier()
        elif self.local_model is None:
            self._init_tfidf_classifier()

    def _init_tfidf_classifier(self):
        """Initialize high-precision TF-IDF and Cosine Centroid classifier."""
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1, 2))
        descriptions = [CATEGORY_DESCRIPTIONS[cat] for cat in self.categories]
        self.centroid_matrix = self.vectorizer.fit_transform(descriptions)

    def classify(self, text: str, title: Optional[str] = None) -> Dict:
        """
        Classifies paper text into research domains.

        Args:
            text: Abstract or combined paper content.
            title: Optional paper title for added signal.

        Returns:
            Dict containing predicted_category, confidence, and all_scores.
        """
        if not text or len(text.strip()) < 10:
            return {
                "predicted_category": "Unknown",
                "confidence": 0.0,
                "all_scores": {cat: 0.0 for cat in self.categories},
                "engine": "none"
            }

        # Combine title and abstract for optimal classification representation
        input_text = f"{title}. {text}" if title else text
        # Truncate to reasonable context window (~1200 characters)
        input_text = input_text[:1200]

        # 1. If Transformer is explicitly requested and initialized
        if self.pipeline is not None:
            try:
                result = self.pipeline(
                    input_text,
                    candidate_labels=self.categories,
                    multi_label=False
                )
                scores = dict(zip(result["labels"], result["scores"]))
                top_category = result["labels"][0]
                top_confidence = float(result["scores"][0])

                return {
                    "predicted_category": top_category,
                    "confidence": top_confidence,
                    "all_scores": scores,
                    "engine": f"Transformer ({self.model_name})"
                }
            except Exception:
                pass

        # 2. Check trained academic classifier
        if self.local_model is not None:
            try:
                pred = self.local_model.predict([input_text])[0]
                classes = self.local_model.classes_
                probs = self.local_model.predict_proba([input_text])[0]
                scores = {cls_name: float(prob) for cls_name, prob in zip(classes, probs)}
                # Ensure all predefined categories are present in scores dict
                for cat in self.categories:
                    if cat not in scores:
                        scores[cat] = 0.0
                confidence = float(np.max(probs))

                return {
                    "predicted_category": pred,
                    "confidence": confidence,
                    "all_scores": scores,
                    "engine": "Supervised Academic Domain Classifier (TF-IDF + Softmax Logistic Model)"
                }
            except Exception:
                pass

        # 3. Fallback to centroid classifier
        return self._classify_tfidf(input_text)

    def _classify_tfidf(self, input_text: str) -> Dict:
        """Cosine similarity against category feature centroids."""
        if not hasattr(self, "vectorizer"):
            self._init_tfidf_classifier()

        from sklearn.metrics.pairwise import cosine_similarity

        vec = self.vectorizer.transform([input_text])
        similarities = cosine_similarity(vec, self.centroid_matrix)[0]

        # Apply softmax-like normalization to similarities
        exp_sim = np.exp(similarities * 5)
        probs = exp_sim / np.sum(exp_sim)

        scores = {self.categories[i]: float(probs[i]) for i in range(len(self.categories))}
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return {
            "predicted_category": sorted_scores[0][0],
            "confidence": sorted_scores[0][1],
            "all_scores": scores,
            "engine": "TF-IDF Semantic Matcher (Zero-Download Baseline)"
        }
