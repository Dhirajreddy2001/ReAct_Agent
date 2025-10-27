ReAct_Agent is a modular, multi-layered AI Agent Framework built with LangGraph, LangChain, and AWS Bedrock Claude models.
It demonstrates a complete end-to-end conversational AI workflow — including agent orchestration, semantic reasoning, and three-level caching for maximum performance.


Environment Set-Up

Create .env file with following Parameters:

# Model configuration
#MODEL_STRING=bedrock_converse:us.anthropic.claude-3-5-haiku-20241022-v1:0

MODEL_STRING=us.anthropic.claude-3-5-haiku-20241022-v1:0
MODEL_MAX_TOKENS=3000


# AWS Bedrock credentials
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1


LLM_CACHE_PATH=.lc_cache.sqlite3


Project Structure:
ReAct_Agent/
│
├── llm_test.py               # Entry point for manual testing
│
├── graph.py                  # Defines state graph and connects nodes
│
├── llm/
│   └── claude.py             # Claude model loader (via AWS Bedrock)
│
├── nodes/
│   ├── answer.py             # Final answer generation node
│   ├── utils.py              # Helper functions (normalize, as_text, etc.)
│
├── cache/
│   ├── cache_class.py        # Thread-safe TTL-based in-memory cache
│   ├── agent_instance.py     # Persists agent instance between runs
│   ├── node_cache.py         # Node-level cache decorator
│   ├── llm_cache.py          # SQLite-backed persistent LLM cache
│
├── config/
│   └── logging.py   # Logging setup (console + file)
|   |__ settings.py    # Holds settings for this model      
│
├── .env                      # Environment variables
└── requirements.txt


Setup and Running:

git clone <repo_url>
cd REACT_AGENT
uv venv
source .venv/bin/activate

uv pip install -r requirements.txt or python pip install -r requirements.txt


**
Run Agent :

uv run python llm_test.py
**
