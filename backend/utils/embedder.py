from sentence_transformers import SentenceTransformer
import torch

model = SentenceTransformer('all-mpnet-base-v2')

def embed_text(text):
    with torch.no_grad():
        embeddings = model.encode(text)
    return embeddings.tolist()
