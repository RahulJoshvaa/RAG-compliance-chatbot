from semantic_cache import get_cache
from llm_client import generate

cache = get_cache()

while True:
    query = input("Enter the query: ")
    if query == "1":
        break
    else:
        cached = cache.get(query)
        if cached:
            print("Cache HIT")
            print(cached.response)
        else:
            print("Cache MISS")
            answer = generate(query)
            if answer:
                cache.put(query = query, response = answer)
                print("ANSWER FOR THE QUERY")
                print(answer)