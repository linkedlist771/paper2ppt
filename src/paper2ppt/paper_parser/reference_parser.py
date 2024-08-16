from typing import List

from langchain_core.documents import Document
from pathlib import Path
from loguru import logger
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter


import nltk

from src.paper2ppt.configs.referce_parser_configs import (
    SUPPORTED_REFERENCES_FILE_SUFFIXES,
)

# nltk.download("punkt")
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

header2md = {
    "Header 1": "#",
    "Header 2": "##",
    "Header 3": "###",
}


class ReferenceParser:
    def __init__(self, docx_path):
        # self.loader = UnstructuredMarkdownLoader(docx_path, mode="single")
        suffix = Path(docx_path).suffix
        if suffix not in SUPPORTED_REFERENCES_FILE_SUFFIXES:
            raise ValueError(
                f"Unsupported file suffix: {suffix}. Supported suffixes: {SUPPORTED_REFERENCES_FILE_SUFFIXES}"
            )

        self.docx_path = docx_path

    def merge_metadata_into_documents(self, documents: List[Document]) -> List[Document]:
        new_documents = []
        for doc in documents:
            page_content = doc.page_content
            if doc.metadata:
                format_str = "\n".join([f"{header2md[k]} {v}" for k, v in doc.metadata.items()])
                page_content = f"{format_str}\n{page_content}"
            new_documents.append(Document(page_content=page_content))
        return new_documents

    def load(self):
        # markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        # md_header_splits = markdown_splitter.split_text(markdown_document)

        # load_res = self.loader.load()
        # page_content = load_res[0].page_content
        # (ˇˍˇ) 就不能这样谢谢了
        page_content = Path(self.docx_path).read_text(encoding="utf-8")
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on
        )
        md_header_splits = markdown_splitter.split_text(page_content)
        md_header_splits = self.merge_metadata_into_documents(md_header_splits)
        return md_header_splits


def main():
    from src.paper2ppt.configs.path_config import RESOURCES_PATH

    paper_path = RESOURCES_PATH / "论文主要内容.md"
    try:
        parser = ReferenceParser(paper_path)
        data = parser.load()
        logger.info(
            f"Successfully loaded the document. Number of paragraphs: {len(data)}"
        )
        for idx, paragraph in enumerate(data):
            logger.info(f"Paragraph {idx}: {paragraph}")
            page_content = paragraph.page_content
            logger.info(f"Page content length: {len(page_content)}")
    except Exception as e:
        logger.error(f"An error occurred while processing the document: {str(e)}")
        logger.exception("Full traceback:")


if __name__ == "__main__":
    main()
