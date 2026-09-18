from io import BytesIO

from docling_core.types.io import DocumentStream
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
)


class DocumentIngestion:
    def __init__(self):
        self.converter = DocumentConverter()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

    def process(self, uploaded_file):
        document = DocumentStream(
            name=uploaded_file.filename,
            stream=BytesIO(uploaded_file.read()),
        )

        result = self.converter.convert(document)

        text = result.document.export_to_markdown().strip()

        if not text:
            raise ValueError("The uploaded document is empty.")

        chunks = self.splitter.create_documents(
            texts=[text],
            metadatas=[
                {
                    "source": uploaded_file.filename,
                }
            ],
        )

        return {
            "filename": uploaded_file.filename,
            "chunks": chunks,
            "total_chunks": len(chunks),
        }
