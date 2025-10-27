from langgraph.graph import StateGraph
from typing_extensions import TypedDict, NotRequired
from llm.claude import load_claude
from nodes.reason import reason_node
from nodes.answer import answer_node

class AgentState(TypedDict, total=False):
    input: str
    question: NotRequired[str]
    thought: NotRequired[str]
    output: NotRequired[str]

def build_graph():
    llm = load_claude()
    g = StateGraph(AgentState)

    g.add_node("reason", lambda s: reason_node(s, llm))
    g.add_node("answer", lambda s: answer_node(s, llm))

    g.set_entry_point("reason")
    g.add_edge("reason", "answer")
    g.set_finish_point("answer")
    return g.compile()
