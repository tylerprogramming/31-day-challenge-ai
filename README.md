# 31 Day Challenge: AI

Code for my 31-day AI agent challenge on [YouTube](https://youtube.com/@TylerReedAI), recorded in March 2024. Each `day_*` folder is a standalone project, mostly built on AutoGen 0.2 (`pyautogen`), with some LangChain, LM Studio, Ollama and Hugging Face days.

Join my [Discord](https://discord.gg/Db6e8KkHww) community for any questions.

## Setup

Each day pins its own dependencies, so install per folder:

```bash
cd day_02_logging
pip install -r requirements.txt
python main.py
```

Use Python 3.11 or 3.12. The pinned `pyautogen` 0.2 releases require Python below 3.13, and pins such as `numpy==1.26.4` and `torch==2.2.1` publish wheels only up to 3.12.

Days that call OpenAI read the key from an `OAI_CONFIG_LIST.json` (or `.env`) in that folder. Replace the placeholder `api_key` with your own key; never commit a real one.
