#from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
#from langchain.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
#from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
import os
import shutil
import dotenv

DATA_PATH = "data/yz-pdfs"
CHROMA_PATH = "chroma"

dotenv.load_dotenv()

def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    chunks = calculate_chunk_ids(chunks)

    save_to_chroma(chunks)


def load_documents():
    md_files = [file for file in os.listdir(DATA_PATH) if file.endswith(".md")]
    pdf_files = [file for file in os.listdir(DATA_PATH) if file.endswith(".pdf")]
    
    if md_files:
        loader = DirectoryLoader(DATA_PATH, glob="*.md")
    elif pdf_files:
        loader = PyPDFDirectoryLoader(DATA_PATH)
    else:
        raise ValueError("No valid documents found in the data directory.")
    
    documents = loader.load()
    return documents

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    # clear db
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # create new DB from the documents
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
