# Skilled AI Agents for Embedded and IoT Systems Development

**Seed ID:** 2236affa-cc2f-4f54-98f9-6ef60eee287e  
**Source:** rss:https://rss.arxiv.org/rss/cs.SE  
**Generated:** 2026-03-24 07:01:25 UTC  
**arXiv:** 2603.19583v1

---

## 摘要

大语言模型（LLMs）与智能体系统已展现出自动化软件开发的潜力，但在**硬件在环（Hardware-in-the-Loop, HIL）**嵌入式与物联网（IoT）系统开发中应用仍面临独特挑战。这些挑战包括：资源受限设备的编译与部署、时序约束验证、硬件驱动适配、以及物理世界交互的不可预测性。本文提出 **Skilled AI Agents (SAA)**，一种多智能体协作框架，专门针对嵌入式/IoT 全生命周期开发。SAA 将开发过程分解为需求分析、架构设计、编码、硬件集成、HIL 测试与优化六个专门化智能体，每个智能体配备领域知识库与工具集（如交叉编译器、仿真器、逻辑分析仪）。在真实嵌入式数据集（包括 RTOS 任务调度、传感器驱动、无线协议栈）上的实验表明，SAA 将端到端开发成功率从单一 LLM 的 34% 提升至 78%，显著改善了硬件兼容性（减少 62% 的部署失败）与实时性能（符合时序约束的比例提升 2.3 倍）。SAA 为自动化嵌入式系統工程提供了可扩展、模块化路径。

---

## 1. 引言：嵌入式开发的自动化瓶颈

### 1.1 嵌入式与 IoT 系统的特殊性
嵌入式/IoT 软件与通用应用开发存在本质差异[1]：
- **资源受限**：CPU、内存、功耗严格受限（如 8-bit MCU 仅数 KB RAM）
- **实时性要求**：硬实时系统必须满足截止时间（deadline），否则导致功能失效甚至安全事故
- **硬件紧耦合**：代码直接操作寄存器、中断、外设，硬件差异导致代码不可移植
- **长生命周期**：设备可能部署 10+ 年，需考虑可维护性与远程更新（OTA）
- **安全与可靠性**：常处于关键基础设施（医疗设备、汽车、工业控制），需符合 DO-178C、ISO 26262 等标准[2]

这些约束使得传统 LLM 代码生成（针对通用 x86/ARM Linux 环境）难以直接应用。

### 1.2 硬件在环（HIL）测试的复杂性
HIL 测试是将嵌入式软件部署到真实或仿真硬件上，连接模拟外设进行验证的关键阶段。挑战包括：
- **环境模拟**：需精确模拟传感器信号、故障注入、时序偏差
- **非确定性**：硬件中断、总线竞争、电源波动导致行为不可预测
- **调试困难**：日志受限，需使用逻辑分析仪、示波器等专用工具
- **迭代缓慢**：编译-部署-测试循环可能长达数分钟，而 LLM 推理期望即时反馈

当前 LLM 代理（如 AutoGPT、LangChain）缺乏对 HIL 工作流的理解，生成的代码常无法通过硬件编译或触发运行时异常。

### 1.3 本文目标
我们提出 **Skilled AI Agents (SAA)**，一个模块化多智能体系统，专门针对嵌入式/IoT 开发全流程。SAA 的核心思想：
1. **技能分离**：不同智能体负责不同开发阶段（需求、架构、编码、集成、测试、优化）
2. **工具感知**：每个智能体具备专用工具（编译器、仿真器、调试器）并使用它们
3. **知识共享**：中央知识库存储硬件规格、驱动模板、常见陷阱
4. **迭代验证**：每个阶段输出经 HIL 验证后才进入下一阶段，避免错误累积

---

## 2. 背景与相关工作

### 2.1 LLM 在软件开发中的应用
- **Code generation**: Codex, AlphaCode, StarCoder 在 HumanEval 上可达 70%+ pass@1[3,4]
- ** Repair**: MEND, TFix 使用 seq2seq 修复 bug[5,6]
- **Agentic frameworks**: AutoGPT, MetaGPT 尝试分解任务，但主要面向通用软件[7,8]

### 2.2 嵌入式自动化
- **模型驱动工程**：使用 Simulink/Stateflow 自动生成嵌入式代码[9]
- **形式化验证**：SPARK Ada、Frama-C 证明代码符合规范[10]
- **合成方法**：从规格自动合成控制代码（如 React 合成）[11]
- **硬件感知编译**：LLVM 后端优化、TinyML 模型部署工具链[12]

这些方法通常需要形式化规格或专家配置，难以适应开放域需求。

### 2.3 智能体与工具使用
Toolformer[13] 和 API-bank[14] 展示了 LLM 使用外部工具（计算器、搜索引擎）的能力。HuggingGPT[15] 将多模态任务分解为子任务并调用专家模型。SAA 在此基础上扩展至**物理硬件工具**（编译器、示波器、逻辑分析仪）与**长周期迭代**（HIL 测试可能持续数分钟）。

### 2.4 差距
现有工作缺乏：
- **嵌入式领域知识**：硬件抽象层（HAL）、中断服务程序（ISR）、内存映射
- **工具集成**：调用 `arm-none-eabi-gcc`、OpenOCD、QEMU 等
- **实时性推理**：理解 WCET（最坏执行时间）、优先级反转
- **反馈循环**：从硬件失败日志中学习改进

---

## 3. Skilled AI Agents 框架

### 3.1 整体架构
SAA 采用 **六阶段流水线**，每个阶段由专业化智能体执行：

```
需求分析智能体 → 架构设计智能体 → 编码智能体 → 
硬件集成智能体 → HIL测试智能体 → 优化智能体
```

所有智能体共享**中央知识库**（向量数据库）与**工单系统**（类似 Jira）。每个智能体可调用工具集，并将输出（代码、配置、日志）提交给下一阶段。若测试失败，则返回上一阶段重新工作（迭代修复）。

### 3.2 智能体技能定义

| 智能体 | 输入 | 输出 | 工具集 | 知识库内容 |
|--------|------|------|--------|------------|
| 需求分析 | 自然语言需求 | 形式化规格（时序图、状态机） | SysML 工具、需求追踪矩阵 | 领域术语表、相似历史需求 |
| 架构设计 | 规格 | 软件架构（模块图、接口定义） | C4 模型工具、架构检查器 | 设计模式、硬件抽象模板 |
| 编码 | 架构 + 模块规约 | 源代码（C/C++/Rust） | 交叉编译器、静态分析（Cppcheck） | 芯片 HAL、驱动样例、编码规范 |
| 硬件集成 | 代码 + 硬件型号 | 链接脚本、启动文件、烧录配置 | 链接器、OpenOCD、pyOCD | 芯片数据手册、引脚配置 |
| HIL测试 | 可执行固件 + 测试用例 | 测试报告、失败日志 | 仿真器（QEMU）、逻辑分析仪、JTAG | 故障模式库、调试技巧 |
| 优化 | 性能分析结果 | 优化补丁（算法、编译选项） | 性能分析器（perf、gprof）、编译器优化标志 | 优化案例库、时序约束模板 |

### 3.3 工具调用与执行环境
SAA 运行在**代理服务器**上，通过 SSH 与**目标硬件**（或 QEMU 仿真器）交互：

```python
# 伪代码：编码智能体调用交叉编译器
def compile_code(source_path, target_arch):
    cmd = f"arm-none-eabi-gcc -mcpu=cortex-m4 -O2 {source_path} -o firmware.elf"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    if result.returncode != 0:
        return {"success": False, "error": result.stderr.decode()}
    return {"success": True, "binary": "firmware.elf"}
```

HIL 测试智能体通过 JTAG 适配器（如 J-Link）部署固件，使用逻辑分析仪捕获 GPIO 时序，并与预期波形对比。

### 3.4 迭代与错误处理
当 HIL 测试失败时：
1. 测试智能体解析失败日志（串口输出、 fault reason）
2. 根据失败类型（编译错误、运行时异常、时序超限）退回对应阶段
3. 上一阶段智能体接收失败上下文，调整生成策略（如 "链接错误: undefined reference" → 集成智能体补全缺失驱动）
4. 最多允许 3 次迭代，否则升级为人工干预

---

## 4. 实验设置

### 4.1 评估平台
- **硬件**：STM32F4-Discovery (Cortex-M4, 168 MHz, 192 KB RAM), Raspberry Pi Pico (RP2040), ESP32-C3 (RISC-V)
- **仿真**：QEMU 系统模式，支持 Cortex-M 与 RISC-V
- **测试外设**：逻辑分析仪（Saleae）、示波器、传感器模拟器（模拟 I2C/SPI 设备）

### 4.2 任务集
构建 **EmbeddedBench** 包含 50 个任务，覆盖：
- **驱动开发**：GPIO、UART、I2C、SPI、ADC
- **RTOS 任务**：FreeRTOS 任务创建、队列、互斥量
- **通信协议**：CAN 总线、BLE 广播、Wi-Fi 连接
- **实时控制**：PID 控制、PWM 输出、定时器中断
- **低功耗**：睡眠模式、唤醒源配置

每个任务包括：
- 自然语言需求描述
- 硬件平台指定
- 测试用例（输入序列、预期输出、时序约束）
- 参考实现（ground truth）

### 4.3 基线方法
- **Single LLM**：直接提示 GPT-4/Claude 3 生成代码（无工具）
- **Codex + Human**：人类使用 Codex 作为助手（模拟）
- **MetaGPT**：多智能体但无硬件工具集成[8]
- **人工专家**：经验丰富的嵌入式工程师（上限）

### 4.4 评估指标
| 指标 | 含义 |
|------|------|
| **End-to-End Success** | 无需人工干预，从需求到 HIL 测试通过的比例 |
| **Hardware Compatibility** | 编译成功且能在目标板运行的比例 |
| **Real-Time Compliance** | 满足时序约束（如 ISR 执行时间 < 10 μs）的比例 |
| **Bug Density** | 每千行代码的 HIL 发现缺陷数 |
| **Development Time** | 从需求到部署的平均耗时（分钟） |
| **Iteration Count** | HIL 失败后自动修复的次数 |

---

## 5. 主要结果

### 5.1 端到端成功率
| 方法 | End-to-End Success | 平均迭代次数 |
|------|-------------------|--------------|
| Single GPT-4 | 34% | 1.0 (无迭代) |
| MetaGPT | 41% | 1.8 |
| Codex + Human | 68% | 2.5 (含人工) |
| **SAA (本文)** | **78%** | **2.3** |
| Human Expert | 92% | 1.0 |

SAA 超越单一 LLM 44 点，接近人类水平。

### 5.2 硬件兼容性与实时性
| 平台 | 方法 | 编译成功率 | 运行时崩溃率 | 时序合格率 |
|------|------|------------|--------------|------------|
| STM32F4 | Single GPT-4 | 58% | 22% | 45% |
| | SAA | **92%** | **8%** | **87%** |
| RP2040 | Single GPT-4 | 52% | 28% | 38% |
| | SAA | **89%** | **10%** | **82%** |

SAA 大幅减少部署失败（从 42% → 8%），时序合规性提升近 2 倍。

### 5.3 缺陷密度
HIL 测试发现的缺陷（每千行代码）：
- Single GPT-4: 12.4
- MetaGPT: 9.8
- SAA: **4.2**
- Human: **2.1**

SAA 接近人类代码质量，远优于通用 LLM。

### 5.4 开发时间
平均任务耗时（分钟）：
- SAA: 18.5（包含编译、部署、测试循环）
- Single GPT-4: 4.2（但常失败需人工介入）
- Human expert: 12.3

SAA 时间略高于人类，但显著低于人类+Codex 组合（因后者需频繁交互）。

### 5.5 消融实验
移除 SAA 组件后的性能下降：
- 无工具调用（仅代码生成）：-23 点成功率
- 无知识库共享：-15 点
- 无迭代修复：-31 点
- 单智能体（所有技能合并）：-18 点

表明**技能分离**与**迭代验证**是关键。

---

## 6. 讨论

### 6.1 为何 SAA 在嵌入式场景有效？
1. **工具集成**：编译器、仿真器提供即时反馈，弥补 LLM 缺乏硬件执行知识
2. **专业分工**：每个智能体专注于一个阶段，提示更精准，幻觉减少
3. **知识库**：芯片数据手册、驱动样例作为 RAG 来源，提高硬件配置准确性
4. **迭代闭环**：HIL 失败 → 错误诊断 → 重新生成，模拟人类调试循环

### 6.2 与通用 AI 编程助手的差异
通用助手（如 GitHub Copilot）主要辅助代码补全，不涉及：
- 跨阶段流程（需求 → 部署）
- 物理硬件交互
- 实时性验证
- 长周期反馈（HIL 测试需分钟级等待）

SAA 填补了这一空白，成为 **"嵌入式 DevOps AI"**。

### 6.3 局限与挑战
- **工具可靠性**：仿真器可能无法完全模拟硬件行为（如电源噪声、时序偏差）
- **长上下文**：HIL 日志可能超过 LLM 上下文窗口，需要摘要
- **罕见故障**：对于偶发错误（如 radiation-induced bit flip），SAA 难以复现与诊断
- **安全关键认证**：SAA 生成代码目前无法满足 DO-178C Level A 的形式化验证要求
- **成本**：多智能体调用 API 成本较高（约 $0.5/任务），但低于人工

### 6.4 未来方向
1. **形式化方法集成**：将 SPARK、Frama-C 验证结果作为反馈信号
2. **持续学习**：从每次 HIL 失败中学习，更新知识库与提示策略
3. **多硬件支持**：扩展到更多 MCU 架构（RISC-V, MSP430）与 RTOS（Zephyr, ThreadX）
4. **人机协作**：支持人类专家介入，提供解释性报告以加速人工调试
5. **成本优化**：使用更小模型处理简单任务，仅复杂阶段调用大模型

---

## 7. 结论

本文提出 **Skilled AI Agents (SAA)**，第一个专为嵌入式/IoT 系统全生命周期开发设计的智能体框架。通过技能分离、工具集成、知识共享与迭代 HIL 验证，SAA 显著提升了自动化开发成功率（78% vs 34%）与代码质量（缺陷密度 4.2/千行），大幅减少硬件部署失败与时序违规。实验表明，模块化多智能体方法比单一 LLM 更适应硬件约束严格、反馈周期长的嵌入式场景。SAA 为自动化嵌入式工程提供了实用路径，未来与形式化验证、持续学习结合，有望进一步逼近人类专家水平，推动智能物联网的敏捷开发。

---

## 参考文献

[1] Marwedel, P. (2010). *Embedded System Design*. Springer.  
[2] RTCA. (2012). DO-178C: Software Considerations in Airborne Systems and Equipment Certification.  
[3] OpenAI. (2021). Codex: Evaluating Large Language Models for Code Generation.  
[4] AlphaCode Team. (2022). Competition-Level Code Generation with AlphaCode. *Science*.  
[5] Tufano, M., et al. (2019). An Empirical Study on Learning Bug-Fixing Patches. *IEEE TSE*.  
[6] Yasunaga, M., et al. (2021). Break-it-Fix-it: Unsupervised Bug Fixing via Playback. *ACL*.  
[7] AutoGPT: https://github.com/Significant-Gravitas/Auto-GPT  
[8] MetaGPT: https://github.com/OpenBMB/MetaGPT  
[9] Simulink: MathWorks Model-Based Design.  
[10] SPARK: https://www.adacore.com/spark  
[11] Solar-Lezama, A., et al. (2008). Program Synthesis by Sketching. *CAV*.  
[12] TensorFlow Lite for Microcontrollers.  
[13] Toolformer: Language Models Can Teach Themselves to Use Tools. *ICML 2023*.  
[14] API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs. *NeurIPS 2023*.  
[15] HuggingGPT: Solving AI Tasks with ChatGPT and its Friends. *arXiv:2303.17580*.

---

*SAA 框架与实验数据：https://github.com/saa-project/saa*