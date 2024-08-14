
from langchain_community.document_loaders import UnstructuredPDFLoader

class PDFParser(object):


    def __init__(self, pdf_path):
        self.loader = UnstructuredPDFLoader(pdf_path)

        raise NotImplementedError("PDFParser is not implemented yet")


    def load(self):
        self.load_res = self.loader.load()
        return self.load_res



def main():
    from src.paper2ppt.configs.path_config import RESOURCES_PATH
    from loguru import logger
    paper_path = RESOURCES_PATH / "AWQ-paper.pdf"
    parser = PDFParser(paper_path)
    data = parser.load()
    logger.info(f"Data: {data}")

if __name__ == "__main__":
    main()


#
# API Reference:
# UnstructuredPDFLoader
# loader = UnstructuredPDFLoader("example_data/layout-parser-paper.pdf")
#
# data = loader.load()
