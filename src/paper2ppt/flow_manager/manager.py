
from pathlib import Path
from loguru import logger

from src.paper2ppt.configs.referce_parser_configs import SUPPORTED_REFERENCES_FILE_SUFFIXES, \
    SUPPRESSED_PAPERS_FILE_SUFFIXES
from src.paper2ppt.content_generator.generator import ContentGenerator
from src.paper2ppt.paper_parser.pdf_parser import PDFParser
from src.paper2ppt.paper_parser.reference_parser import ReferenceParser


class FlowManager(object):
    """
    This flow manager will control all the process of the ppt generation.
    """
    # SUPPORTED_REFERENCES_FILE_SUFFIXES = [".md"]
    # SUPPRESSED_PAPERS_FILE_SUFFIXES = [".pdf"]

    def __init__(self, paper_path: Path, reference_path: Path):
        assert paper_path.suffix in SUPPRESSED_PAPERS_FILE_SUFFIXES
        assert reference_path.suffix in SUPPORTED_REFERENCES_FILE_SUFFIXES
        self.paper_path = paper_path
        self.reference_path = reference_path

        self.paper_parser = PDFParser(paper_path)
        self.reference_parser = ReferenceParser(reference_path)


    def load(self):
        self.paper_data = self.paper_parser.load()
        self.reference_data = self.reference_parser.load()


    async def generate(self):
        generator = ContentGenerator(reference_documents=self.reference_data, related_contents=self.paper_data)
        res = await generator.generate_contents()
        self.generated_contents = res

    def save(self, save_path: Path):
        if save_path.suffix == ".md":
            with open(save_path, "w") as f:
                for i, page in enumerate(self.generated_contents):
                    f.write(page.page_content)



async def main():
    from src.paper2ppt.configs.path_config import RESOURCES_PATH

    paper_path = RESOURCES_PATH / "AWQ-paper.pdf"
    reference_path = RESOURCES_PATH / "论文主要内容.md"
    flow_manager = FlowManager(paper_path, reference_path)
    flow_manager.load()
    await flow_manager.generate()
    for i, page in enumerate(flow_manager.generated_contents):
        print(f"Page {i}: {page.page_content}")
    save_path = RESOURCES_PATH / "generated_ppt.md"
    flow_manager.save(save_path)
    logger.info(f"Successfully saved the generated ppt to {save_path}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


