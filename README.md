# 31 Day Challenge: AI

Code for my 31-day AI agent challenge on [YouTube](https://youtube.com/@TylerReedAI), recorded in March 2024. Each `day_*` folder is a standalone project, mostly built on AutoGen 0.2 (`pyautogen`), with some LangChain, LM Studio, Ollama and Hugging Face days.

Join my [Discord](https://discord.gg/Db6e8KkHww) community for any questions.

> **Legacy code (2024).** This repo matches the videos and is not updated. OpenAI shut down `gpt-3.5-turbo`, `gpt-4` and `gpt-4-vision-preview`, which most OpenAI days use, so those days fail with `model_not_found` until you change the model name. See [Models used in this repo were retired](#models-used-in-this-repo-were-retired).

## Setup

Each day pins its own dependencies, so install per folder:

```bash
cd day_02_logging
pip install -r requirements.txt
python main.py
```

Use Python 3.11 or 3.12. The pinned `pyautogen` 0.2 releases require Python below 3.13, and pins such as `numpy==1.26.4` and `torch==2.2.1` publish wheels only up to 3.12.

Days that pin `chromadb==0.4.24` need Python 3.11, because its `chroma-hnswlib==0.7.3` dependency has no Python 3.12 wheel. On 3.12, pip tries to compile it and needs a C++ compiler. Those days are 15, 16, 18, 19, 20, 23, 24, 25 and 30.

`day_17` has no code. It only links the AutoGen video it reacts to.

Days that call OpenAI read the key from an `OAI_CONFIG_LIST.json` (or `.env`) in that folder. Replace the placeholder `api_key` with your own key; never commit a real one.

## Models used in this repo were retired

These models have been shut down. The substitutes are the ones listed on the [OpenAI deprecations page](https://developers.openai.com/api/docs/deprecations) and the [Anthropic deprecations page](https://docs.anthropic.com/en/docs/about-claude/model-deprecations):

| Model in this repo | Shut down | Substitute |
| --- | --- | --- |
| `gpt-3.5-turbo` | 2026-10-23 | `gpt-5.6-terra` |
| `gpt-4`, `gpt-4-1106-preview` | 2026-10-23 | `gpt-5.6-sol` |
| `gpt-4-vision-preview` | 2024-12-06 | a current vision model, e.g. `gpt-5.6-terra` |
| `claude-3-sonnet-20240229` (day 28) | 2025-07-21 | `claude-sonnet-5-5` |

`gpt-5.4-mini` is a cheaper option for these small demos ($0.75 / $4.50 per 1M input/output tokens, against $2 / $12 for `gpt-5.6-terra` and $4 / $20 for `gpt-5.6-sol`).

To run an affected day:

1. Change the model name everywhere that day sets it: `"model"` in `OAI_CONFIG_LIST.json`, `MODEL=` in `.env`, and any `filter_dict`, `model=` or `os.environ["model"]` in its `.py` files (search the folder for `gpt-`).
2. Delete `"temperature"` and `"max_tokens"` from the `llm_config`. GPT-5 models only accept the default temperature, and use `max_completion_tokens` instead of `max_tokens`. For LangChain `ChatOpenAI(...)` calls (days 09 and 24), set `temperature=1` instead of deleting it: the pinned `langchain-openai==0.0.8` sends `temperature=0.7` whenever you leave it out.
3. Expect a cost-calculation warning from `pyautogen` 0.2: its price table predates these models. The chat still runs.

Days 19 and 20 also build LangChain's `OpenAI()` class with no model name. That class calls the legacy Completions endpoint and defaults to `gpt-3.5-turbo-instruct`, which OpenAI shut down on 2026-09-28. The suggested substitutes (`gpt-5.6-terra`, `gpt-5.4-mini`) do not support that endpoint, so changing a model name is not enough there (and `os.environ["model"]` in day 19 is never read). Replace the import and the call:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-5.4-mini", temperature=1)  # instead of OpenAI(...)
```

`RetrievalQA` (day 19) and `ConversationalRetrievalChain` (day 20) accept a chat model unchanged. Day 30 uses the same `OpenAI()` class but points it at a local LM Studio server through `BASE_URL`, so it is not affected.

Day 28 (`claude.py`) calls the Anthropic Messages API directly, so the GPT steps above do not cover it. Two changes are needed besides the model name:

1. Delete `temperature=0.0` from `client.messages.create(...)`. `claude-sonnet-5-5` returns a 400 error when a request sets `temperature`, `top_p` or `top_k` ([model page](https://platform.claude.com/docs/en/models/sonnet-5-5/overview)).
2. Print only the text blocks. Adaptive thinking is on by default on this model, so `message.content[0]` can be a `thinking` block with no text. Replace the last `print` with:

```python
print("".join(block.text for block in message.content if block.type == "text"))
```

Thinking tokens count toward `max_tokens`, so keep `max_tokens=4096` or raise it. `main.py` talks to Claude through a LiteLLM proxy at `0.0.0.0:4000`, so change the model in the proxy's config as well. The `zephyr` config in `claude.py` points at LM Studio on `localhost:1234` and only borrows the Claude name; it is not affected.

Days that reference a retired model: 01, 02, 03, 05, 08, 09, 10, 11, 13, 16, 18, 19, 20, 21, 22, 23, 24, 25, 28 and 29 (web search). Days 04, 06 and 27 run local models through LM Studio or Ollama and are not affected.

For current, maintained AutoGen code (AutoGen 0.7 API), see [tylerprogramming/ai](https://github.com/tylerprogramming/ai/tree/main/frameworks/autogen).
