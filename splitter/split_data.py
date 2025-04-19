import os
from pathlib import Path
from langchain.docstore.document import Document
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

# from your_module import split_text

SKIP_EXTENSIONS = {".env", ".lock", ".yml", ".md", ".mjs"}
SKIP_FILES = {"README.md", "tsconfig.json", "package-lock.json"}
SKIP_DIRS = {".git", "assets", "node_modules", "__pycache__"}

EXT_TO_LANGCHAIN = {
    ".py": Language.PYTHON,
    ".ts": Language.TS,
    ".js": Language.JS,
}

def is_valid_file(file_path: Path):
    return (
        file_path.suffix not in SKIP_EXTENSIONS and
        file_path.name not in SKIP_FILES and
        not any(part in SKIP_DIRS for part in file_path.parts)
    )

def collect_documents_from_repo(repo_path: str) -> list[Document]:
    repo_path = Path(repo_path)
    documents = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for file in files:
            full_path = Path(root) / file
            # print(full_path)
            if is_valid_file(full_path):
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    doc = Document(
                        page_content=content,
                        metadata={"source": str(full_path), "extension": full_path.suffix}
                    )
                    documents.append(doc)
                except Exception as e:
                    print(f"⚠️ Skipped {full_path} due to error: {e}")

    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # document = chunks[10]
    # print(document.page_content)
    # print(document.metadata)

    return chunks

def splitter_main():
    repo_path = "./quiz-edloops"
    docs = collect_documents_from_repo(repo_path)
    print(f"✅ Collected {len(docs)} valid files.")
    split_chunks = split_text(docs)

    return split_chunks
