from langchain_community.document_loaders import PyPDFLoader


class PDFParser(object):

    def __init__(self, pdf_path):
        self.loader = PyPDFLoader(pdf_path)

    def load(self):
        self.load_res = self.loader.load()
        return self.load_res


def main():
    from src.paper2ppt.configs.path_config import RESOURCES_PATH
    from loguru import logger

    paper_path = RESOURCES_PATH / "AWQ-paper.pdf"
    parser = PDFParser(paper_path)
    data = parser.load()
    for i, page in enumerate(data):
        logger.info(f"Page {i}: {page.page_content}")

if __name__ == "__main__":
    main()


#
# API Reference:
# UnstructuredPDFLoader
# loader = UnstructuredPDFLoader("example_data/layout-parser-paper.pdf")
#
# data = loader.load()
