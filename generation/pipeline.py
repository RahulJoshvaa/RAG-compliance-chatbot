from semantic_cache import get_cache
from llm_client import generate

while True:
    query = input("Enter the query: ")
    if query == "1":
        break
    else:
        cache = get_cache()
        cached = cache.get(query)
        if cached:
            print("Cache HIT")
            print(cached.response)
        else:
            print("Cache MISS")
            answer = generate(query)
            if answer:
                cache.put(query = query, response = answer)
                print(answer)