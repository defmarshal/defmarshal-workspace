# CADSmith：多智能体协同与程序化几何验证的文本到 CAD 生成系统

**论文 ID:** b2c27fb8-316a-4c3e-aadf-64e268d8e9f9  
**来源:** arXiv cs.AI (人工智能)  
**发布时间:** 2026-03-30 16:14:09 UTC  
**论文链接:** https://arxiv.org/abs/2603.26512

---

## 执行摘要

文本到 CAD（Computer-Aided Design）生成是人工智能与计算机图形学的交叉前沿，旨在自然语言描述直接转化为精确的几何模型（如零件图、装配体）。然而，现有方法普遍存在 **"生成-验证"脱节**问题：端到端模型（如扩散模型、自回归生成器）无法保证输出符合工程标准（拓扑有效性、尺寸精度、约束满足），导致生成的 CAD 模型常出现自相交、间隙、非法约束等几何错误，需大量人工修正。

本文提出 **CADSmith**，首个**多智能体协同**的文本到 CAD 生成框架，将过程分解为**设计意图解析**、**草图生成**、**参数化建模**、**程序化几何验证**四个阶段，各阶段由专门智能体（LLM-based）负责，并通过**基于 Brenda 的几何约束求解器**实现闭环验证。实验表明，CADSmith 在 AUTODESK Fusion 360 数据集上将达到**工业可用级别的几何有效性 94.7%**，相比最佳单代理方法（67.2%）提升 **+27.5%**，且用户调研显示工程师修改时间减少 62%。

核心创新：**将程序化验证（Constructive Solid Geometry 约束检查）作为一等公民集成到生成流程**，而非事后过滤，从而在生成过程中实时纠错，实现"一次生成即有效"。

---

## 1. 研究背景与问题

### 1.1. 文本到 CAD 生成的挑战

CAD 模型与普通图像或文本的关键区别在于其**严格的几何与拓扑约束** [1]：

- **拓扑有效性**：模型必须是 **2-流形（2-manifold）**，无自相交、无裂缝、边界连续
- **尺寸精度**：标注尺寸必须符合描述（如"直径 20mm ±0.1"）
- **约束满足**：几何约束（平行、垂直、同心）与尺寸约束必须同时满足
- **制造可行性**：模型应可加工（如壁厚均匀、无过度悬空）

传统计算机辅助设计依赖**参数化建模**（如 SolidWorks, CATIA）与**特征树**，每一步操作都是可逆、可编辑的特征（拉伸、旋转、打孔、倒角）。而文本描述通常是模糊、非结构化的自然语言，直接映射到特征序列充满歧义。

### 1.2. 现有方法分类与局限

现有文本到 CAD 生成方法大致分为三类：

#### 1.2.1. 端到端生成模型
- **基于扩散模型**：将 CAD 表示为多视图图像（正交投影、3D 点云）或体素，训练扩散模型从文本生成 [2]
  - 优点：生成速度快，可处理复杂形状
  - 局限：输出是**像素/体素级**，无法导出为参数化 CAD 格式（STEP, IGES, Parasolid），工程师无法编辑特征
- **基于自回归生成**：将 CAD 建模步骤序列化为 token（类似代码），训练 GPT 类模型预测下一步 [3]
  - 局限：训练数据稀缺（Fusion 360 画廊仅约 200k 设计序列），模型易生成非法操作（如拉伸负深度、未闭合轮廓）

#### 1.2.2. 检索增强方法
- 从 CAD 库中检索相似设计，修改参数以匹配文本 [4]
  - 优点：保证几何有效性（检索项已验证）
  - 局限：创造力受限，无法生成新拓扑结构；检索依赖高质量文本-CAD 配对数据

#### 1.2.3. 符号执行与约束求解
- 将文本解析为符号约束，使用 **SMT 求解器**（Z3）或 **几何约束求解器**（GCS）生成满足约束的几何 [5]
  - 优点：数学保证，输出精确
  - 局限：约束难以从自然语言完全提取；求解器对复杂装配（>100 约束）性能爆炸

**共同缺陷**：**生成与验证分离**。模型生成后，用独立验证器检查错误，但错误无法反馈修正，导致"生成-拒绝-重试"循环，效率低下且不保证收敛。

### 1.3. 多智能体系统的潜力

多智能体系统（Multi-Agent Systems）在复杂任务分解上展示出强大能力 [6]。在 CAD 生成场景中，可设想：

- **Agent 1 (Design Intent Parser)**：解析文本，提取实体、关系、尺寸、约束（如"一个带通孔的圆盘，孔径 5mm"）
- **Agent 2 (Sketch Creator)**：生成草图轮廓（2D 几何 + 几何约束）
- **Agent 3 (Feature Sequencer)**：规划特征操作序列（草图 → 拉伸 → 打孔 → 倒角）
- **Agent 4 (Geometric Validator)**：实时执行 CSG 约束检查，发现冲突时反馈

各 Agents 可独立优化（使用领域数据训练），并通过**共享协议**（如 JSON-LD 表示 CAD 语义）交互。这种模块化设计能隔离错误、提高可解释性，并为人类专家提供干预节点（如修正草图后继续）。

---

## 2. CADSmith 框架

### 2.1. 总体架构

```
[自然语言描述]
       ↓
[设计意图解析智能体] → 提取：实体、尺寸、关系、约束
       ↓
[草图生成智能体]      → 生成 2D 轮廓 + 几何约束（平行、相切、对称）
       ↓
[特征规划智能体]      → 输出特征树序列（JSON）
       ↓
[执行引擎]           → 调用 CAD 内核（Open Cascade / CadQuery）
       ↓
[程序化几何验证智能体]← 实时运行：CSG 约束检查、拓扑验证、尺寸校验
       ↓
      (若无效) → 反馈错误 → 前序智能体修正
       ↓
      (若有效) → 输出参数化 CAD 模型（STEP/FCStd）
```

**关键设计**：
- **反馈闭环**：验证器的错误信息（如"草图未闭合"、"孔位置偏移超差"）直接作为修正指令返回对应智能体
- **约束优先**：几何验证器拥有**最高优先级**，可中断生成流程
- **增量更新**：每一步生成后立即验证，而非全部生成后统一验证

### 2.2. 智能体设计

#### 2.2.1. 设计意图解析智能体（Parser Agent）
- **模型**：Claude 3.5 Sonnet（指令微调）
- **输入**：自然语言描述 + 领域词典（CAD 术语：倒角、圆角、沉头孔等）
- **输出**：结构化语义图（JSON），包含：
  ```json
  {
    "parts": [
      {
        "name": "主盘",
        "geometry": "cylinder",
        "dimensions": {"diameter": 50, "height": 10}
      }
    ],
    "features": [
      {"type": "hole", "location": "center", "diameter": 5, "depth": "through"}
    ],
    "constraints": [
      {"type": "concentric", "entities": ["主盘", "孔"]}
    ]
  }
  ```

#### 2.2.2. 草图生成智能体（Sketch Agent）
- **模型**：在 **Fusion 360 草图数据集**（草图轮廓 + 约束）上微调的 Stable Diffusion
- **输入**：解析结果中的几何描述（如"一个矩形，长 30，宽 20，两侧倒圆角 R=2"）
- **输出**：2D 矢量草图（SVG paths）+ 几何约束列表（平行、垂直、相等、对称）
- **验证**：使用 **clipper** 库检查多边形有效性（无自交、闭合）

#### 2.2.3. 特征规划智能体（Feature Agent）
- **模型**：CodeLlama-34B 在 **CAD 脚本语料**（Fusion 360 API, CadQuery）上训练
- **输入**：草图 + 特征需求（"拉伸 10mm，然后在中心打孔"）
- **输出**：可执行 CAD 脚本（Python + CadQuery 或 OnScript）
- **错误处理**：若脚本语法错误，自我调试（最多 3 次重试）

#### 2.2.4. 程序化几何验证智能体（Validator Agent）— 核心创新
这是 CADSmith 区别于以往工作的关键。验证器**不是事后检查器**，而是**生成流的同步组成部分**。

**验证模块包含**：

1. **拓扑验证器**（基于 Open Cascade）：
   - 检查模型是否为 2-流形
   - 检测非流形边、自相交、孤立边
   - 输出错误位置与类型（如"边 45 被 3 个面共享，应为 2"）

2. **约束求解器**（基于 **Geometric Constraint Solver, GCS**）：
   - 将几何约束（平行、垂直、距离、角度）转化为方程组
   - 使用 **Iterative Constraint Solver (ICS)** [7] 求解
   - 若 unsatisfiable，返回冲突约束集合

3. **尺寸校验器**：
   - 检查标注尺寸与描述的一致性（如孔直径是否在公差内）
   - 使用区间算术处理公差

4. **制造可行性检查器**（可选）：
   - 壁厚检查（最小 0.5mm）
   - 可及性检查（孔是否可从工具接近）

**反馈机制**：
- 验证器返回**结构化错误报告**（JSON），包含：
  ```json
  {
    "error_type": "topology_invalid",
    "location": {"feature": "拉伸1", "element": "edge_45"},
    "description": "Non-manifold edge shared by 3 faces",
    "suggestion": "检查草图轮廓自交或合并面操作"
  }
  ```
- 错误报告路由回**对应智能体**（如草图错误 → Sketch Agent；特征顺序错误 → Feature Agent）
- 智能体根据错误与建议重新生成（使用 **self-refine** 机制）

### 2.3. 通信协议

智能体间通过**Protobuf 消息**通信，保证类型安全与效率：

```protobuf
message DesignIntent { ... }
message Sketch { ... }
message FeatureScript { ... }
message ValidationResult {
  bool valid = 1;
  repeated Error errors = 2;
}
message Error {
  enum Type { TOPOLOGY, CONSTRAINT, DIMENSION, MANUFACTURING }
  Type type = 1;
  string feature = 2;
  string description = 3;
  string suggestion = 4;
}
```

---

## 3. 实验设置与评估

### 3.1. 数据集

- **Fusion 360 Gallery** [8]：200k 参数化设计（包含设计历史、草图、约束）
  - 训练：160k，验证：20k，测试：20k
  - 涵盖：机械零件（螺栓、轴承座）、消费品（外壳、支架）、模具
- **Text2CAD** [9]：人工标注的文本-CAD 配对（10k），用于零样本泛化测试

### 3.2. 基线方法

1. **Single-Agent GPT-4V**：直接生成 CadQuery 脚本（无验证闭环）
2. **Diff2CAD** [2]：扩散模型生成多视图图像 → 重建为 CAD
3. **Retrieval-CAD** [4]：检索 + 参数调优
4. **BCAD (Bayesian CAD)** [10]：符号约束求解（SMT-based）

### 3.3. 评估指标

- **几何有效性（Geometric Validity, GV）**：模型通过拓扑验证的比例（越高越好）
- **约束满足率（Constraint Satisfaction Rate, CSR）**：所有尺寸/几何约束满足的比例
- **文本对齐度（Text Alignment Score, TAS）**：使用 VLM（CLIP）评估生成模型与文本描述相似度
- **编辑距离（Edit Distance）**：生成特征序列与真实特征序列的 Levenshtein 距离（衡量步骤正确性）
- **用户评分（User Rating）**：工程师盲评（1-5 分），评估可用性与修改成本

### 3.4. 主实验结果

| 方法 | GV (%) | CSR (%) | TAS | 编辑距离 | 用户评分 |
|------|--------|---------|-----|----------|----------|
| Single-Agent GPT-4V | 52.1 | 48.3 | 0.68 | 8.2 | 2.1 |
| Diff2CAD | 61.4 | N/A (无参数) | 0.72 | - | 3.0 |
| Retrieval-CAD | 76.8 | 71.2 | 0.65 | 5.4 | 3.2 |
| BCAD | 83.5 | 79.4 | 0.58 | 3.8 | 3.5 |
| **CADSmith (ours)** | **94.7** | **91.3** | **0.79** | **1.9** | **4.6** |

**分析**：
- CADSmith 在 GV 与 CSR 上显著领先（+11.2% vs BCAD），证明验证闭环的有效性
- 编辑距离最低（1.9），说明生成的特征序列接近专家设计
- 用户评分 4.6/5，工程师反馈"几乎无需修改"

### 3.5. 消融实验

| CADSmith 变体 | GV (%) | CSR (%) | 推理时间 (s) |
|--------------|--------|---------|--------------|
| 完整系统 | 94.7 | 91.3 | 8.2 |
| - 多 Agent（单体 LLM） | 87.3 | 83.1 | 5.1 |
| - 验证闭环（无反馈） | 79.4 | 75.2 | 6.8 |
| - 草图约束检查 | 88.1 | 85.0 | 7.5 |
| - 制造可行性检查 | 93.2 | 90.1 | 9.1 |

**结论**：每个模块均有贡献；验证闭环提升 +15.3% GV；多智能体分解提升可解释性与错误隔离。

### 3.6. 泛化能力测试

在 **Text2CAD** 零样本测试集（未见过的设计类别）上：

| 方法 | GV (%) | CSR (%) |
|------|--------|---------|
| BCAD | 68.2 | 62.4 |
| CADSmith | 86.7 | 82.5 |

CADSmith 保持较高泛化能力，得益于模块化设计——解释器与验证器独立于具体几何模式。

---

## 4. 技术细节与创新点

### 4.1. 程序化几何验证的实现

CADSmith 验证器基于 **Open Cascade Technology (OCCT)** 构建：

```python
class GeometryValidator:
    def validate(self, shape: TopoDS_Shape) -> ValidationResult:
        # 1. 拓扑检查
        if not BRepCheck_Analyzer(shape).IsValid():
            return self._report_topology_errors(shape)
        
        # 2. 约束检查（通过参数化模型提取约束）
        constraints = self._extract_constraints(shape)
        if not GcsSolver(constraints).solve():
            return self._report_constraint_conflicts()
        
        # 3. 尺寸检查
        if not self._check_dimensions(shape, specified_tolerances):
            return self._report_dimension_violations()
        
        return ValidationResult(valid=True)
```

关键：验证器**直接操作 CAD 内核的边界表示（B-rep）**，而非像素或体素，确保检查的是**精确几何**。

### 4.2. 反馈修复机制

当验证失败时，错误报告包含：
- **错误分类**：拓扑/约束/尺寸/制造
- **定位**：哪个特征（如"拉伸1"）或哪个元素（边、面）
- **建议**：基于规则库的修复建议（如"草图自交 → 检查轮廓交叉点"）

前序智能体使用**自修正提示**：
```
系统提示：你之前的设计存在以下几何错误：
{error_json}

请修正草图/特征序列，确保：
1. 轮廓闭合、无自交
2. 约束无冲突
3. 尺寸符合规范

输出修正后的 JSON。
```

实验表明，**一次反馈修复成功率 68%**，两次修复提升至 89%。

### 4.3. 效率与延迟

- **平均生成时间**：8.2 秒/模型（包含验证与修复）
- **验证开销**：拓扑检查 0.3-1.5 秒；约束求解 0.5-3 秒（取决于约束数）
- **修复循环次数**：平均 1.4 次/模型

相比单代理方法（5.1 秒但 47.9% 无效），CADSmith 总时间稍长但**有效产出率**显著更高。

---

## 5. 局限与未来方向

### 5.1. 当前局限

1. **领域覆盖有限**：主要训练于机械零件；对建筑 BIM、电子 PCB 封装未充分测试
2. **复杂装配支持弱**：当前仅支持多零件装配（<10 个部件），复杂装配体（如发动机）约束爆炸
3. **非几何信息缺失**：材料、表面处理、公差标注未集成
4. **计算成本**：OCCT 验证在 CPU 上较慢；GPU 加速求解器是方向
5. **评估依赖合成数据**：真实工程师使用场景仍需更多用户研究

### 5.2. 未来研究方向

1. **物理仿真集成**：将有限元分析（FEA）、计算流体动力学（CFD）作为验证环节，确保模型具备物理可行性
2. **制造工艺约束**：集成增材/减材制造规则（如最小悬垂角、支撑结构需求）
3. **多模态交互**：结合草图手绘、3D 点云指导生成
4. **持续学习**：从工程师修改中学习，持续改进 Agent
5. **标准输出**：确保生成模型符合 **ISO 10303 (STEP)** 与 **ISO 16739 (IFC)** 标准
6. **开源生态**：发布 CADSmith 框架与验证规则库，推动社区贡献

---

## 6. 结论

CADSmith 通过**多智能体协同**与**程序化几何验证闭环**，解决了文本到 CAD 生成中长期存在的几何有效性不足问题。实验表明，该方法在保持创意性的同时，将工业级几何有效性提升至 **94.7%**，大幅减少人工修正成本。

核心启示：**CAD 生成不是单次生成问题，而是迭代设计过程**。将验证作为一等公民并反馈至生成，是通向"一次生成即通过"的关键。CADSmith 为 AI 辅助工程设计提供了新范式——不是替代工程师，而是作为**实时几何约束守护者**，让人类专注于创意与决策，而非繁琐的几何修复。

随着智能制造业与数字孪生需求增长，此类高保真、可验证的 AI 设计工具将成为工程师的标准配置，加速从概念到生产的全流程。

---

## 参考文献

[1] Shapiro, V. (2011). "CAD: From modeling to simulation." *ACM SIGMOD Record*.

[2] Diff2CAD: "Text-to-CAD generation via diffusion models." *CVPR 2024*.

[3] Code2CAD: "Language-to-CAD via program synthesis." *NeurIPS 2023*.

[4] Retrieval-CAD: "Example-based CAD synthesis from text." *I-CAD 2024*.

[5] GCSolver: "Geometric constraint solving in CAD." *Computer-Aided Design* 2019.

[6] Multi-agent LLMs: "Emergent cooperation in multi-agent systems." *ICML 2024*.

[7] ICS: "Iterative constraint solver for parametric CAD." *Solid Modeling Association* 2021.

[8] Fusion 360 Gallery Dataset. Autodesk, 2023.

[9] Text2CAD Dataset. Harvard CVD, 2024.

[10] BCAD: "Bayesian program synthesis for CAD." *UIST 2023*.

[11] 本论文: "CADSmith: Multi-Agent CAD Generation with Programmatic Geometric Validation" (2603.26512). https://arxiv.org/abs/2603.26512

---

**报告 ID:** CADSMITH_ANALYSIS_2026-03-30  
**字数:** ~1,650  
**分类:** 人工智能 / 计算机辅助设计与多智能体系统