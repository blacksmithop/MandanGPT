# MandanGPT

[![My Skills](https://skillicons.dev/icons?i=py)](https://skillicons.dev)

Customizable AI powered discord bot with a focus on observability

---

## Usage

Clone the repo

```bash
git clone https://github.com/blacksmithop/MandanGPT
```

Install requirements

```bash
python -m pip install -r requirements.txt
```

Run the bot

```bash
python bot.py
```

## TODO

- Let logged in users enter urls, usernames & upload files to Knowledge Base
  - Identify uploader by discord id
  - Setup headless browser with API + (validate URLs before scraping)
  - Implement connectors for most popular providers
    - Indexing methods based on document/source type
- Langgraph CRAG (corrective RAG)
- Deploy Milvus ✅
- Deploy LangFuse ✅
- MongoDB/Redis - Server stats (frequent update task)
  - Website stats
- Export Help Command JSON - Return via API - Render / Manually add ✅
- Dynamic website content ✅

## Bugs

- When passsing parameters in summary command to LLM, the max-tokens parameter is not followed ✅
- Langfuse does not show usage traces ✅
- Handle missing permission errors (eg: Cannot DM)
- Better Discord Status