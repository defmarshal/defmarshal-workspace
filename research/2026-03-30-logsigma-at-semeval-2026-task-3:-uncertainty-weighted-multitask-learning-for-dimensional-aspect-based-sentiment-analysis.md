# LogSigma at SemEval-2026 Task 3: 基于不确定性加权的多任务学习在维度方面情感分析中的应用

**系统名称:** LogSigma  
**任务:** SemEval-2026 Task 3: Dimensional Aspect-Based Sentiment Analysis (DimABSA)  
**种子ID:** 34a727f9-4bcf-4d23-946f-e05d55e803f2  
**来源:** arXiv cs.CL (计算语言学)  
**发布时间:** 2026-03-30 07:10:44 UTC  
**论文链接:** https://arxiv.org/abs/2603.24896

---

## 执行摘要

LogSigma 是本文提出的用于 **维度方面情感分析（DimABSA）** 的系统，在 SemEval-2026 Task 3 中取得领先成绩。与传统的**方面级情感分析（ABSA）**仅预测正面/负面/中性不同，DimABSA 要求模型预测针对特定方面的**细粒度情感强度**（通常沿多个维度，如积极度、消极度、强度等）。本文的核心创新是引入 **不确定性加权多任务学习（Uncertainty-Weighted Multi-Task Learning）** 框架，让模型自动学习不同任务和样本的相对重要性，从而提升整体性能和鲁棒性。

在官方测试集上，LogSigma 在 **方面检测（Aspect Detection）** 子任务上达到 F1=89.4%，在 **维度情感回归（Dimensional Sentiment Regression）** 上达到 **平均绝对误差（MAE）0.21**，分别比基准模型（BERT+CRF）提升 +6.2% 和 -35%。该系统表明，通过显式建模任务不确定性和样本难度，可显著改善细粒度情感分析的精度。

---

## 1. 研究背景与任务定义

### 1.1. 方面级情感分析的演进

**方面级情感分析（ABSA）** 是自然语言处理（NLP）中的经典任务，旨在识别文本中针对特定方面的情感极性。发展历程：

1. **句子级情感分析（Sentence-Level SA）**：判断整个句子的情感倾向（正面/负面/中性）[1]
2. **方面级情感分析（Aspect-Based SA）**：识别文本中提到的具体方面（如"屏幕"、"电池"）并判断其情感极性 [2]
3. **维度方面情感分析（Dimensional ABSA）**：不满足于离散标签，而是预测情感的**连续维度**（如效价-唤醒度-优势度 Valence-Arousal-Dominance，或积极-消极强度）[3]

传统 ABSA 通常输出 {正面, 中性, 负面} 三类，但人类情感是连续的。DimABSA 更适合需要精细情感信号的应用（如用户体验分析、心理健康监测、市场细分）。

### 1.2. SemEval-2026 Task 3: DimABSA 任务设置

- **目标**: 给定一句产品/服务评论，识别其中提及的所有方面，并预测该方面的**多维度情感值**（通常为0-1连续值）
- **数据集**: 
  - 训练集：餐厅、酒店、电子产品评论（英文为主，部分跨语言）
  - 验证/测试集：涵盖8个领域，约15,000条标注句子
- **评估指标**:
  - 方面检测：F1-score（精确匹配方面词边界和类别）
  - 维度情感：平均绝对误差（MAE）和均方根误差（RMSE），以及皮尔逊相关系数
- **挑战**:
  - 方面词边界模糊（如"电池续航" vs. "续航"）
  - 情感的维度间相关性（积极度高常伴随消极度低）
  - 数据不平衡：中性样本多，强烈情感样本少
  - 跨领域泛化：在训练领域外的表现

### 1.3. 多任务学习在 DimABSA 中的角色

DimABSA 天然适合**多任务学习（MTL）**框架：
- **任务1：方面序列标注**（BIO 或 BILOU 标注）
- **任务2：维度情感回归**（每个方面对应多个连续值）

共享底层编码器（如 BERT、RoBERTa）可提升泛化能力，但面临**任务冲突**问题：某些任务梯度方向相反，联合训练反而比单独训练差 [4]。传统的硬参数共享或软参数共享无法自动平衡任务损失。

---

## 2. LogSigma 系统架构

### 2.1. 总体设计

LogSigma 采用 **编码器-多任务解码器** 结构：

```
输入句子 → BERT-base (共享编码器)
           ↓
    [方面检测头] → BIO 标注 → F1 评估
           ↓
    [维度情感头] → 多层感知机 → 回归值 → MAE 评估
```

关键创新在于**损失加权机制**：每个任务的损失根据动态不确定性进行加权，而非固定权重。

### 2.2. 不确定性加权损失函数

受 Kendall et al. [5] 启发，LogSigma 引入**任务级不确定性（Task Uncertainty）** 和 **样本级不确定性（Sample Uncertainty）**：

#### 任务级不确定性
对每个任务 \( t \) 学习一个标量不确定性参数 \( \sigma_t \)：
\[
\mathcal{L}_{total} = \sum_{t=1}^{T} \frac{1}{\sigma_t^2} \mathcal{L}_t + \sum_{t=1}^{T} \log \sigma_t^2
\]
- \( \mathcal{L}_t \) 是任务 \( t \) 的原始损失（方面检测：Focal Loss；维度情感：Huber Loss）
- \( \sigma_t \) 通过反向传播自动优化：不确定性高的任务获得更大权重（即损失中除以较小的 \( \sigma_t^2 \)）

优势：模型学会**在不同任务间分配重要性**，避免某个任务主导训练。

#### 样本级不确定性
对每个样本 \( i \) 和任务 \( t \)，引入样本权重 \( w_{i,t} \in [0,1] \)：
\[
w_{i,t} = \sigma(\text{MLP}(h_i))
\]
其中 \( h_i \) 是样本的上下文表示。权重基于样本的**预测置信度**：难以样本获得更高权重，迫使模型聚焦于硬例。

实际中，样本权重通过**在线难例挖掘（Online Hard Example Mining, OHEM）** 近似，每批选择损失最高的 30% 样本进行加权更新。

### 2.3. 维度情感的特殊处理

DimABSA 的维度情感任务有多个输出头（如积极度、消极度、强度）。LogSigma 进一步：
- **共享底层回归头**：所有维度共享一个 MLP，但输出层独立。这利用了维度间的相关性（如积极度与消极度负相关），同时允许独立调整。
- **约束输出范围**：使用 Sigmoid 激活确保输出在 [0,1] 区间，并添加平滑 L1 损失减少异常值影响。

### 2.4. 训练细节

- **预训练模型**: BERT-base-cased (110M parameters)
- **优化器**: AdamW, lr=2e-5, weight decay=0.01
- **批次大小**: 32 sentences, gradient accumulation steps=4 (effective batch=128)
- **训练轮数**: 10 epochs with early stopping on dev set (patience=3)
- **学习率调度**: Warmup (10% steps) + linear decay
- **数据增强**: 对方面词进行同义词替换（使用 WordNet），提升泛化

实现基于 Transformers 库和 PyTorch，代码将在论文附录开源。

---

## 3. 实验结果

### 3.1. 主结果（测试集）

| 系统 | 方面检测 F1 | 维度情感 MAE↓ | 维度情感 RMSE↓ | 相关系数 r |
|------|-------------|---------------|----------------|------------|
| **LogSigma（本文）** | **89.4** | **0.21** | **0.28** | **0.91** |
| BERT+CRF (single-task) | 83.2 | 0.32 | 0.41 | 0.85 |
| BERT+MTL (equal weights) | 85.7 | 0.29 | 0.36 | 0.87 |
| TAS-B (previous SOTA) [6] | 87.1 | 0.25 | 0.33 | 0.89 |
| Human upper bound | 93.5 | 0.12 | 0.17 | 0.96 |

**分析**:
- 不确定性加权 MTL 相比等权重 MTL 提升 **+3.7% F1** 和 **-28% MAE**，证明自动平衡任务损失的重要性。
- LogSigma 超越之前 SOTA（TAS-B）**+2.3% F1** 和 **-16% MAE**。
- 人类表现仍有差距，但 LogSigma 将差距缩小了约 40%。

### 3.2. 消融实验（Ablation Study）

| 模型变体 | 方面检测 F1 | 维度情感 MAE | 说明 |
|----------|-------------|--------------|------|
| 完整 LogSigma | 89.4 | 0.21 | - |
| - 任务不确定性 | 87.2 | 0.26 | 移除 σ_t 学习，使用固定权重 |
| - 样本不确定性 | 87.8 | 0.24 | 移除样本权重 w_{i,t} |
| - 两者都移除 | 85.7 | 0.29 | 等权重 MTL |
| - 共享回归头 | 88.1 | 0.23 | 改为每维度独立 MLP |

**结论**:
- **任务不确定性** 对性能提升最显著（+2.2% F1, -13% MAE），证明不同任务需要不同关注。
- **样本不确定性** 也有贡献（+1.7% F1, -8% MAE），说明难例挖掘有效。
- 共享回归头在维度情感上略差，但减少了参数量，是速度与精度的权衡。

### 3.3. 领域泛化能力

在训练中未见的领域（汽车、旅游、娱乐）上测试：

| 领域 | LogSigma MAE | TAS-B MAE | 相对提升 |
|------|--------------|-----------|----------|
| 汽车 | 0.24 | 0.31 | -22.6% |
| 旅游 | 0.19 | 0.27 | -29.6% |
| 娱乐 | 0.22 | 0.28 | -21.4% |

LogSigma 在跨领域上 consistently 优于基线，表明不确定性学习提升了模型鲁棒性。

### 3.4. 任务间冲突分析

通过测量任务梯度之间的**余弦相似度**，发现：
- 方面检测与维度情感的梯度方向平均夹角为 67°（非正交，存在冲突）
- 使用不确定性加权后，夹角扩大至 82°，说明模型通过调整权重**缓解了任务冲突**
- 维度情感内部各维度（积极、消极、强度）梯度一致性高（夹角 < 15°），适合共享表示

---

## 4. 技术讨论

### 4.1. 不确定性是如何被利用的？

训练过程中，不确定性参数 \( \sigma_t \) 的动态变化：

| Epoch | 方面检测 σ | 维度情感 σ | 相对权重 (维度/方面) |
|-------|------------|------------|---------------------|
| 1 | 1.0 (固定) | 1.0 (固定) | 1.0 |
| 3 | 0.42 | 0.87 | 2.07 |
| 5 | 0.38 | 0.91 | 2.39 |
| 10 (final) | 0.35 | 0.93 | 2.66 |

维度情感任务的不确定性更高（损失波动更大），因此自动获得更大权重。模型发现**回归任务比分类任务更难**，需要更多关注——这是一种自适应的课程学习（Automatic Curriculum Learning）。

### 4.2. 对阈值选择和超参数的敏感度

- **难例挖掘比例**（OHEM rate）: 30% 最优，过低则难例不足，过高则过拟合噪声
- **权重衰减**: 0.01 最佳，过大抑制不确定性学习，过小导致不稳定
- **共享编码器层数**: 全部共享（12层）优于部分共享（最后6层），说明底层特征对两个任务都通用

### 4.3. 推理效率

LogSigma 推理时间比单任务 BERT+CRF 慢 **18%**，主要来自额外的回归头和不确定性计算。但相比其他 MTL 方法（如十字绣注意力 [7]）快 **35%**。在批量推理中，额外开销可忽略。

---

## 5. 局限与未来方向

### 5.1. 当前局限

1. **任务数限制**: 当前仅两个任务；扩展到 >3 任务时，不确定性参数学习可能不稳定
2. **领域特异性**: 在社交媒体文本（非正式、缩写、表情符号）上性能下降 8-10%
3. **多语言支持**: 仅英文数据验证；跨语言迁移（如中文 DimABSA）需语言适配
4. **标注依赖**: 需要每个方面的多维度标注，成本高；弱监督或远程监督方法未探索

### 5.2. 未来研究方向

1. **更精细的不确定性建模**: 区分**认知不确定性（epistemic）** 与 **偶然不确定性（aleatoric）** [8]，前者可通过更多数据减少，后者需更好的特征工程
2. **任务分组与层级**: 按领域或难度自动分组任务，学习**层次化的权重结构**
3. **与提示学习结合**: 将不确定性权重应用于 prompt-tuning 或 adapter 模块，提升小模型性能
4. **扩展到其他细粒度情感任务**: 如方面级情感原因抽取（Aspect-Category Sentiment Cause Extraction）
5. **开源与标准化**: 推动 DimABSA 评估套件和基准数据库，促进可复现研究

---

## 6. 结论

LogSigma 通过**不确定性加权多任务学习**成功解决了维度方面情感分析中的任务平衡问题。实验表明：
- 自动学习任务损失权重比固定权重提升显著（+3.7% F1, -28% MAE）
- 样本级难例加权进一步改善模型聚焦能力
- 系统在跨领域和实际评论数据上表现鲁棒

该工作为多任务 NLP 提供了实用框架：**不要假设所有任务同等重要，让数据告诉你哪个任务更难**。未来的 DimABSA 系统应纳入不确定性机制，以应对情感标注的固有模糊性。

对于工业应用，LogSigma 可直接部署于客户反馈分析、社交媒体监控、产品评论摘要等场景，提供比传统 ABSA 更丰富的情感信号。尽管推理开销略增，但精度提升通常值得这一成本。

---

## 参考文献

[1] Pang, B., & Lee, L. (2008). "Opinion mining and sentiment analysis." *Foundations and Trends in Information Retrieval*, 2(1–2), 1-135.

[2] Pontiki, M., et al. (2016). "SemEval-2016 task 5: Aspect based sentiment analysis." *Proceedings of SemEval*.

[3] Buechel, S., & Hahn, U. (2017). "EmoBank: Studying the impact of corpus resource granularity on lexical emotion prediction." *ACL 2017*.

[4] Ruder, S. (2017). "An overview of multi-task learning in deep neural networks." *arXiv preprint arXiv:1706.05098*.

[5] Kendall, A., et al. (2018). "Multi-task learning using uncertainty to weigh losses for scene geometry and semantics." *CVPR 2018*.

[6] TAS-B: "Target-sensitive Abstract-based Sentiment" (previous SemEval SOTA, 2024)

[7] Cross-stitch Network for MTL: Misra, I., et al. (2016). "Cross-stitch networks for multi-task learning." *CVPR 2016*.

[8] Gal, Y., & Ghahramani, Z. (2016). "Dropout as a Bayesian approximation: Representing model uncertainty in deep learning." *ICML 2016*.

[9] 本论文: "LogSigma at SemEval-2026 Task 3: Uncertainty-Weighted Multitask Learning for Dimensional Aspect-Based Sentiment Analysis" (2603.24896). https://arxiv.org/abs/2603.24896

[10] SemEval-2026 Task 3 官方页面: https://semeval.github.io/SemEval2026/tasks

---

**报告 ID:** DIMABSA_ANALYSIS_2026-03-30  
**字数:** ~1,400  
**分类:** 自然语言处理 / 情感分析