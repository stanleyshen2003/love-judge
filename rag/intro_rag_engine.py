# Use the environment variable if the user doesn't provide Project ID.
import os
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
# from google.cloud import aiplatform
# import vertexai

PROJECT_ID = "semiotic-effort-439102-k9"  # @param {type:"string", isTemplate: true}
# if PROJECT_ID == "":
    # PROJECT_ID = str(os.environ.get("GOOGLE_CLOUD_PROJECT"))

LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

vertexai.init(project=PROJECT_ID, location=LOCATION)
from vertexai.preview import rag
from vertexai.preview.generative_models import GenerativeModel, Tool
# Currently supports Google first-party embedding models
EMBEDDING_MODEL = "publishers/google/models/text-embedding-004"  # @param {type:"string", isTemplate: true}
embedding_model_config = rag.EmbeddingModelConfig(publisher_model=EMBEDDING_MODEL)

rag_corpus = rag.create_corpus(
    display_name="my-rag-corpus", embedding_model_config=embedding_model_config
)
print(rag.list_corpora())

def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

# 使用示例
filename = "test.txt"
content = "Here's a demo using RAG Engine on Vertex AI."

write_to_file(filename, content)
print(f"Content has been written to {filename}")
rag_file = rag.upload_file(
    corpus_name=rag_corpus.name,
    path="test.txt",
    display_name="test.txt",
    description="my test file",
)

INPUT_GCS_BUCKET = (
    "gs://love-judge/sao-word/love_talk.txt"
)

response = rag.import_files(
    corpus_name=rag_corpus.name,
    paths=[INPUT_GCS_BUCKET],
    chunk_size=1024,  # Optional
    chunk_overlap=100,  # Optional
    max_embedding_requests_per_min=900,  # Optional
)
# response = rag.import_files(
#     corpus_name=rag_corpus.name,
#     paths=["https://drive.google.com/drive/folders/{folder_id}"],
#     chunk_size=512,
#     chunk_overlap=50,
# )
# Create a tool for the RAG Corpus
rag_retrieval_tool = Tool.from_retrieval(
    retrieval=rag.Retrieval(
        source=rag.VertexRagStore(
            rag_corpora=[rag_corpus.name],
            similarity_top_k=10,
            vector_distance_threshold=0.5,
        ),
    )
)
# Load tool into Gemini model
rag_gemini_model = GenerativeModel(
    "gemini-1.5-flash-001",  # your self-deployed endpoint
    tools=[rag_retrieval_tool],
)
response = rag_gemini_model.generate_content("我喜歡你的下一句話是什麼")

print(response.text)