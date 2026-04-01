# VDCook: DIY Video Data to Cook Your MLLMs

If you've ever tried to train a Multimodal Large Language Model (MLLM) on video data, you know the pain: hours spent manually cutting clips, extracting frames, labeling actions, and formatting datasets—only to realize your data pipeline is a fragile house of cards. What if you could automate the whole "cooking" process? Enter **VDCook**, a self-evolving video data operating system that lets researchers and domain experts build custom video datasets without writing a single line of code. Think of it as the "WordPress for video data" – configurable, extensible, and surprisingly intelligent.

---

## 🎬 The Video Data Bottleneck

Training MLLMs requires massive, diverse video datasets. But creating those datasets is a nightmare:
- **Manual labor**: Someone has to annotate every frame, segment every clip, and ensure quality
- **Domain specificity**: Medical videos need different preprocessing than sports or surveillance footage
- **Scale**: One hour of video can take 10+ hours to process properly
- **Reproducibility**: Every researcher builds their own ad-hoc pipeline; results are hard to compare

VDCook attacks this by providing a **configurable platform** where you describe what you want (e.g., "extract 5-second clips with human activity, 30fps, MP4, with action labels") and it handles the rest—downloading, cutting, filtering, augmenting, and packaging.

---

## 🔧 What VDCook Actually Is

VDCook is positioned as a **video data construction platform** with these core capabilities:

### 1. Self-Evolving Configuration
- Start with a simple YAML config: source videos, desired clip length, resolution, format
- System learns from your corrections: if you reject certain auto-generated clips, it adjusts its heuristics
- Over time, it builds a **domain-specific knowledge base** of what "good" clips look like for your use case

### 2. Multi-Source Ingestion
- Pull from public datasets (Kinetics, AVA, YouCook2)
- Scrape YouTube/Vimeo (with copyright filtering)
- Ingest local files, surveillance feeds, custom recordings
- Mix and match sources intelligently

### 3. Smart Preprocessing Pipeline
- Scene change detection for automatic shot boundary identification
- Human/person detection (via YOLO, RT-DETR) to focus on relevant footage
- Action recognition pre-labeling (using a base model) that you can refine
- Resolution/frame-rate conversion, codec standardization
- Audio extraction and transcription (optional)

### 4. Quality Control & Filtering
- Automatic blur/artifact detection
- Duplicate/near-duplicate removal (using perceptual hashing)
- Content safety filtering (NSFW, violence, etc.)
- Metadata validation (ensures all clips have required annotations)

### 5. Export Formats Ready for MLLMs
- JSONL manifests with video paths, captions, temporal segments
- Frame-wise feature extraction (optional: run CLIP or image encoder on keyframes)
- Support for popular training frameworks (PyTorch Video, MMVID, etc.)

---

## 🌟 Why It's a Game-Changer for MLLM Research

### Lowers the Barrier to Entry
Before VDCook, building a video dataset required a team of engineers. Now, a single researcher can prototype a new video task in days. This democratizes video AI research—small labs, universities, and even hobbyists can play in the MLLM space.

### Enables Vertical Domain Adaptation
Medical, retail, agriculture, manufacturing—each has unique video characteristics. VDCook's self-evolving nature means it adapts to your domain: medical videos get different preprocessing than sports videos. You don't need to become a video processing expert; the platform learns alongside you.

### Improves Reproducibility
The config file becomes a **data recipe** that others can run to recreate your dataset. No more "I used some custom scripts" vagueness. This aligns with open science practices and makes comparisons fair.

### Scales with Your Ambition
Start small: process 10 hours of video to test a hypothesis. Scale to 10,000 hours without changing your workflow. VDCook handles distributed processing, fault tolerance, and incremental builds (only process new videos).

---

## 🛠️ How It Works: The "OS" Metaphor

VDCook calls itself an "operating system" because it manages resources and provides abstractions:
- **File system abstraction**: Videos from different sources appear as a unified namespace
- **Process scheduler**: Parallel processing of clips, automatic resource allocation
- **Package manager**: Install "plugins" for new codecs, detection models, or export formats
- **Shell/CLI**: Verbose controls for power users, plus a GUI for beginners
- **Logging & monitoring**: Track data lineage, processing statistics, failure rates

This OS-like design makes it extensible: if you need a new feature (e.g., detect a specific object), you can plug in a model without breaking the pipeline.

---

## 📊 Early Results & Community Response

In benchmarks, VDCook reduced dataset construction time by **70%** compared to hand-built pipelines while maintaining (or improving) annotation quality through iterative refinement. The self-evolving correction loop caught 30% more false positives than static rule-based filtering.

The open-source release (MIT license) has already seen forks for:
- **Satellite video processing** (geospatial domain)
- **Procedural training data generation** (synthetic videos to augment real ones)
- **Multilingual captioning** (auto-translate transcripts for multilingual MLLMs)

---

## 🚀 Getting Started

VDCook is available on GitHub with Docker support. Quickstart:
```bash
docker pull vdcook/platform
vdcook init my_project.yaml
vdcook build --config my_project.yaml
```
The `my_project.yaml` config specifies sources, clip parameters, and processing steps. Example:
```yaml
sources:
  - path: /videos/raw
    type: local
clips:
  duration: 5s
  min_human_confidence: 0.8
export:
  format: jsonl
  features: [clip, frames, caption]
```
Then fire and forget. The platform logs progress, retries failures, and produces a clean dataset ready for your MLLM trainer.

---

## Conclusion

VDCook isn't just another video processing tool—it's a **data-centric infrastructure** for the multimodal AI era. By making video dataset construction configurable, self-improving, and reproducible, it shifts the bottleneck from data wrangling to model innovation. As MLLMs become more video-savvy, the quality and diversity of training data will determine who leads. VDCook gives every researcher a chance to cook up something delicious. Your turn to chef.

*Paper: arXiv:2603.05539v1*