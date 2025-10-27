from typing import Dict, Any
from nodes.utils import as_text

def reason_node(state: Dict[str, Any], llm) -> Dict[str, Any]:
    # Always capture the user input explicitly
    user_q = state.get("input", "")
    prompt = (
        "You are a planner. Think step-by-step and outline how you will answer.\n"
        "Return 2–4 concise bullet points only.\n\n"
        f"QUESTION: {user_q}"
    )
    resp = llm.invoke(prompt)
    # IMPORTANT: echo both 'input' and a stable 'question' key so downstream always has it
    return {
        "input": user_q,              # keep original for downstream nodes
        "question": user_q,           # stable copy used by answer_node
        "thought": as_text(resp),
    }
