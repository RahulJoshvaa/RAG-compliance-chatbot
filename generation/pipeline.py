from semantic_cache import get_cache
from llm_client import generate

cache = get_cache()

<<<<<<< HEAD
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
=======
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
>>>>>>> ad4f8f3c309e735c18d0f8579e7f692f948e0480
