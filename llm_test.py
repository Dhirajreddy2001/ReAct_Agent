from dotenv import load_dotenv
from cache.llm_cache import enable_llm_cache
from config.logging import setup_logging
from cache.agent_instance import get_agent
from nodes.utils import as_text  # ✅ reuse the shared utility

EXIT_WORDS = {"exit", "end", "quit", "q"}

def main():
    load_dotenv()
    setup_logging("INFO")
    enable_llm_cache()
    app = get_agent()

    print("\n--- Agent Initialized ---")
    print("Type exit / quit / end to stop\n")

    while True:
        try:
            user = input("You > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Chat !! -- Bye--!! ")
            break

        if not user:
            continue
        if user.lower() in EXIT_WORDS:
            print("\nExiting Chat !! -- Bye--!! ")
            break

        # Pass user input as 'input' key
        state = app.invoke({"input": user})

        thought = state.get("thought")
        output = state.get("output") or state.get("answer") or state.get("result")

        if thought:
            print("Plan >", as_text(thought))
        print("\n \n Assistant >", as_text(output))

if __name__ == "__main__":
    main()
