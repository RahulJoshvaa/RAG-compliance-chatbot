from semantic_cache import get_cache
from llm_client import generate

cache = get_cache()

def run_pipeline_wo_cache(query):
    answer = generate(query)

    return answer

def run_pipeline(query):
    cached = cache.get(query)

    if cached:
        print("Cache HIT")
        return cached.response

    print("Cache MISS")

    answer = generate(query)

    if answer:
        cache.put(
            query=query,
            response=answer
        )

    return answer


if __name__ == "__main__":

    while True:

        query = input("Enter the query: ")

        if query == "1":
            break

        answer = run_pipeline(query)

        print("\nANSWER FOR THE QUERY\n")
        print(answer)
