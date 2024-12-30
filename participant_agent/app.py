import os

from redisvl.extensions.llmcache import SemanticCache
from redisvl.extensions.router import Route, SemanticRouter
from redisvl.utils.vectorize import HFTextVectorizer

## This is the code for the whole flow of the overall application even parts that are not included in the agent

REDIS_URL = os.environ.get("REDIS_URL", "redis://host.docker.internal:6379/0")

# Semantic router
blocked_references = [
    "thinks about aliens",
    "corporate questions about agile",
    "anything about the S&P 500",
]

block_route = Route(name="block_list", references=blocked_references)

router = SemanticRouter(
    name="bouncer",
    vectorizer=HFTextVectorizer(),
    routes=[block_route],
    redis_url=REDIS_URL,
    overwrite=True,
)


# Semantic cache
hunting_example = "There's a deer. You're hungry. You know what you have to do..."

semantic_cache = SemanticCache(
    name="oregon_trail_cache",
    redis_url=REDIS_URL,
    distance_threshold=0.1,
)

semantic_cache.store(prompt=hunting_example, response="bang")