from typing import List

from langchain_core.documents import Document
from tqdm import tqdm
from src.paper2ppt.configs.settings import get_settings
from src.paper2ppt.llm.openai_llm import get_openai_sync_client
from src.paper2ppt.prompt_builder.imitation_prompt import ImitationPrompt
from tqdm.asyncio import tqdm_asyncio
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
    # async def generate_contents(self) -> List[Document]:
    #     # 怎么找到这些match的内容呢？ 我想想，
    #     # 先用最简单的吧
    #     # TODO: more complex logic could be used here
    #     results = []
    #     for __related, __reference in tqdm(zip(
    #         self.related_contents, self.reference_documents
    #     )):
    #         # 这里就是一个简单的复制吧
    #         __related_content = __related.page_content
    #         __reference_content = __reference.page_content
    #         prompt = ImitationPrompt(
    #             style_reference=__reference_content,
    #             current_related_text=__related_content,
    #         )
    #         rendered_prompt = await prompt.render_prompt()
    #         client = get_openai_sync_client()
    #         res = client.generate(rendered_prompt)
    #         # print(res)
    #         results.append(Document(page_content=res))
    #     return results
    #         # break
    #     # raise NotImplemented

    async def generate_single_content(self, related: Document, reference: Document) -> Document:
        prompt = ImitationPrompt(
            style_reference=reference.page_content,
            current_related_text=related.page_content,
        )
        rendered_prompt = await prompt.render_prompt()
        client = get_openai_sync_client()
        res = client.generate(rendered_prompt)
        return Document(page_content=res)

    async def generate_contents(self) -> List[Document]:
        async def process_pair(idx: int, related: Document, reference: Document):
            res = await self.generate_single_content(related, reference)
            return idx, res

        # results = await tqdm_asyncio.gather(*tasks)
        tasks = [
            process_pair(i, related, reference)
            for i, (related, reference) in enumerate(zip(self.related_contents, self.reference_documents))
        ]

        results = [None] * len(tasks)  # Pre-allocate the result list
        total_tasks = len(tasks)

        for f in tqdm_asyncio.as_completed(tasks, total=total_tasks):
            index, result = await f
            results[index] = result

        return results

async def main():
    from loguru import logger
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
    res = await generator.generate_contents()
    for r in res:
        logger.info(r.page_content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
