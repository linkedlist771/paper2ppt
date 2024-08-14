from typing import List

from langchain_core.documents import Document

from src.paper2ppt.configs.settings import get_settings
from src.paper2ppt.prompt_builder.imitation_prompt import ImitationPrompt
import unify

# First, only generate the txt content, for the image, let's leave them for now.


class ContentGenerator(object):

    generated_contents: List[Document]

    def __init__(
        self, reference_documents: List[Document], related_contents: List[Document]
    ):
        self.reference_documents = reference_documents
        self.related_contents = related_contents

    #  然后这个部分就是最重要的， 怎么生成仿写的内容
    async def generate_contents(self) -> List[Document]:
        # 怎么找到这些match的内容呢？ 我想想，
        # 先用最简单的吧
        for __related, __reference in zip(self.related_contents, self.reference_documents):
            # 这里就是一个简单的复制吧
            __related_content = __related.page_content
            __reference_content = __reference.page_content
            prompt = ImitationPrompt(
                style_reference=__reference_content,
                current_related_text=__related_content,
            )
            rendered_prompt = await prompt.render_prompt()
            client = unify.Unify("gpt-4o@openai", api_key=get_settings().OPENAI_API_KEY)
            res = client.generate(rendered_prompt)
            print(res)
            break
        # raise NotImplemented


async def main():
    dummy_reference = [
        Document(
            page_content="""hI this is a reference document, it is a very good document"""
        ),
        Document(
            page_content="""hI this is a reference document, it is a very good document"""
        ),
        Document(
            page_content="""hI this is a reference document, it is a very good document"""
        ),
    ]

    dummy_related = [
        Document(
            page_content="""hI this is a related document, it is a very good document"""
        ),
        Document(
            page_content="""hI this is a related document, it is a very good document"""
        ),
        Document(
            page_content="""hI this is a related document, it is a very good document"""
        ),
    ]

    generator = ContentGenerator(dummy_reference, dummy_related)
    await generator.generate_contents()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())