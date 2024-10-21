import os
import vertexai
from vertexai.preview import rag

PROJECT_ID = "tw-rd-tam-jameslu"
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
vertexai.init(project=PROJECT_ID, location=LOCATION)
EMBEDDING_MODEL = "publishers/google/models/text-embedding-004"
embedding_model_config = rag.EmbeddingModelConfig(publisher_model=EMBEDDING_MODEL)

def initialize_love_talk_corpus():
    rag_corpus = rag.create_corpus(
        display_name="love_talk",
        embedding_model_config=embedding_model_config
    )
    INPUT_GCS_BUCKET = "gs://love-judge/sao-word/love_talk.txt"
    rag.import_files(
        corpus_name=rag_corpus.name,
        paths=[INPUT_GCS_BUCKET],
        chunk_size=1024,
        chunk_overlap=100,
        max_embedding_requests_per_min=900,
    )
    print(f"Love Talk RAG Corpus created and initialized. Corpus name: {rag_corpus.name}")
    return rag_corpus.name

def initialize_reconciliation_corpus():
    rag_corpus = rag.create_corpus(
        display_name="reconciliation",
        embedding_model_config=embedding_model_config
    )
    INPUT_GCS_BUCKET = "gs://love-judge/reconciliation/love_suggest.txt"
    rag.import_files(
        corpus_name=rag_corpus.name,
        paths=[INPUT_GCS_BUCKET],
        chunk_size=1024,
        chunk_overlap=100,
        max_embedding_requests_per_min=900,
    )
    print(f"Reconciliation RAG Corpus created and initialized. Corpus name: {rag_corpus.name}")
    return rag_corpus.name

if __name__ == "__main__":
    love_talk_corpus_name = initialize_love_talk_corpus()
    reconciliation_corpus_name = initialize_reconciliation_corpus()
    
    # 将 corpus_name 保存到文件中，以便主脚本使用
    with open("rag_corpus_names.txt", "w") as f:
        f.write(f"Love Talk Corpus: {love_talk_corpus_name}\n")
        f.write(f"Reconciliation Corpus: {reconciliation_corpus_name}\n")