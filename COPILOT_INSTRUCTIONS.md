# GitHub Copilot Instructions for agentic-ai ✅

> Quick guide for using GitHub Copilot (and any AI assistant) productively with this repository.

---

## Project summary 🔧
- Purpose: A small conversational agent that uses OpenAI's Chat API to answer user prompts, call small helper tools, and generate/execute SQL queries against local SQLite data.
- Key runtime entrypoint: `src/agentic_ai/run_agent.py` (interactive CLI loop).
- Primary functionality files:
  - `src/agentic_ai/functions/agent_orchestrator.py` — orchestrates chat + tool calls.
  - `src/agentic_ai/functions/agents.py` — tool implementations (weather, price, vacation, sales).
  - `src/agentic_ai/functions/llm_fn.py` — helpers and model runner.
  - `src/agentic_ai/functions/sqldb_fn.py` — SQLite helpers.
  - `src/agentic_ai/functions/ui_fn.py` — UI/conversational glue.
  - `src/agentic_ai/models/prompt.py` & `models/memory.py` — prompt templates and simple in-memory memory.

## Quick start (developer) ▶️
1. Create and activate a Python 3.11+ virtualenv.
2. Install deps: `pip install -r requirements.txt` (note: `langchain` is included but minimally used).
3. For running tests: `pip install pytest` (not in requirements.txt yet).
4. Set environment variables (create `.env` or export):
   - `OPENAI_API_KEY` — required to call OpenAI API.
   - `WEATHER_API_KEY` — optional (used by `get_current_weather`).
5. Run interactive agent:
   - `python src/agentic_ai/run_agent.py`  
   - Type prompts at the CLI, `exit` to quit.

## Important configuration notes ⚠️
- The active LLM model is set in `src/agentic_ai/config.py` (`MODEL_NAME`). Default is `gpt-3.5-turbo`. Change to a compatible model (e.g., `gpt-4o` or newer) if you have access.
- Database path is `config.database` (current default points to `./data/History1`). Confirm this is a SQLite file or change as needed.
- The code uses the OpenAI Python client and the `tools`/`tool_calls` fields in chat completions — adjust code if API surface changes.

## Suggested Copilot tasks (high value) 💡
Use Copilot to help with these tasks. For each prompt below, paste it into your editor as a comment and follow up with code completions.

1. Add type hints and return types to all public functions.
2. Improve error handling around network and DB calls (timeouts, request exceptions, SQL errors).
3. Expand unit tests for `agents.get_sales` and other functions (basic tests exist).
4. Add a GitHub Actions workflow to run linters and tests.
5. Add comprehensive logging and error handling patterns.
6. Add input validation for tool call arguments in `agent_orchestrator`.
7. Add a small CLI argument parser to `run_agent.py` for `--db` and `--model` overrides.

### Example Copilot prompt to add a new tool
"Add a new function `get_exchange_rate(from_currency: str, to_currency: str) -> str` to `agents.py` that calls a free public exchange-rate API, returns a JSON string with the rate, and add the corresponding tool spec to `agent_orchestrator.py`. Include unit tests with network call mocked."

## How Copilot can be most useful here 🛠️
- Implementing small helpers (type annotations, docstrings, input validation).
- Generating unit tests/mocks for HTTP and DB interactions.
- Writing consistent docstrings, README updates, and `.env.example` files.
- Refactoring repeated patterns (e.g., consistent logging, standardized error handling).
- Creating small feature branches and PR descriptions (use suggested commit message templates).

## Code style & reviewer guidelines ✅
- Keep functions small and single-purpose.
- Add docstrings for exported functions and classes.
- Prefer explicit over implicit I/O (pass `db_file` rather than relying on globals where feasible).
- Validate external inputs before passing to SQL or HTTP requests.

## Security & privacy notes 🔒
- Never commit real API keys or `.env` files. Use `.env` locally and add `.env` to `.gitignore` (already present).
- When creating unit tests that need API responses, **mock** HTTP calls (e.g., with `requests-mock` or `responses`).

## Suggested TODOs (low-effort, high payoff) 📋
- Add `pytest` to requirements.txt as dev dependency (tests exist but pytest not listed).
- Add a `Makefile` or `poetry` config for reproducible dev setup.
- Add GitHub Actions CI workflow to run tests automatically.
- Add more comprehensive error handling and logging throughout the codebase.

---

✅ **Setup status:** Core files (`.env.example`, `tests/`, this instruction file) are already created and ready to use.
