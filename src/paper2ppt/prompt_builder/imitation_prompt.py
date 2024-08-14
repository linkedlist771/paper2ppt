from typing import List, Optional
from pydantic import Field

from src.paper2ppt.prompt_builder.base_prompt import BasePrompt


class ImitationPrompt(BasePrompt):
    base_prompt: str = Field(
        default="""\
You are an AI assistant capable of imitating various writing styles. Your task is to create text that mimics a given style while incorporating specific content and context.

Style Reference: 

{self.style_reference}

Current Related Text: 

{self.current_related_text}

Task: Create a new text that imitates the style of the reference, while considering 
the current related text and maintaining the essence of the original style.

{keywords_instruction}

You should just give the answer directly, without any additional information or explanation and follow the style of the reference text. Ensure that your output is unique, relevant, and faithful to the provided style and context.
The output should be in the specified language: {self.output_language.value}.\
""",
        description="Base instructions for the imitation task",
    )
    style_reference: str = Field(
        ..., description="Reference text for the style to imitate"
    )
    current_related_text: str = Field(
        ..., description="Current related text for the style to imitate"
    )
    content_keywords: Optional[List[str]] = Field(
        default=None, description="Keywords to include in the imitated content"
    )

    async def render_prompt(self) -> str:
        keywords_instruction = ""
        if self.content_keywords:
            keywords_instruction = f"Please include the following keywords: {', '.join(self.content_keywords)}"

        return self.base_prompt.format(
            self=self, keywords_instruction=keywords_instruction
        )


async def main():
    prompt = ImitationPrompt(
        style_reference="""论文主要内容 
1. 引入了两个新的机器学习力场(MLFF)基准数据集SAMD23,反映了在各种情况下对SiN和HfO进行的半导体模拟。这为研究人员提供了标准的数据集来开发和评估MLFF模型在半导体材料模拟中的性能。
2. 提供了一个框架来促进MLFF模型的开发。该框架可能包含数据预处理、模型训练、性能评估等组件,方便研究人员快速开发和测试模型。
3. 为SiN和HfO提供了基准测试,并提出了五个模拟指标来评估MLFF模型在模拟中的预测性能和外推能力。这些指标为全面评价模型在半导体材料模拟中的表现提供了标准。
4. 通过对10个MLFF模型进行比较分析,提出了一个基线训练方案和模型选择策略,以在实际模拟中使用性能最优的模型。这为研究人员在众多MLFF模型中选择最适合特定半导体模拟任务的模型提供了指导。""",
        current_related_text="""
        Abstract

Psychological measurement is essential for mental health, self-understanding, and personal development. Traditional methods, such as selfreport scales and psychologist interviews, often face challenges with engagement and accessibility. While game-based and LLM-based tools have been explored to improve user interest and automate assessment, they struggle to balance engagement with generalizability. In this work, we propose PsychoGAT (Psychological Game AgenTs) to achieve a generic gamification of psychological assessment. The main insight is that powerful LLMs can function both as adept psychologists and innovative game designers.

By incorporating LLM agents into designated roles and carefully managing their interactions, PsychoGAT can transform any standardized scales into personalized and engaging interactive fiction games. To validate the proposed method, we conduct psychometric evaluations to assess its effectiveness and employ human evaluators to examine the generated content across various psychological constructs, including depression, cognitive distortions, and personality traits. Results demonstrate that PsychoGAT serves as an effective assessment tool, achieving statistically significant excellence in psychometric metrics such as reliability, convergent validity, and discriminant validity. Moreover, human evaluations confirm PsychoGAT's enhancements in content coherence, interactivity, interest, immersion, and satisfaction.
        """,
        content_keywords=[],
    )
    from loguru import logger

    logger.info(await prompt.render_prompt())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
