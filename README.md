# Currency Conversion Agent (LangChain Tool Calling)

A small Python project that shows how an LLM can use **tools** to answer a real-world question with live data. The user asks to convert an amount between two currencies, the model decides which tools to call, and the program executes them and returns the final answer.

## Features

- **Two LangChain tools**
  - `get_conversion_rate` fetches the live exchange rate from the ExchangeRate-API.
  - `multiply` calculates the converted amount.
- **Injected argument (`InjectedToolArg`)**: the exchange rate is hidden from the model and added by the code, so the model cannot invent the number.
- **Manual tool-calling loop**: a `while` loop runs the requested tools, returns the results as `ToolMessage` objects, and calls the model again until it gives a final text answer.
- **Groq-hosted LLM** (`openai/gpt-oss-120b`) through `langchain-groq`.
- **Secrets in `.env`**: no API keys are stored in the code.

## How it works

1. The user question is sent to the model together with the tool descriptions (`bind_tools`).
2. The model replies with a tool request (for example `get_conversion_rate("USD", "PKR")`). It does not run the tool itself.
3. The program executes the tool and sends the result back as a `ToolMessage`.
4. The model requests the second tool (`multiply`). The program injects the real exchange rate and runs it.
5. The model receives the result and writes the final answer. The loop ends when a reply contains no tool requests.

## Project structure

```
currency-conversion-agent/
├── currency_conversion.py   # main script
├── requirements.txt         # dependencies
├── .env.example             # template for your API keys
├── .gitignore
└── README.md
```

## Setup

**Requirements:** Python 3.10 or newer, a free [Groq](https://console.groq.com) API key, and a free [ExchangeRate-API](https://www.exchangerate-api.com) API key.

```bash
# 1. Clone the repository
git clone https://github.com/FawadAhmad-bilal/currency-conversion-agent.git
cd currency-conversion-agent

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install the dependencies
pip install -r requirements.txt

# 4. Add your keys
copy .env.example .env         # Windows
# cp .env.example .env         # macOS / Linux
# then open .env and paste your own keys
```

## Usage

```bash
python currency_conversion.py
```

Example output (the rate changes over time):

```
The current conversion rate is 1 USD = 276.7262 PKR.
So, 10 USD x 276.7262 = 2,767.262 PKR.
```

To change the question, edit the `HumanMessage` text in the script.

## Configuration

| Setting | Where | Default |
|---|---|---|
| Model name | `ChatGroq(model=...)` in the script | `openai/gpt-oss-120b` |
| Temperature | `ChatGroq(temperature=...)` | `0` recommended for reliable tool calling |
| API keys | `.env` | `GROQ_API_KEY`, `EXCHANGE_API_KEY` |

Hosted models are sometimes retired by the provider. If you see a `model_not_found` (404) error, check the Groq documentation for the current model names and update the `model` value.

## Security

- Never commit your real `.env` file. It is listed in `.gitignore`.
- If a key is ever pushed or shared by mistake, revoke it in the provider dashboard and create a new one.
- Free API plans have request limits, so avoid running the script in a loop.

## Limitations and ideas for improvement

- Add error handling for failed API responses (for example, check `result == "success"` before reading the rate).
- Cache exchange rates to save API requests.
- Validate currency codes before calling the API.
- Turn the script into an interactive chat loop that keeps the conversation history.
- Add automated tests for the tools.

## Tech stack

Python, LangChain (`langchain-core`, `langchain-groq`), Groq API, ExchangeRate-API, `python-dotenv`, `requests`.

## Author

**Fawad Ahmad Bilal**, BS Artificial Intelligence student, University of Haripur.
GitHub: [FawadAhmad-bilal](https://github.com/FawadAhmad-bilal)
