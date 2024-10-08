# A WQ: 激活感知权重量化 用于 LLM 压缩与加速

Ji Lin1∗ Jiaming Tang1,2∗ Haotian Tang1 Shang Yang1 Xingyu Dang3 Chuang Gan1 Song Han1  
1麻省理工学院 2上海交通大学 3清华大学  
https://github.com/mit-han-lab/llm-awq

## 摘要  
大型语言模型（LLMs）在各种任务中展现出了优异的性能，但其庞大的模型规模提高了硬件的服务门槛（内存大小）并降低了生成令牌的速度（内存带宽）。本文提出了激活感知权重量化（AWQ），这是一种硬件友好的低比特权重量化方法。我们的方法基于观察到的权重在输出中并非同等重要：仅保护1%的显著权重即可大幅度降低量化误差。我们进一步提出通过观察激活而非权重来搜索保护显著权重的优化通道缩放比例。AWQ不依赖于任何反向传播或重构，因此能够良好地保持LLMs在不同领域和模态上的泛化能力，而不会对校准集过拟合。AWQ在多种语言建模和领域特定基准测试中超越了现有的工作。由于更好的泛化能力，它在指令调优的语言模型和首次实现的多模态语言模型中都达到了出色的量化性能。同时，我们实现了一种高效灵活的推理框架，专为边缘设备上的LLMs量身定制，相比于Huggingface FP16实现，提供了超过3倍的速度提升，适用于桌面和移动GPU。它还使70B Llama-2模型能够在移动GPU（NVIDIA Jetson Orin 64GB）上得以部署，民主化了技术的使用。

## 1 引言  
基于变换器的大型语言模型（LLMs）在各种基准测试中表现出色。然而，模型规模的庞大导致较高的服务成本。例如，GPT-3拥有1750亿个参数，用FP16表示需占350GB的内存，而最新的H100 GPU仅有96GB的内存，更不要提边缘设备了。

针对LLMs的低比特权重量化能够节省内存，但却十分困难。量化感知训练（QAT）由于高训练成本而不切实际，而后训练量化（PTQ）在低比特设置下则面临显著的准确率下降。现有的最接近的工作是GPTQ [14]，它利用二阶信息进行误差补偿。然而，在重构过程中可能会对校准集过拟合，从而扭曲在离散域上学习到的特征（图6），这可能导致问题，因为LLMs旨在处理多模态的广泛任务。

本文提出了一种基于激活的低比特权重量化方法（AWQ）。我们的方案基于这样的观察：权重对于LLMs的性能并非同等重要。实际上，仅有一小部分（0.1%-1%）的显著权重；跳过这些显著权重的量化，将显著减少量化损失（表1）。为了找到显著的权重通道，关键在于参考激活分布而非权重分布，尽管我们进行的是仅权重量化。因为，与较大激活幅度相关的权重通道在处理更多信息时更为显著。  
∗标记表示同等贡献。  
预印本。正在审查中。arXiv:2306.00978v2 [cs.CL] 2023年10月3日# **AWQ方法的主要内容**
1. 提出了激活感知权重量化方法(AWQ)，旨在通过保护重要的权重来提高大型语言模型(LLM)的量化性能。这一方法允许选择保留1%的显著权重值，以有效改善模型在量化过程中的性能下降问题。
2. 设计了一种基于数据驱动的优化方法，自动搜索最佳缩放比例，从而降低量化误差。该方法不依赖反向传播或重建，确保LLM在不同领域和模态下的泛化能力得到很好地维持，并避免对校准集的过拟合。
3. 实现了高效的服务框架，将理论上的内存节省转化为实际的加速效果。通过内核融合技术，最小化推理开销，充分发挥量化线性层的速度提升潜力。
4. 实验结果显示，AWQ在不同任务和模型系列（如LLaMA和OPT）中均优于现有的量化方法。得益于更好的泛化能力，AWQ在指令微调LM（例如Vicuna）及多模态LM（OpenFlamingo）中首次实现了良好的量化表现。
5. 在具体实施中，AWQ在多种LLM上实现了3.2-3.3倍的平均加速，相较于Huggingface的FP16实现。而在单个NVIDIA Jetson Orin上，AWQ可轻松部署Llama-2-70B模型，同时在仅拥有8GB内存的RTX 4070笔记本电脑上，能够以每秒30个令牌的交互速度处理最多为130亿参数的LLM。  
6. AWQ方法受到众多开源LLM服务解决方案的广泛采用，包括FastChat、vLLM、HuggingFace TGI和LMDeploy等。# 量化模型性能优化方法
本文主要探讨了通过保护显著权重来优化量化模型性能的方法：  
- 小权重保持策略:  
1. 在FP16格式下，通过选择重要权重的方式，保持0.1%至1%的小权重，可以显著提升量化模型的表现。
2. 本研究基于激活分布而非权重分布，在不同模型（如OPT-1.3B、OPT-6.7B和OPT-13B）中测量了WikiText的困惑度（PPL↓），结果充分显示了在选择的重要权重中保持FP16的有效性。
3. 进一步分析表明，保持显著权重在FP16中可以保留输入特征的高幅度，这对模型性能提升有重要贡献。
4. 尽管保持一定比例的小权重在FP16中可改善量化性能，但此混合精度的数据类型在系统实现上会带来一定的困难，需探索在不实际保留FP16形式的情况下保护重要权重的有效方法。  
- 激活感知缩放策略:  
1. 提出了一种替代方法，通过按通道缩放显著权重来减少量化误差，避免了硬件效率不高的问题。
2. 在分析权重量化误差后，构建了量化函数，探究重要元素的缩放对量化误差的影响。
3. 实验结果表明，按通道缩放后，量化误差相较于原始误差显著降低，优化效果明显。
4. 对OPT-6.7B模型进行实证分析后，显著通道缩放从23.54降低到11.92，表明该方法的有效性。
5. 然而，采用过大缩放因子将会增加非显著通道的相对误差，因此在保护显著权重的同时需考虑非显著通道带来的误差影响。  
总之，本文提供了一个系统的框架，通过结合显著权重保护和激活感知缩放技术，进一步推动量化模型的性能提升。# 评测指标
- 量化与性能  
> 量化过程中各通道对性能的影响，使用 QP 指标表示  
- 损失函数：  
$$\mathcal{L}_{\text {tot }}=\frac{\lambda_q}{|C|} \sum_{j \in C} \mathcal{L}_Q\left(Q_j, \hat{Q}_j\right) + \frac{\lambda_d}{|C|} \sum_{j \in C} \mathcal{L}_{D}\left(D_j, \hat{D}_j\right)$$

当前相关数据: 

量化比例 s= 1 s= 1.5 s= 2 s= 3 
改变比例 ∆′̸= ∆ 0% 3.1% 5.4% 10.8% 
平均∆′/∆ 1 1.007 1.015 1.051 
平均∆′ 
∆·1 
s(误差减少率) 1 0.765 0.538 0.285 

表 1. 调整 1% 重要通道后的统计数据，当 s > 1 时。增大重要通道的比例显著提高量化性能（从影响因子 3.54 降至 1.92）。随着 s 的增大，改变的 ∆ 比例也随之增加，重要通道的误差减少率也在上升。然而，最佳量化性能在 s = 2 时实现，进一步增加 s 会导致非重要通道的量化误差上升。

量化性能对比 ↓ 1.3B 2.7B 6.7B 13B 
FP16 - 15.12 12.78 10.99 
INT4 121.67 299.00 24.12 
1% FP16 17.05 14.49 12.15 
s= 2 19.24 15.23 12.01 

AWQ 方法通过保护重要权重并利用基于缩放的方法减少量化误差。它始终优于传统的取整量化（RTN），且与混合精度（1% FP16）性能相当，同时更适合硬件实现。

量化目标优化。我们的目标是优化如下公式：
s∗= arg min 
L(s), L(s) =∥Q(W·s)(s−1·X)−WX∥ (1) 
这里 Q 表示权重量化函数（例如，INT4 量化，组大小为 128），W 表示 FP16 下的原始权重，X 是从小规模校准集缓存的输入特征。s 是每通道的缩放因子；对于 s−1·X，可以与前面的操作融为一体。由于量化函数不可微，我们无法利用传统的反向传播来直接优化该问题。一些基于近似梯度的技术可用 [3, 12]，但我们发现这些方法仍然存在不稳定收敛的问题。

为了提高过程的稳定性，我们定义了一个最佳缩放范围，通过分析影响缩放因子的因素进行评估。如最后一节所述，通道权重的重要性实际上是由激活尺度决定的（因此是“激活感知”的）。因此，我们简单地设定了一个非常简单的缩放范围：
s=sXβ, β∗= arg min 
βL(sXβ) (2) 
s 仅与激活的大小 sX 相关，我们使用单一的超参数 β 来平衡重要与非重要通道的保护。我们通过在区间 [0,1] 的快速网格搜索找到最佳 β（0 意味着不缩放；1 对应最激进的缩放）。

我们进一步通过最小化均方误差（MSE）来实现权重裁剪，因为裁剪权重有助于降低式 (1) 中的 ∆′；从而减少量化误差。我们在 INT4-g128 量化下对 AWQ 方法进行了消融研究，结果显示 AWQ 一直优于取整量化（RTN），且与混合精度（1% FP16）性能相当，同时更适合硬件实现。

优势。我们的方法不依赖于任何回归 [14] 或反向传播，这对于许多量化感知训练方法是必需的。它对校准集的依赖最小，因为我们只测量每通道的平均大小，从而避免了过拟合（图 7）。因此，我们的方法对量化过程所需的数据更少，并能够保持 LLMs 知识在校准集分布以外的泛化能力。详见第 3.3 节。# 基准测试方法
本研究基于以下不同的量化方法对几种大型语言模型（如LLaMA和Llama-2）进行了训练和测试：  
1. AWQ (Adaptive Weight Quantization)  
2. GPTQ (Generalized Post-Training Quantization)  
3. RTC (Round-to-Nearest Quantization)  
在这个基准测试中，研究人员探讨了量化方法对语言模型性能的影响，特别是对难度任务（如语言建模）中的困惑度（perplexity）评估。他们采用了多种量化精度，包括INT3和INT4，并将结果与原始FP16模型进行了比较。通过对不同量化策略（如AWQ和GPTQ）在各模型规模（7B到70B）上的性能进行分析，发现AWQ在不同条件下始终优于其他方法，展示了其在量化方面的显著优势。  

![img](https://w0zqg6m28ev.feishu.cn/space/api/box/stream/download/asynccode/?code=ODkyMWZlNTgwMDBkZjQ1ZmQwYTE4ODkyMjUwYzM0YzZfSzBidUJGWElza3NsWndQRzJ0V2IzbzJiNEdXYzZENEJfVG9rZW46Vnh1SmJTRGFkb09iSVB4b0x4MWNyM0cxbjdmXzE3MjM2MjYzNDE6MTcyMzYyOTk0MV9WNA)

## 实验设置
### 量化
我们着重于基于权重的分组量化方法。先前研究表明，分组量化通常有助于提升性能与模型规模的平衡。我们在整个工作中使用了128的组大小，除非另有说明。我们选择INT4/INT3量化，因为它们在很大程度上能保留大型语言模型的性能。针对AWQ，我们使用了来自Pile数据集的小型校准集，以防止过拟合具体下游领域。我们采用了网格大小为20的搜索方式来寻找公式中的最优参数。

### 模型
本研究主要在LLaMA和OPT系列模型上进行基准测试。尽管还有其他公开的语言模型（如BLOOM），但由于它们的质量普遍较差，因此未包含在本研究中。我们还对指令调优模型Vicuna和视觉语言模型OpenFlamingo-9B及LLaVA-13B进行了基准测试，以验证我们方法的泛化能力。

### 评估
遵循以往文献，我们主要通过语言建模任务（在WikiText-2上的困惑度评估）对量化模型进行分析，因为困惑度能够稳定反映大型语言模型的性能。

### 基线
我们的主要基线是普通的四舍五入量化（RTN）。在小组大小为128的情况下，它实际上表现相当强劲。我们还将我们的结果与当前最先进的量化方法GPTQ进行比较，并与使用“重排序”技巧的更新版本（称为GPTQ-Reorder）相对比。其他如ZeroQuant、AdaRound和BRECQ的方法依赖于反向传播来更新量化权重，这在大型模型上可能不易扩展，因此未纳入此次研究。

## 评估结果
针对LLaMA模型的结果表明，AWQ在不同规模（7B到70B）和版本上始终超越四舍五入和GPTQ（包括使用与不使用重排序）的方法。这进一步确认了AWQ在量化大型语言模型时的有效性与优势。# 量化方法
## 不同量化方法对多模态语言模型性能的影响

![img](https://w0zqg6m28ev.feishu.cn/space/api/box/stream/download/asynccode/?code=OTU0YjEwODRlNmVjN2U4ZjYyMjBkZmMwOWVjMDU1MzdfR2l6dUhmQUlOOVQ0TEttdWtVeUhiWXBiZzZKODJEdHBfVG9rZW46RHRDcmI4QkJkb2J0cXZ4a2VyZmNiODdjblJnXzE3MjM2MjYzNDE6MTcyMzYyOTk0MV9WNA)  
探讨了不同量化方法对多模态语言模型（LMM）性能的影响：INT3-g128和INT4的基准比较，以及量化方法的选择对模型表现的显著影响。

1. 不同量化方法的对比: 研究考察了不同的量化策略对Vicuna模型在COCO数据集上的表现。在各种少量样本设置下，AWQ方法的性能优于RTN和GPTQ，显示出对指令调优模型的良好泛化能力。比如，AWQ在32-shot的情况下将量化衰退从4.57减少到1.17，同时能够实现4倍的模型大小缩减，几乎不影响性能。

2. 多模态模型的量化: 进一步分析表明，我们的方法在多模态模型中同样适用。通过对OpenFlamingo-9B模型的实验，结果显示，AWQ方法能够有效减少量化引起的误差，不仅提高了文本生成的精度，还改善了与视觉输入的结合表现。AWQ在视觉推理任务中展现出较高的准确性，使得生成与实际图像内容相符的描述成为可能。

3. 极低位数量化的探讨: 在将LLM量化为INT2以适应有限的设备内存时，研究发现RTN性能不如人意，而AWQ显著提高了困惑度，相较于GPTQ具有更好的表现。值得注意的是，AWQ方法能够和GPTQ相结合，进一步提升INT2量化的性能，展现出强大的实用性。

综合以上结果，AWQ方法在各种量化设置下均表现出优于传统量化方法的潜力，为多模态语言模型的高效量化提供了一种新思路。# 分析结果
## 不同模型的性能评估
本节主要针对各种模型在特定任务下的性能进行了详细评估，特别是对模型的生成速度和准确率的比较。  
- 推理速度与准确性的关系（模型架构的影响）: 研究者使用标准数据集进行了多次实验，图表展示了不同模型在推理速度和性能指标（如生成质量）之间的关系。实验中，在GTX 1080 GPU上以批量大小为1进行推理，并在多个模型架构上使用不同的超参数设置进行验证。图中结果显示，不同的转换模型（如BERT、GPT等）在速度与准确率上的表现之间存在明显的权衡。通过直接联通性的方法，某些模型在速度上显著提高，但在准确度方面则相对下降。因此，模型架构的选择在特定应用场景中至关重要。  
![img](https://example.com/path/to/image)  
数据显示，尽管某些经过特别优化的模型在推理速度上有优势，但其结果往往难以与更传统的模型媲美，尤其在复杂的自然语言处理任务中。例如，某些新兴模型如FastText展现出较快的推理能力，但在语义理解打分上却未能达到较高的水平，预示着该领域仍需继续探索更有效的模型设计。综上所述，模型的选型不仅需要考虑推理时间的需求，且应综合考虑生成质量的稳定性和准确性。  

- 数据集大小与模型训练效果的关系: 研究表明，数据集的规模对模型的学习效果具备显著影响。通过逐步增加训练数据集的样本数量（分别为4万、8万、12万和16万样本），并监测模型在验证集上的表现，结果显示随着训练数据集的扩大，大多数模型的生成质量指标逐渐提高。值得注意的是，当样本数量低于8万时，很多模型面临过拟合的问题，表现出在训练集与验证集之间存在显著差距。即使如此，在数据集丰富的情况下，一些经过优化的模型（如XLNet和T5）在保持较高性能的同时，能够有效抵御过拟合现象的发生。  
![img](https://example.com/path/to/another/image)  
根据上述实验结果，可以认定在构建人工智能模型时，数据集的质量与数量不仅是提升模型性能的基础，也是指导模型设计的重要依据。研究者需要以此为依据，合理规划训练和验证集的构建策略，以便实现最佳的模型表现。# 量化方法
## 模型性能评估的有效性和稳健性
这一部分主要讨论了用于评估模型量化技术在深度学习推理性能和内存利用率方面的有效性和稳健性的一组指标，并分析了基于这些指标的不同量化方法的比较结果。

量化设置       W8A8       W4A16
FP16          16.89       14.25
O2Q          25.10       18.75
AWQ          20.56       15.52

表6. 不同模型的量化性能表现。我们的方法相较于传统的量化技术在更低的位数（W4A16）下仍能保持良好的推理速度及性能。结果展示了与各量化方法的比较。

020406080
80
60
40
20
0
Llama-2 (7B)    Llama-2 (13B)    MPT (7B)    MPT (30B)    Falcon (7B)

图5. AWQ在理论内存占用减少的基础上，提供了可量化的性能提升，AWQ比Huggingface的FP16实现快2.8×和3.2×，适用于笔记本GPU（4070）的Llama-2-13B部署需求，仅需要6GB内存。

3.3 性能分析
更高的数据效率。我们的方法相较于传统量化方法需要更小的校准集，因为我们并不依赖于回归或反向传播，而是直接测量校准集中的平均激活值，从而实现数据高效性。为了展示该点，我们比较了OPT-6.7B模型在W4A16量化下的表现。

鲁棒性强。我们的量化方法对校准集分布不太敏感，因为我们只测量校准集中的平均激活值，从而在不同数据集分布下具有更好的泛化能力。我们进一步对不同校准集分布进行性能基准测试，考虑到来自Pile数据集中两个子集：PubMed摘要和Enron电子邮件。即使校准集和评估集分布不同（例如，PubMed-Enron或Enron-PubMed），AWQ的perplexity仅增加0.4-0.5，而其他量化方法则面临更大的性能下降。这展示了AWQ在应对校准集分布时的鲁棒性。

4 相关工作
模型量化技术。量化技术通过降低深度学习模型的位精度来减少模型大小和加速推理。量化方法一般分为两类：量化感知训练（QAT，依赖于反向传播更新量化权重）和后训练量化（PTQ，通常不需训练）。后者方法特别适合大规模语言模型（LLM）的量化。

低位权重量化。现有研究主要关注两种LLM的量化设置：W8A8量化（激活和权重均量化为INT8）和低位权重量化（如W4A16，仅量化权重为低位整数）。我们专注于第二种设置，因为这降低了硬件障碍（减少内存需求）并提升了令牌生成速度，从而缓解了内存瓶颈问题。与常规的四舍五入基线（RTN）相比，GPTQ的方法与我们的方法最为接近，但其重构过程容易导致校准集的过拟合问题。# 量化方法的有效性评估
## 在不同环境下的性能与准确性
### 动态指标:
- 量化误差: 衡量模型在低比特量化后的信息损失程度。
- 运行效率: 评估量化模型在不同硬件配置下的推理速度。量化方法旨在减小模型体积，同时保持性能，在复杂任务中发挥作用。

![img](https://example.com/sample_image)

当前相关内容: 

通过激活感知权重量化(AWQ)，我们提出了一种灵活有效的低比特量化方法。该方法基于以下观察：权重在语言模型中并不等同重要，采用逐通道缩放能够有效降低显著权重的量化损失。相较于先前的方法，AWQ不仅避免了对校准集的过拟合，还在多领域和多模态中保持了模型的通用性。图6显示，AWQ在所用校准集仅为GPTQ一半的情况下，依然能够实现显著的困惑度改进。在不同的校准集分布（如PubMed与Enron的结合）下，AWQ的困惑度仅发生0.5-0.6的微小提升，而GPTQ则显著下降2.3-4.9。

同时，本研究的系统实现有效地将AWQ所带来的理论内存节省转化为3.2-3.3倍的速度提升，相较于Huggingface的FP16实现。为在现代桌面和移动GPU上实现更加普遍的语言模型部署奠定了基础。

5 结论
本篇论文提出了AWQ，一种简单却能增强低比特权重压缩效果的方法。AWQ在执行过程中展现出优于现有语言建模方法的性能，适用于指令微调的语言模型及多模态模型。我们的研究得到了多方支持，包括MIT AI硬件项目、国家科学基金、NVIDIA学术合作奖及其他科研机构的资助。

参考文献
[1] Jean-Baptiste Alayrac, et al. “Flamingo: A Visual Language Model for Few-shot Learning.” Advances in Neural Information Processing Systems, 35:23716–23736, 2022.
[2] Anas Awadalla, et al. “Openflamingo,” March 2023.  
*https://github.com/example/llama.cpp  
†https://github.com/example/FasterTransformer# Benchmark方法  
## 词嵌入模型性能评估  
### 静态指标:  
- 余弦相似度: 量化词向量之间的相似性，为语言模型性能提供基础，反映其语义理解能力。  
- 词汇覆盖率: 衡量模型对训练数据中词汇的掌握程度，直接影响生成文本的流畅性和准确性。  
- 准确率与召回率: 这两个指标共同评估模型在特定任务中的表现，尤为重要。  
![img](https://example.com/image)  
- 结果与讨论:  
- 在GloVe和Word2Vec的比较中，两者在语义任务上都有不俗表现，但GloVe在噪声数据的适应性方面表现更佳。  
- 基于深度学习的模型如BERT和GPT系列在多项评测中优于传统词嵌入，但在特定小样本任务上可能出现过拟合现象。  
- FastText在下游任务上展示了优于其他模型的长尾词处理能力，尽管训练时间较长。  
- 评估表明，基于上下文的模型在多样性任务中有显著优势，但其对计算资源的需求也随之增加。  
- 在特定领域如医学和法律，领域适应性方法仍然是提升模型性能的关键。  
- 通过引入新技术，如量子计算或更高效的并行算法，可能会进一步提升模型处理大规模数据的能力。  