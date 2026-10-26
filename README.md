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
2. Delete `"temperature"` and `"max_tokens"` from the `llm_config` (and `temperature=` from LangChain `ChatOpenAI(...)` calls). GPT-5 models only accept the default temperature, and use `max_completion_tokens` instead of `max_tokens`.
3. Expect a cost-calculation warning from `pyautogen` 0.2: its price table predates these models. The chat still runs.

Days that reference a retired model: 01, 02, 03, 05, 08, 09, 10, 11, 13, 16, 18, 19, 20, 21, 22, 23, 24, 25, 28 and 29 (web search). Days 04, 06 and 27 run local models through LM Studio or Ollama and are not affected.

For current, maintained AutoGen code (AutoGen 0.7 API), see [tylerprogramming/ai](https://github.com/tylerprogramming/ai/tree/main/frameworks/autogen).
