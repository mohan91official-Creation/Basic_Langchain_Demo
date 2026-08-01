# AI Brainstorming Studio

AI Brainstorming Studio is a small LangChain application for developing YouTube ideas, titles, hooks, and content strategies. It includes both a Streamlit chat interface and a command-line interface, with streamed responses and in-session conversational memory.

## Features

- Real-time streamed responses from OpenAI
- Conversational memory for the current session
- Streamlit chat interface with a custom dark theme
- Command-line interface for lightweight use
- Optional LangSmith tracing configured through environment variables

## Project structure

```text
Basic_Langchain_Demo/
|-- .streamlit/
|   `-- config.toml      # Streamlit theme
|-- .env.example        # Safe environment-variable template
|-- .gitignore          # Local and sensitive files excluded from Git
|-- app.py              # Command-line application
|-- requirements.txt    # Python dependencies
|-- SECURITY.md         # Security and secret-handling guidance
|-- ui.py               # Streamlit application
`-- README.md            # Project documentation
```

## Requirements

- Python 3.10 or later
- An OpenAI API key
- A LangSmith API key only if tracing is enabled

## Setup

1. Clone the repository and enter the project directory.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Copy the safe environment template:

   ```powershell
   Copy-Item .env.example .env
   ```

5. Open `.env` and add your own credentials. Never commit this file.

## Run the application

Start the Streamlit interface:

```powershell
streamlit run ui.py
```

Or run the command-line interface:

```powershell
python app.py
```

Enter `quit` to close the command-line application.

## Environment variables

| Variable | Required | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | Yes | Authenticates requests to OpenAI. |
| `LANGSMITH_TRACING` | No | Set to `true` to enable tracing. |
| `LANGSMITH_ENDPOINT` | No | Overrides the LangSmith API endpoint. |
| `LANGSMITH_API_KEY` | When tracing | Authenticates LangSmith tracing. |
| `LANGSMITH_PROJECT` | No | Names the LangSmith tracing project. |

## Security

Secrets belong only in `.env` or another ignored secret store. The repository includes placeholders, never real keys. See [SECURITY.md](SECURITY.md) before sharing logs, screenshots, or bug reports.

## Notes

- Conversation history is held in memory and is cleared when the process or Streamlit session ends.
- The default model is `gpt-4o-mini`; update the `ChatOpenAI` initialization in `app.py` and `ui.py` if you want to use another compatible model.
