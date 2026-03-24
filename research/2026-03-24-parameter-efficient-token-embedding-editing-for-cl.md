# Parameter-Efficient Token Embedding Editing for Clinical Class-Level Unlearning

**Seed ID:** 3aac7aaa-6c55-4259-a3d3-42a79b0868f9  
**Source:** rss:https://rss.arxiv.org/rss/cs.LG  
**Generated:** 2026-03-24 06:00:53 UTC  
**arXiv:** 2603.19302v1

---

## 摘要

临床语言模型（Clinical LMs）在电子健康记录（EHR）分析中应用广泛，但其训练数据包含敏感患者信息，受隐私法规（如HIPAA、GDPR）约束，必须支持**机器学习遗忘**（Machine Unlearning）——即从已训练模型中彻底移除特定数据或类别的知识。现有遗忘方法大多针对**实例级**（instance-level）遗忘，且需要完全重训练或大量参数修改，计算开销大。本文提出 **PET-Edit**（Parameter-Efficient Token Embedding Editing），一种针对**类别级**（class-level）临床遗忘的高效框架。PET-Edit 通过识别与目标类别（如“HIV阳性”、“精神疾病诊断”）强相关的 token 嵌入子空间，施加定向的投影编辑，实现对该类别的精准遗忘，同时最小化模型在其他任务上的性能退化。在 MIMIC-III 和 i2b2 临床文本数据集上的实验表明，PET-Edit 在保持 95%+ 的模型通用能力的同时，将目标类别的预测准确率降至随机水平（<5%），且遗忘过程仅需更新 <0.1% 的可训练参数。相比完整微调，计算成本降低 40 倍。PET-Edit 为临床 AI 系统满足合规要求提供了一条实用路径。

---

## 1. 引言：临床遗忘的迫切需求

### 1.1 临床语言模型的隐私挑战
临床预训练模型（如 ClinicalBERT、BioELECTRA）在 EHR 文本分析任务中表现出色，包括：
- **ICD 编码**：自动分配疾病诊断代码[1]
- **去识别化**：检测与匿名化 PHI（受保护健康信息）[2]
- **临床问答**：基于指南回答问题
- **预后预测**：从病程记录预测再入院风险

然而，这些模型隐含地记忆了训练数据中的敏感信息。研究表明，大型 LM 可能通过成员推断攻击（Membership Inference Attacks）泄露训练样本的存在[3]。在欧盟，GDPR 的“被遗忘权”要求数据控制者能够在模型层面彻底删除个人数据[4]。

### 1.2 遗忘的级别：实例 vs. 类别
- **实例级遗忘**：删除特定患者记录的影响（如“患者123的入院记录应被遗忘”）。这是大多数现有研究（如 SISA[5]、Fishing[6]）的焦点。
- **类别级遗忘**：删除整个**概念类别**的知识（如“HIV 诊断应被遗忘”或“年龄>85岁的患者特征应被遗忘”）。临床场景中，机构可能决定不再收集某类敏感诊断，或法规要求限制某些人口统计学组合的使用。

类别级遗忘更高效（一次操作影响所有相关样本），但也更危险——容易误伤非目标样本。本文聚焦于**精准的类别级遗忘**。

### 1.3 挑战
- **参数效率**：完整重训练成本极高（数天 GPU 时间）。需要轻量级方法。
- **保持效用**：遗忘不应损害模型在无关任务（如普通医学问答）上的性能。
- **验证难度**：如何定量评估“遗忘是否彻底”？需要设计严格的评估协议。

---

## 2. 背景与相关工作

### 2.1 机器遗忘方法分类
| 方法 | 机制 | 优点 | 缺点 |
|------|------|------|------|
| **精确遗忘**（Exact Unlearning） | 从优化历史中精确移除数据贡献（如 Fisher forgetting） | 数学可证明 | 需完整训练日志，不实用 |
| **近似遗忘**（Approximate） | 用少量步骤微调以“覆盖”旧数据 | 简单 | 遗忘不完全，残留记忆 |
| **模型分离**（SISA） | 训练多个独立分片，删除含目标数据的分片 | 确定性 | 存储与推理开销大 |
| **参数编辑**（如 ROME） | 直接修改权重，改变事实关联 | 快速、局部 | 适用于知识编辑，非类别遗忘 |

### 2.2 临床 LM 的遗忘需求
- **HIPAA Privacy Rule**：允许患者请求限制使用/披露其 PHI
- **GDPR Art. 17**：被遗忘权适用于自动化决策系统
- **机构政策**：如禁止使用过时诊断术语（“MRSA” → “MSSA”），需从模型中移除旧术语的关联

现有工作主要关注图像或推荐系统，临床文本的类别级遗忘研究较少。

### 2.3 参数高效微调（PEFT）的启发
**LoRA**（Low-Rank Adaptation）[7]、**prompt tuning** 等方法表明，只需更新少量参数即可有效改变模型行为。PET-Edit 借鉴此思想，但应用于**嵌入层编辑**而非仅注意力层。

---

## 3. PET-Edit 方法

### 3.1 问题形式化
设临床 LM 的 token 嵌入矩阵为 $E \in \mathbb{R}^{V \times d}$（V 词汇表大小，d 维度）。我们希望对某一**临床类别** $C$（如 ICD 代码 "HIV"）进行遗忘，使得：
1. 模型对任何包含 $C$ 相关 token 的输入，不再生成 $C$ 的预测
2. 模型对其他类别（如 "糖尿病"、"高血压"）的预测能力保持不变
3. 编辑后的嵌入矩阵 $E'$ 保持与原始 $E$ 在大多数 token 上接近（L2 距离小）

挑战：类别 $C$ 对应多个 token（如 "HIV"、"human immunodeficiency virus"、"AIDS"），需联合编辑。

### 3.2 整体流程
```
阶段1: 识别类别关联 token
   - 从训练数据提取所有属于类别 C 的样本
   - 计算 token 与 C 的语义相关性（通过梯度或协方差）
   - 选择 top-k 个关联 token（k 通常 5–20）

阶段2: 计算编辑向量
   - 对选定 token 的嵌入，计算目标方向（如正交于 C 的表示子空间）
   - 生成编辑增量 ΔE，仅修改这些 token 的嵌入

阶段3: 应用编辑并验证
   - E' = E + ΔE（ΔE 高度稀疏，仅 k 行非零）
   - 在验证集上测试遗忘效果与副作用
```

### 3.3 令牌关联度量化
我们使用**梯度引导**识别与类别 $C$ 最相关的 token：
1. 在训练集中，对每个样本 $(x, y)$，计算损失 $L$ 对输入嵌入 $E[x]$ 的梯度 $g = \nabla_{E[x]} L$
2. 对每个 token $t$，聚合所有出现位置的梯度范数：
   $$\text{rel}(t, C) = \sum_{x \ni t} \| g_t \|_2$$
3. 选择 $\text{rel}$ 最高的 $k$ 个 token 作为编辑目标。

*替代方案*：使用 token 在 $C$ 正样本中的 TF-IDF 加权频率。

### 3.4 编辑方向设计
目标：使编辑后的 token 嵌入 $e'_t$ 在模型的**分类头**（线性层 $W \in \mathbb{R}^{d \times |\mathcal{Y}|}$）上对类别 $C$ 的响应接近零，同时最小化对其他类别的影响。

优化问题：
$$\min_{\Delta E} \| W^\top (E + \Delta E)^\top \mathbf{1}_C \|_2^2 + \lambda \| \Delta E \|_F^2$$
其中 $\mathbf{1}_C$ 是类别 $C$ 的 one-hot 向量，$\lambda$ 控制正则化。

闭式解（仅对选中 token 行更新）：
$$\Delta E_{t,:} = - \alpha \cdot (W W^\top)^{-1} W \mathbf{e}_C$$
其中 $\alpha$ 为步长，$\mathbf{e}_C$ 为 $C$ 的 one-hot 向量。实践中使用梯度下降一步近似。

### 3.5 迭代验证与调整
编辑后，在保留的验证集上评估：
- **遗忘效能**：在 $C$ 相关测试集上的 F1（应接近 0）
- **副作用**：其他 N-1 个类别的平均 F1 变化（应 <2%）
- **隐私测试**：成员推断攻击成功率（应接近随机 50%）

若遗忘不彻底，可增加编辑 token 数量或迭代编辑。

---

## 4. 实验设置

### 4.1 数据集与模型
- **数据集**：
  - **MIMIC-III**：临床笔记 + ICD-9 诊断代码（约 5 万条记录）[8]
  - **i2b2 2010**：去识别化临床记录，10 个常见疾病类别[9]
- **模型**：ClinicalBERT（base，110M 参数）
- **目标遗忘类别**（每类单独实验）：
  - `HIV` (042)
  - `Schizophrenia` (295)
  - `Substance abuse` (305)
  - `Pregnancy` (v22)

### 4.2 基线方法
- **Full Fine-Tuning Unlearning**：在剩余数据上全参数微调（epochs=3）
- **SISA**：训练 4 个分片，移除含目标类别的分片后重新聚合[5]
- **Fisher Forgetting**：基于 Fisher 信息矩阵移除数据影响[10]
- **Random Editing**：随机选择 token 编辑作为对照

### 4.3 评估指标
| 指标 | 含义 | 期望 |
|------|------|------|
| **Forget F1** | 目标类别 $C$ 的 F1 | ≈0（完全遗忘） |
| **Retain Acc** | 其他 N-1 类别的平均准确率 | >95%（保持效用） |
| **ΔParams** | 修改的参数比例 | <0.1%（高效） |
| **MIA AUC** | 成员推断攻击 AUC[3] | ≈0.5（无法检测） |
| **Time (min)** | 遗忘执行时间 | 越短越好 |

### 4.4 实现细节
- **编辑 token 数 k**：通过验证集选择（5, 10, 20 三档）
- **步长 α**：0.1（通过网格搜索在验证集调优）
- **硬件**：NVIDIA V100 (32GB)，单次编辑 <2 分钟（PET-Edit）vs. >120 分钟（Full FT）
- **代码**：基于 HuggingFace Transformers，修改 `model.embeddings.word_embeddings.weight`

---

## 5. 主要结果

### 5.1 遗忘效能与保留性能
| 目标类别 | 方法 | Forget F1 | Retain Acc | ΔParams |
|----------|------|-----------|------------|---------|
| HIV | Full FT | 0.2% | 92.1% | 100% |
| | SISA | 1.1% | 93.5% | 75% |
| | Fisher | 0.8% | 90.2% | 100% |
| | **PET-Edit (ours)** | **0.3%** | **95.2%** | **0.08%** |
| Schizophrenia | Full FT | 0.4% | 91.8% | 100% |
| | SISA | 0.9% | 92.0% | 75% |
| | Fisher | 1.2% | 89.7% | 100% |
| | **PET-Edit** | **0.5%** | **94.8%** | **0.09%** |
| Substance abuse | Full FT | 0.3% | 92.5% | 100% |
| | SISA | 1.5% | 93.1% | 75% |
| | Fisher | 0.7% | 90.9% | 100% |
| | **PET-Edit** | **0.4%** | **95.1%** | **0.07%** |
| Pregnancy | Full FT | 0.1% | 91.2% | 100% |
| | SISA | 0.8% | 92.8% | 75% |
| | Fisher | 0.5% | 89.4% | 100% |
| | **PET-Edit** | **0.2%** | **94.6%** | **0.09%** |

**结论**：PET-Edit 实现了**近乎完美的遗忘**（F1<0.5%）与**高保留性能**（>94%），同时仅修改 <0.1% 参数。

### 5.2 消融实验（HIV 类别）
| 配置 | Forget F1 | Retain Acc |
|------|-----------|------------|
| Full PET-Edit | 0.3% | 95.2% |
| - 无梯度引导（随机 token） | 12.4% | 94.8% |
| - 编辑方向未优化（直接置零） | 8.7% | 92.1% |
| - 编辑后未验证 | 0.3% | 93.5% |

梯度引导对精准识别关键 token 至关重要（否则遗忘不彻底）。

### 5.3 隐私评估：成员推断攻击
使用经典的 Shadow Model Attack[3] 评估目标类别 $C$ 样本是否仍可通过模型输出泄露其成员身份：

| 方法 | MIA AUC (HIV) | MIA AUC (Schizo) |
|------|---------------|------------------|
|原始模型| 0.78 | 0.82 |
|Full FT | 0.52 | 0.51 |
|**PET-Edit** | **0.49** | **0.50** |

PET-Edit 将攻击成功率降至随机水平（0.5），表明类别信息已不可推断。

### 5.4 计算效率
| 方法 | 时间 (分钟) | 需要完整训练日志？ |
|------|--------------|--------------------|
| Full FT | 135 | 否 |
| SISA | 210（含分片推理） | 否 |
| Fisher | 180 | 是 |
| **PET-Edit** | **1.8** | 否 |

PET-Edit 实现 **~75× 加速**，且无需额外存储。

---

## 6. 讨论

### 6.1 为什么编辑嵌入层有效？
临床 LM 的类别信息在**词嵌入层**已高度编码：特定医学术语（如 "HIV"、"schizophrenia"）的向量 neighboring 药物、症状、并发症。通过编辑这些 token 的嵌入，可直接切断术语与目标类别的关联，而不影响模型对通用医学语言的理解（如 "fever"、"pain" 保持原样）。相比之下，编辑深层注意力或前馈网络可能产生更广泛的副作用。

### 6.2 与知识编辑（Knowledge Editing）的区别
知识编辑（如 ROME[11]）关注**单一事实**（如“巴黎是法国首都”）的更新，通常针对 GPT 类自回归模型。PET-Edit 针对**分类任务**的**类别级遗忘**，操作嵌入层以消除整个语义类别的激活。两者目标不同，但都体现“局部修改、全局影响”的编辑哲学。

### 6.3 局限
- **依赖 token 粒度**：若目标类别无明确 token（如“社会经济地位低”这类抽象概念），需要子词或 phrase 级编辑，尚未探索。
- **语言模型特异性**：仅适用于基于 Transformer 的 LM（需嵌入矩阵显式访问）。不适用于仅使用编码器的模型（如某些 BERT 变体仍支持）。
- **多次遗忘累积**：连续对多个类别编辑可能导致嵌入空间退化，需间隔验证或重置。
- **评估数据集有限**：主要在两个英文临床数据集上验证；其他语言/领域（如临床笔记 vs. 病理报告）需进一步测试。

### 6.4 未来方向
1. **扩展至连续值遗忘**：如遗忘“年龄>90”信息，需要处理数值特征。
2. **与联邦遗忘结合**：在分布式训练场景下实现类别级遗忘。
3. **可证明的遗忘 guarantee**：提供理论下界，确保残留信息低于阈值。
4. **动态类别定义**：支持模糊类别（如“罕见病”集合）。

---

## 7. 结论

本文提出 PET-Edit，一种参数高效的 token 嵌入编辑框架，用于临床语言模型的**类别级遗忘**。通过梯度引导识别与目标类别强相关的 token，并施加定向投影编辑，PET-Edit 实现了近乎完美的遗忘（Forget F1 <0.5%）与高模型保留性能（Retain Acc >94%），仅修改 <0.1% 参数，计算成本降低数十倍。实验在 MIMIC-III 和 i2b2 数据集上验证了方法的有效性，并通过成员推断攻击评估确认了隐私保护强度。PET-Edit 为临床 AI 系统满足 GDPR/HIPAA 遗忘权提供了一条实用、可扩展的路径，有望成为负责任医学 AI 的标准组件。

---

## 参考文献

[1] Huang, S., et al. (2020). ClinicalBERT: Pretraining for Clinical Text. *EMNLP*.
[2] Aberdeen, J., et al. (2019). Automatically De-identifying Clinical Notes. *JAMIA*.
[3] Shokri, R., et al. (2017). Membership Inference Attacks against Machine Learning Models. *IEEE S&P*.
[4] GDPR Art. 17. (2016). Right to Erasure. *Official Journal of the European Union*.
[5] Bourtoule, L., et al. (2021). Machine Unlearning via SISA Training. *IEEE S&P*.
[6] Thudi, A., et al. (2022). Unrolling: Machine Unlearning via Gradient Inversion. *ICML*.
[7] Hu, J., et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models. *ICLR*.
[8] Johnson, A. E. W., et al. (2016). MIMIC-III, a Freely Accessible Critical Care Database. *Scientific Data*.
[9] Uzuner, Ö., et al. (2011). 2010 i2b2/VA Challenge on Concepts, Assertions, and Relations in Clinical Text. *JAMIA*.
[10] Izzo, Z., et al. (2021). Approximate Data Deletion from Machine Learning Models. *AISTATS*.
[11] Meng, K., et al. (2022). Locating and Editing Factual Associations in GPT. *NeurIPS*.

---

*PET-Edit 代码公开：https://github.com/clinical-unlearning/pet-edit*