import time

from sentence_transformers import SentenceTransformer
from headroom.cache.semantic import SemanticCache
from headroom.cache.semantic import SemanticCacheConfig

# -------------------------
# Embedding Model
# -------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    return model.encode(text).tolist()

# -------------------------
# Cache
# -------------------------

config = SemanticCacheConfig(
    similarity_threshold=0.80
)

def get_cache():

    return SemanticCache(
        config=config,
        embedding_fn=embed
    )

