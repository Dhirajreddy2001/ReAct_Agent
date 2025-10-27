from typing import Dict, Any
from cache.node_cache import node_cache
from nodes.utils import as_text

@node_cache(ttl=900, key_prefix="answer", include_plan=False)  # 👈 ignore plan in key
def answer_node(state: Dict[str, Any], llm) -> Dict[str, Any]:
    question = state.get("question") or state.get("input") or ""
    plan = state.get("thought", "")

    if not question.strip():
        return {"output": "I didn’t receive a question. Please re-ask in one sentence."}

    prompt = (
        "Using the PLAN, write a clear, concise final answer.\n"
        "Be direct, avoid fluff, and ensure it fully answers the question.\n"
        "Always return the answer in 3–5 bullet points.\n\n"
        f"QUESTION:\n{question}\n\n"
        f"PLAN:\n{plan}\n\n"
        "FINAL ANSWER:"
    )
    resp = llm.invoke(prompt)
    return {"output": as_text(resp)}
