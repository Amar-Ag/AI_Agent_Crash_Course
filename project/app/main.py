import ingest
import search_agent 
import logs

import asyncio


REPO_OWNER = "DataTalksClub"
REPO_NAME = "data-engineering-zoomcamp"


def initialize_index():
    print(f"Starting AI FAQ Assistant for {REPO_OWNER}/{REPO_NAME}")
    print("Initializing data ingestion...")

    index, vindex, embedding_model = ingest.index_data(REPO_OWNER, REPO_NAME)
    print("Data indexing completed successfully!")
    return index, vindex, embedding_model


def initialize_agent(index, vindex, embedding_model):
    print("Initializing search agent...")
    agent = search_agent.init_agent(index, vindex, embedding_model, REPO_OWNER, REPO_NAME)
    print("Agent initialized successfully!")
    return agent


def main():
    index, vindex, embedding_model = initialize_index()
    agent = initialize_agent(index, vindex, embedding_model)
    print("\nReady to answer your questions!")
    print("Type 'stop' to exit the program.\n")

    while True:
        question = input("Your question: ")
        if question.strip().lower() == 'stop':
            print("Goodbye!")
            break

        print("Processing your question...")
        response = asyncio.run(agent.run(user_prompt=question))
        logs.log_interaction_to_file(agent, response.new_messages())

        print("\nResponse:\n", response.output)
        print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    main()
