from semantic_cache import get_cache
from llm_client import generate
from control_group_test import get_answer
import time
cache = get_cache()

def run_pipeline_wo_cache(query):
    answer = generate(query)

    return answer["answer"]

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
        print("Choose the pipeline for answer generation\n1.Headroom RAG\n2.Traditional RAG")
        option = int(input("Enter the option: "))

        if option == 1:
            start = time.time()
            answer = run_pipeline_wo_cache(query)
            print(f"Time Taken {time.time() - start}")
        elif option == 2:
            start = time.time()
            answer = get_answer(query)
            print(f"Time Taken {time.time() - start}")

        else:
            print("Enter valid option")
            break

        print("\nANSWER FOR THE QUERY\n")
        print(answer)
