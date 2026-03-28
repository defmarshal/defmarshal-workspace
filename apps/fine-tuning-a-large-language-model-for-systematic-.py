```python
#!/usr/bin/env python3
"""
Fine-Tuning Demonstration: Systematic Review Screening with LLM
Simulates training an LLM-based classifier to screen research papers.
"""

import json
import random
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score

# Simulated dataset: titles and abstracts with inclusion/exclusion labels
# In practice, this would be thousands of real papers labeled by human reviewers
DATASET = [
    {
        "title": "Deep Learning for Chest X-Ray Diagnosis",
        "abstract": "We propose a CNN architecture for automated detection of pneumonia from chest X-rays. Our model achieves 96% accuracy on a dataset of 10,000 images.",
        "included": True
    },
    {
        "title": "A Novel Approach to Sentiment Analysis",
        "abstract": "This paper presents a new method for sentiment classification using BERT embeddings. We evaluate on movie reviews and show improved F1 scores.",
        "included": False  # Not relevant to systematic review topic
    },
    {
        "title": "Machine Learning in Healthcare: A Systematic Review",
        "abstract": "We review 200 studies applying ML to medical diagnosis, discussing challenges in interpretability, data quality, and clinical deployment.",
        "included": True
    },
    {
        "title": "Optimizing Database Query Performance",
        "abstract": "We introduce a new indexing technique for PostgreSQL that reduces query latency by 30% in benchmark tests.",
        "included": False
    },
    {
        "title": "Federated Learning for Privacy-Preserving Cancer Detection",
        "abstract": " Hospitals collaborate to train a deep learning model for cancer detection without sharing patient data. Our approach maintains 95% accuracy compared to centralized training.",
        "included": True
    },
    {
        "title": "Blockchain for Supply Chain Transparency",
        "abstract": "We propose a blockchain-based system to track goods through the supply chain, improving traceability and reducing fraud.",
        "included": False
    },
    {
        "title": "Natural Language Processing for Clinical Notes",
        "abstract": "We develop a transformer model to extract medical conditions from unstructured clinical notes, achieving state-of-the-art results on the i2b2 dataset.",
        "included": True
    },
    {
        "title": "Reinforcement Learning for Game Playing",
        "abstract": "Our new RL algorithm achieves superhuman performance on Atari games using less training data than previous methods.",
        "included": False
    },
    {
        "title": "Explainable AI for Medical Imaging",
        "abstract": "We use Grad-CAM and SHAP values to interpret deep neural network decisions in radiology, helping radiologists understand model predictions.",
        "included": True
    },
    {
        "title": "Cloud Computing Cost Optimization",
        "abstract": "We present a scheduling algorithm that reduces cloud infrastructure costs by 25% while maintaining performance SLAs.",
        "included": False
    }
]

def prepare_dataset(data: List[dict]) -> Tuple[List[str], List[int]]:
    """Convert dataset to text features and binary labels."""
    texts = []
    labels = []
    for item in data:
        # Combine title and abstract for screening
        text = f"{item['title']} {item['abstract']}"
        texts.append(text)
        labels.append(1 if item['included'] else 0)
    return texts, labels

def train_screening_model(texts: List[str], labels: List[int]) -> tuple:
    """Train a simple TF-IDF + Logistic Regression model."""
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2)
    )
    X = vectorizer.fit_transform(texts)
    
    model = LogisticRegression(
        class_weight='balanced',  # Handle class imbalance
        max_iter=1000,
        random_state=42
    )
    model.fit(X, labels)
    
    return vectorizer, model

def screen_paper(vectorizer, model, title: str, abstract: str) -> dict:
    """Screen a new paper and return decision with confidence."""
    text = f"{title} {abstract}"
    features = vectorizer.transform([text])
    prob = model.predict_proba(features)[0]
    prediction = model.predict(features)[0]
    
    return {
        "include": bool(prediction),
        "confidence": float(prob[prediction]),
        "reason": "Relevant to systematic review topic" if prediction else "Not relevant"
    }

def show_feature_importance(vectorizer, model, top_n: int = 10):
    """Show most important features for inclusion/exclusion decisions."""
    feature_names = vectorizer.get_feature_names_out()
    coefficients = model.coef_[0]
    
    # Get top positive (include) and negative (exclude) features
    sorted_indices = coefficients.argsort()
    top_include = [(feature_names[i], coefficients[i]) for i in sorted_indices[-top_n:]][::-1]
    top_exclude = [(feature_names[i], coefficients[i]) for i in sorted_indices[:top_n]]
    
    print("\nTop Features Predicting INCLUSION:")
    for word, weight in top_include:
        print(f"  {word:20} {weight:+.3f}")
    
    print("\nTop Features Predicting EXCLUSION:")
    for word, weight in top_exclude:
        print(f"  {word:20} {weight:+.3f}")

def main():
    """Demonstrate fine-tuning for systematic review screening."""
    print("=" * 70)
    print("SYSTEMATIC REVIEW SCREENING: LLM FINE-TUNING DEMO")
    print("=" * 70)
    print()
    
    # 1. Prepare data
    texts, labels = prepare_dataset(DATASET)
    print(f"[1] Dataset: {len(texts)} papers ({sum(labels)} included, {len(labels)-sum(labels)} excluded)")
    
    # 2. Split and train
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.3, random_state=42, stratify=labels
    )
    
    print(f"[2] Training on {len(X_train)} papers, testing on {len(X_test)}")
    
    vectorizer, model = train_screening_model(X_train, y_train)
    print("[3] Model trained: TF-IDF + Logistic Regression")
    
    # 3. Evaluate
    X_test_vec = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_vec)
    
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    print("\n[4] Performance on Test Set:")
    print(f"    Precision: {precision:.2%}")
    print(f"    Recall:    {recall:.2%}")
    print(f"    F1 Score:  {f1:.2%}")
    
    # 4. Show important features
    show_feature_importance(vectorizer, model)
    
    # 5. Demonstrate screening new papers
    print("\n[5] Screening New Papers:")
    new_papers = [
        {
            "title": "AI for Drug Discovery: A Comprehensive Review",
            "abstract": "We survey recent advances in using artificial intelligence for drug repurposing and novel compound design, covering deep learning, reinforcement learning, and generative models."
        },
        {
            "title": "Efficient Sorting Algorithms for Large Datasets",
            "abstract": "We present a new quicksort variant that reduces worst-case complexity through pivot selection heuristics and cache-aware partitioning."
        }
    ]
    
    for paper in new_papers:
        result = screen_paper(vectorizer, model, paper["title"], paper["abstract"])
        status = "✅ INCLUDE" if result["include"] else "❌ EXCLUDE"
        print(f"\n  {status}")
        print(f"  Title: {paper['title']}")
        print(f"  Confidence: {result['confidence']:.1%}")
        print(f"  Reason: {result['reason']}")
    
    print("\n" + "=" * 70)
    print("KEY CONCEPTS DEMONSTRATED:")
    print("  • Text vectorization (TF-IDF) for paper representations")
    print("  • Binary classification for screening decisions")
    print("  • Handling class imbalance (fewer included papers)")
    print("  • Feature interpretation (what words predict inclusion?)")
    print("  • Applying trained model to new submissions")
    print("\nIn a real system, you would:")
    print("  • Use thousands of labeled papers")
    print("  • Fine-tune a large language model (LLaMA, GPT, etc.)")
    print("  • Incorporate metadata (year, journal, study design)")
    print("  • Use active learning to prioritize uncertain papers")
    print("  • Implement human-in-the-loop validation")
    print("=" * 70)

if __name__ == "__main__":
    random.seed(42)
    main()
```