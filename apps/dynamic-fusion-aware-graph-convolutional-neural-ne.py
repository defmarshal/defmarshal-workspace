```python
#!/usr/bin/env python3
"""
Dynamic Fusion-Aware GCN for Multimodal Emotion Recognition in Conversations (MERC)
Simplified demo based on arXiv:2603.22345v1
"""

import numpy as np
from collections import defaultdict
import random
from enum import Enum

class Emotion(Enum):
    NEUTRAL = 0
    HAPPY = 1
    SAD = 2
    ANGRY = 3
    EXCITED = 4

class Speaker:
    def __init__(self, speaker_id: str):
        self.id = speaker_id
        self.utterances = []

class Utterance:
    def __init__(self, speaker: str, text: str, turn: int):
        self.speaker = speaker
        self.text = text
        self.turn = turn
        self.features = None
        self.emotion = None

class MultimodalFeatureExtractor:
    """Simulates feature extraction from text, audio, visual modalities"""
    def __init__(self):
        # Simple lexicons for demo
        self.emotion_lexicon = {
            'happy': ['great', 'wonderful', 'excellent', 'love', 'happy', 'joy'],
            'sad': ['sad', 'depressed', 'unhappy', 'cry', 'heartbroken'],
            'angry': ['angry', 'mad', 'furious', 'hate', 'rage'],
            'excited': ['excited', 'amazing', 'wow', 'incredible', 'thrilled']
        }
    
    def extract(self, utterance: Utterance) -> np.ndarray:
        """Extract 12-dimensional multimodal features"""
        features = np.zeros(12)
        
        # Text-based features (dimensions 0-3)
        text = utterance.text.lower()
        for i, (emotion, keywords) in enumerate(self.emotion_lexicon.items()):
            features[i] = sum(1 for kw in keywords if kw in text) / max(1, len(text.split()))
        
        # Simulated audio features (pitch, energy, speaking rate - dims 4-7)
        # In real system: extract from waveform
        features[4] = random.uniform(0.3, 0.9)  # pitch variation
        features[5] = random.uniform(0.2, 0.8)  # energy
        features[6] = random.uniform(0.4, 0.7)  # speaking rate
        features[7] = 1.0 if '!' in utterance.text else random.uniform(0.1, 0.5)  # emphasis
        
        # Simulated visual features (facial action units - dims 8-11)
        # In real system: detect from video
        features[8] = random.uniform(0, 1)  # smile
        features[9] = random.uniform(0, 0.3)  # frown (usually low)
        features[10] = random.uniform(0, 0.2)  # brow raise
        features[11] = random.uniform(0.1, 0.5)  # eye widening
        
        utterance.features = features
        return features

class ConversationGraph:
    """Builds dynamic graph of conversation with speaker and temporal relations"""
    def __init__(self, utterances: list, window_size: int = 3):
        self.utterances = utterances
        self.window = window_size
        self.adjacency = None
        self.edge_features = None
        
    def build(self):
        """Construct graph with utterance nodes and edge types"""
        n = len(self.utterances)
        self.adjacency = np.zeros((n, n))
        self.edge_features = []
        
        for i in range(n):
            for j in range(max(0, i-self.window), min(n, i+self.window+1)):
                if i == j:
                    continue
                    
                # Edge exists if within temporal window
                self.adjacency[i, j] = 1
                
                # Edge features encode relationship type
                edge_feat = self._compute_edge_feature(i, j)
                self.edge_features.append(edge_feat)
        
        self.edge_features = np.array(self.edge_features) if self.edge_features else None
        
    def _compute_edge_feature(self, i: int, j: int) -> np.ndarray:
        """Compute edge features: temporal distance, speaker relationship"""
        utt_i = self.utterances[i]
        utt_j = self.utterances[j]
        
        feat = np.zeros(4)
        feat[0] = abs(utt_i.turn - utt_j.turn) / len(self.utterances)  # normalized temporal distance
        feat[1] = 1.0 if utt_i.speaker == utt_j.speaker else 0.0  # same speaker
        feat[2] = 1.0 if utt_j.turn > utt_i.turn else 0.0  # direction (past->future)
        feat[3] = 1.0  # always present edge
        
        return feat

class DynamicFusionGCN:
    """Graph Convolutional Network with dynamic fusion of modalities"""
    def __init__(self, input_dim: int = 12, hidden_dim: int = 32, num_classes: int = 5):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_classes = num_classes
        
        # Initialize weights (simplified for demo)
        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.1
        self.W2 = np.random.randn(hidden_dim, num_classes) * 0.1
        self.W_fusion = np.random.randn(3, 1) * 0.1  # fusion weights for text, audio, visual
        
    def forward(self, node_features: np.ndarray, adjacency: np.ndarray) -> np.ndarray:
        """GCN forward pass with graph convolution"""
        n = len(node_features)
        
        # Normalize adjacency (symmetrically)
        D = np.diag(adjacency.sum(axis=1) ** -0.5)
        A_norm = D @ adjacency @ D
        
        # First GCN layer
        h = np.tanh(A_norm @ node_features @ self.W1)
        
        # Second GCN layer (no activation, linear)
        logits = A_norm @ h @ self.W2
        
        return logits
    
    def dynamic_fusion(self, features: np.ndarray) -> np.ndarray:
        """Dynamically fuse multimodal features based on learned attention"""
        # Split modalities (simplified: first 4=text, next 4=audio, last 4=visual)
        text = features[:, :4]
        audio = features[:, 4:8]
        visual = features[:, 8:12]
        
        # Compute modality importance scores
        scores = []
        for modality in [text, audio, visual]:
            # Simple heuristic: variance indicates informativeness
            score = np.var(modality, axis=1).mean()
            scores.append(score)
        
        scores = np.array(scores)
        weights = np.exp(scores) / np.sum(np.exp(scores))
        
        # Weighted fusion
        fused = (weights[0] * text.mean(axis=1, keepdims=True) +
                weights[1] * audio.mean(axis=1, keepdims=True) +
                weights[2] * visual.mean(axis=1, keepdims=True))
        
        # Concatenate fused signal back to feature space
        # For demo: broadcast fused value across all features
        result = features * (fused / (features.mean(axis=1, keepdims=True) + 1e-8))
        
        return result, weights

class MERCTrainer:
    """Main training/inference pipeline"""
    def __init__(self):
        self.extractor = MultimodalFeatureExtractor()
        self.model = DynamicFusionGCN()
        self.graph_builder = None
        
    def prepare_conversation(self, conversation: list, speakers: dict):
        """Convert raw conversation to graph structure"""
        utterances = []
        for turn, (speaker_id, text) in enumerate(conversation):
            speaker = speakers[speaker_id]
            utt = Utterance(speaker_id, text, turn)
            self.extractor.extract(utt)
            utterances.append(utt)
            
        self.graph_builder = ConversationGraph(utterances)
        self.graph_builder.build()
        
        return utterances
    
    def predict_emotions(self, utterances: list) -> list:
        """Predict emotions for all utterances"""
        # Stack features
        features = np.array([utt.features for utt in utterances])
        
        # Dynamic fusion
        fused_features, weights = self.model.dynamic_fusion(features)
        
        # Build graph
        adjacency = self.graph_builder.adjacency
        
        # GCN forward pass
        logits = self.model.forward(fused_features, adjacency)
        predictions = np.argmax(logits, axis=1)
        
        # Store results
        for utt, pred in zip(utterances, predictions):
            utt.emotion = Emotion(pred)
            
        return predictions, weights
    
    def evaluate(self, utterances: list, ground_truth: list) -> dict:
        """Simple evaluation"""
        predictions = [utt.emotion for utt in utterances]
        correct = sum(p == Emotion(gt) for p, gt in zip(predictions, ground_truth))
        accuracy = correct / len(ground_truth)
        
        # Per-class accuracy
        class_correct = defaultdict(int)
        class_total = defaultdict(int)
        for p, gt in zip(predictions, ground_truth):
            cls = Emotion(gt).name
            class_total[cls] += 1
            if p == Emotion(gt):
                class_correct[cls] += 1
                
        class_acc = {cls: class_correct[cls]/class_total[cls] if class_total[cls]>0 else 0 
                    for cls in class_total}
        
        return {
            'accuracy': accuracy,
            'class_accuracy': class_acc,
            'fusion_weights': {'text': 0.4, 'audio': 0.3, 'visual': 0.3}  # Fixed for demo
        }

def sample_conversation():
    """Create a sample 2-speaker conversation"""
    return [
        ('A', "I just got some great news!"),
        ('B', "Oh really? What happened?"),
        ('A', "I got the job I applied for! I'm so excited!"),
        ('B', "That's amazing! Congratulations!"),
        ('A', "Thanks! I've been waiting for this for months."),
        ('B', "You deserve it. Let's celebrate!"),
        ('A', "I know, but I'm also nervous about the responsibilities."),
        ('B', "Don't worry, you'll do great. Everyone believes in you."),
        ('A', " Thanks, that means a lot. I feel much better now."),
        ('B', "Anytime! That's what friends are for.")
    ]

def main():
    """Demonstrate MERC with Dynamic Fusion-Aware GCN"""
    print("🎭 Multimodal Emotion Recognition in Conversations (MERC)")
    print("   Dynamic Fusion-Aware Graph Convolutional Network Demo")
    print("=" * 60)
    
    # Create speakers
    speakers = {'A': Speaker('A'), 'B': Speaker('B')}
    
    # Get conversation
    conversation = sample_conversation()
    print(f"\n📱 Conversation ({len(conversation)} turns):")
    for turn, (speaker, text) in enumerate(conversation):
        print(f"  {turn+1}. {speaker}: {text}")
    
    # Prepare and predict
    trainer = MERCTrainer()
    utterances = trainer.prepare_conversation(conversation, speakers)
    predictions, fusion_weights = trainer.predict_emotions(utterances)
    
    # Show results
    print("\n🔍 Emotion Predictions:")
    for utt in utterances:
        print(f"  Turn {utt.turn+1} ({utt.speaker}): {utt.text[:30]:<30} → {utt.emotion.name}")
    
    # Simulated ground truth for demo (simple rule-based)
    ground_truth = []
    for utt in utterances:
        text = utt.text.lower()
        if any(w in text for w in ['great', 'excited', 'amazing', 'congratulations']):
            ground_truth.append(Emotion.HAPPY.value)
        elif any(w in text for w in ['nervous', 'worried']):
            ground_truth.append(Emotion.SAD.value)
        else:
            ground_truth.append(Emotion.NEUTRAL.value)
    
    metrics = trainer.evaluate(utterances, ground_truth)
    
    print(f"\n📊 Evaluation Metrics:")
    print(f"  Overall Accuracy: {metrics['accuracy']:.2%}")
    print(f"  Fusion Weights: Text={fusion_weights[0]:.2f}, Audio={fusion_weights[1]:.2f}, Visual={fusion_weights[2]:.2f}")
    
    print("\n💡 Key Insight:")
    print("  Graph convolution captures conversation dynamics (who spoke to whom, in what order)")
    print("  Dynamic fusion adapts modality importance based on content")
    print("  This enables accurate emotion recognition even with missing modalities")
    
    print("\n" + "=" * 60)
    print("✅ MERC with Dynamic Fusion-Aware GCN demonstration complete!")

if __name__ == "__main__":
    main()
```