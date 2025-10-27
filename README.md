# 🧠 ReAct_Agent

**ReAct_Agent** is a **modular, multi-layered AI Agent Framework** built with **LangGraph**, **LangChain**, and **AWS Bedrock Claude models**.  
It demonstrates a complete **end-to-end conversational AI workflow** — including **agent orchestration**, **semantic reasoning**, and a **three-level caching layer** for optimal performance and cost efficiency.

---

## ⚙️ Key Features

- 🧩 **Composable LangGraph State Graph** for reasoning and planning  
- 🤖 **Claude 3.5 (via AWS Bedrock)** integration for natural language and tool reasoning  
- 💾 **3-Level Cache System**
  - Node-level (in-memory)
  - LLM-level (SQLite)
  - Agent instance (persistent session cache)
- 🪶 **Logging & Monitoring**
  - Structured logs via `config/logging.py`
  - OpenTelemetry tracing and metrics to **Jaeger**, **Prometheus**, and **Grafana**
- 🧠 **Semantic reasoning flow** with ReAct-style architecture (Reason + Act + Observe)
- 🧱 **Modular Design** — easy to extend with new nodes, tools, or memory backends

---

## 🧰 Environment Setup

### 1️⃣ Create a `.env` file at project root:

```bash
# ------------ Model Configuration -------------
MODEL_STRING=us.anthropic.claude-3-5-haiku-20241022-v1:0
MODEL_MAX_TOKENS=3000

# ------------ AWS Bedrock Credentials ----------
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1

# ------------ Cache ----------------------------
LLM_CACHE_PATH=.lc_cache.sqlite3

# ------------ OpenTelemetry --------------------
OTEL_SERVICE_NAME=react-agent
OTEL_RESOURCE_ATTRIBUTES=app=react-agent,env=dev
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
OTEL_METRICS_EXPORTER=otlp
OTEL_TRACES_EXPORTER=otlp
OTEL_TRACES_SAMPLER=parentbased_always_on
OTEL_PYTHON_LOG_CORRELATION=true
OTEL_EXPERIMENTAL_ENABLE_RUNTIME_METRICS=true
```

---

## 🧱 Project Structure

```
ReAct_Agent/
│
├── llm_test.py               # Entry point for manual / debugging runs
│
├── graph.py                  # LangGraph state machine definition
│
├── llm/
│   └── claude.py             # Claude model interface (via AWS Bedrock)
│
├── nodes/
│   ├── answer.py             # Final response composition
│   ├── utils.py              # Normalization, formatting, etc.
│
├── cache/
│   ├── cache_class.py        # Thread-safe TTL in-memory cache
│   ├── agent_instance.py     # Persistent session agent
│   ├── node_cache.py         # Node-level decorator
│   ├── llm_cache.py          # SQLite-based LLM cache
│
├── config/
│   ├── logging.py            # File + console logging setup
│   └── settings.py           # Model + cache configuration
│
├── observability/
│   ├── docker-compose.yml    # Grafana, Prometheus, Jaeger, Collector stack
│   ├── prometheus.yml        # Scrape config for metrics
│   └── otel-collector.yaml   # Collector routes traces + metrics
│
├── telemetry.py              # Initializes OpenTelemetry tracer + meter
│
├── .env                      # Environment configuration
└── requirements.txt           # All dependencies
```

---

## 🐍 Installation & Running

### 1️⃣ Clone & Setup Virtual Environment

```bash
git clone <repo_url>
cd ReAct_Agent
uv venv
source .venv/bin/activate
```

### 2️⃣ Install Dependencies

```bash
uv pip install -r requirements.txt
# or
python -m pip install -r requirements.txt
```

---

## 🪄 Running the Agent

### Run Locally
```bash
python llm_test.py
```

### Run with uv
```bash
uv run python llm_test.py
```

Your agent will load the AWS Bedrock Claude model, initialize the graph, and begin reasoning interactively.

---

## 📈 Observability (Docker-based Stack)

### 1️⃣ Start Jaeger + Prometheus + Grafana + Collector

From the project root:
```bash
docker compose up -d
```

Services launched:
| Service | Port | Description |
|----------|------|-------------|
| Jaeger | 16686 | Trace visualization |
| Prometheus | 9090 | Metrics storage |
| Grafana | 3000 | Dashboards (login: admin / Password123) |
| OTel Collector | 4318 | Receives OTLP traces & metrics |

---

### 2️⃣ Verify Setup

#### 🧩 Check Targets
Open Prometheus → [http://localhost:9090/targets](http://localhost:9090/targets)  
You should see:
- `otel-collector-pipeline`
- `otel-collector-internal`  
both marked **UP** ✅

#### 🧩 Check Jaeger
Open Jaeger → [http://localhost:16686](http://localhost:16686)  
Select **Service = react-agent** → You’ll see live trace spans from `llm_test.py`.

#### 🧩 Check Grafana
Open Grafana → [http://localhost:3000](http://localhost:3000)  
Login: `admin / Password123`  
Add Prometheus datasource → URL: `http://prometheus:9090`

Example queries:
```promql
up
otelcol_process_uptime
react_agent_smoke_test_counter
```