import os
import time
import json
import tiktoken
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

def evaluate_retrieval_performance(retrieved_contexts, pricing_per_1k_tokens=0.0015):
    """
    Calculates the automated efficiency and cost metrics.
    """
    # the next line loads the GPT4 tokenizer logic
    tokenizer = tiktoken.get_encoding("cl100k_base")
    # converts the paragraphs into one single massive text block
    full_context_text = " ".join([chunk["text"] for chunk in retrieved_contexts])
    
    tokens = len(tokenizer.encode(full_context_text))
    # We leave the cost calculation here to show project leads what a cloud API *would* have cost
    cost_per_single_query = (tokens / 1000) * pricing_per_1k_tokens
    cost_per_1k_queries = cost_per_single_query * 1000
    
    return {
        "tokens_per_query": tokens,
        "cost_per_1k_queries": round(cost_per_1k_queries, 4)
    }

def calculate_sources_fit_rate_ai(query, retrieved_contexts):
    """
    Calculates the Sources-fit rate automatically using a FREE OpenRouter Cloud Model.
    Requires OPENROUTER_API_KEY to be set in your environment variables.
    """
    print(f"\n[AI EVALUATION] Grading Context Precision for: '{query}'")
    
    # Initialize the OpenRouter connection using the OpenAI connector structure
    try:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("API Key missing from Environment Variables")
            
        ai_judge = ChatOpenAI(
            # Using Meta's Llama 3.1 8B model via OpenRouter's 100% free tier
            model="meta-llama/llama-3.1-8b-instruct:free", 
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0
        )
    except Exception as e:
        print("[Error] Could not initialize OpenRouter AI Judge. Is your OPENROUTER_API_KEY set?")
        return {"relevant_chunks": 0, "total_chunks": len(retrieved_contexts), "sources_fit_rate_percent": 0.0}

    relevant_count = 0
    total_chunks = len(retrieved_contexts)
    
    for idx, chunk in enumerate(retrieved_contexts):
        print(f"--- Grading Match #{idx + 1}... ", end="", flush=True)
        
        # The prompt that forces the AI to act as a strict classifier
        system_prompt = SystemMessage(content="You are a strict compliance evaluator. Your only job is to check if the provided text contains the factual answer to the user's query. Respond strictly with 'YES' or 'NO'. Do not explain your reasoning.")
        user_prompt = HumanMessage(content=f"Query: {query}\n\nText to evaluate: {chunk['text']}")
        
        # Request evaluation from OpenRouter
        response = ai_judge.invoke([system_prompt, user_prompt])
        verdict = response.content.strip().upper()
        
        if "YES" in verdict:
            print("Verdict: PASS (Relevant)")
            relevant_count += 1
        else:
            print("Verdict: FAIL (Irrelevant)")
            
    # Calculate the exact percentage
    sources_fit_rate = (relevant_count / total_chunks) * 100 if total_chunks > 0 else 0.0
        
    return {
        "relevant_chunks": relevant_count,
        "total_chunks": total_chunks,
        "sources_fit_rate_percent": round(sources_fit_rate, 2)
    }

def retrieve_context(query, top_k=3):
    # starts the latency stopwatch
    start_time = time.perf_counter()
    # these are the path to find the local database folder
    db_path = "./chroma_db"
    parent_store_path = "parent_document_store.json"

    # initialize the embedding model to turn the query into vector array for searching
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Connects to ChromaDB or our local vector database
    chroma_client = chromadb.PersistentClient(path=db_path)
    try:
        # tries to open the database containing the tiny search vector
        child_collection = chroma_client.get_collection(name="compliance_child_chunks")
    except Exception:
        print("[Error] Could not find the vector database collection.")
        return

    # Load the Parent document mapper or the JSON vault where the files are stored
    try:
        with open(parent_store_path, "r") as file:
            parent_document_store = json.load(file)
    except FileNotFoundError:
        print("[Error] Parent document store file missing.")
        return

    print(f"\n[Query] Searching baseline database for: '{query}'")

    # searches the database for the top k chunks that matches the query using tiny child vector
    results = child_collection.query(
        query_texts=[query],
        n_results=top_k
    )

    # extracting the metadata tags from the search results containing the parent ID to map them back to their original parent paragraphs
    metadatas = results['metadatas'][0] if results['metadatas'] else []
    # keep track of the duplicates
    seen_parents = set()
    # holds the final text
    retrieved_contexts = []

    for meta in metadatas:
        parent_id = meta.get("parent_id")
        # this line helps us to prevent from pulling the exact same paragraph twice
        if parent_id and parent_id not in seen_parents:
            seen_parents.add(parent_id)
            # uses the parent id to access the data for that specific original paragraph
            if parent_id in parent_document_store:
                parent_data = parent_document_store[parent_id]
                # saves the clean text data along with the metadata
                retrieved_contexts.append({
                    "text": parent_data["text"],
                    "source": parent_data["metadata"]["source_file"],
                    "page": parent_data["metadata"]["page_number"]
                })

    # stops the latency stopwatch
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000

    # this line runs the Automated AI Sources-Fit Grader (Via Free OpenRouter Model)
    fit_metrics = calculate_sources_fit_rate_ai(query, retrieved_contexts)

    # calculates the rest automated metrics
    metrics = evaluate_retrieval_performance(retrieved_contexts)
    
    # prints the final results here
    print("\n=== SYSTEM PERFORMANCE METRICS ===")
    print(f"Latency per query: {latency_ms:.2f} ms")
    print(f"Tokens per query: {metrics['tokens_per_query']} tokens")
    print(f"Projected Cloud Cost per 1k queries: ${metrics['cost_per_1k_queries']} (Actual OpenRouter Cost: $0.00)")
    print(f"Sources-fit rate (AI Graded): {fit_metrics['sources_fit_rate_percent']}% ({fit_metrics['relevant_chunks']}/{fit_metrics['total_chunks']} chunks relevant)")
    print("==================================\n")

    return retrieved_contexts

if __name__ == "__main__":
    # Test your baseline pipeline with a specific question you know the answer to
    sample_query = "What are the rules regarding risk management framework and ICT compliance?"
    retrieve_context(sample_query, top_k=3)