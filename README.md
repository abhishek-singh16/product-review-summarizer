# Product Review Summarizer - LangChain Single Agent Project

A beginner-friendly project that teaches you how to build a **single agent** using **LangChain + OpenAI**. The agent takes a batch of customer reviews and produces a structured sentiment analysis along with a clear pros-and-cons summary.

## What You'll Learn

- How LangChain works (LLMs, prompts, tools, agents)
- How to create tools using the `@tool` decorator
- How an agent decides which tools to call and in what order
- How `PromptTemplate` shapes LLM output
- How the agent's tool-calling loop works (think -> act -> observe -> repeat)

## How It Works

```
User's batch of customer reviews (separated by '|')
       |
       v
  [Agent thinks: "I need to analyze sentiment first"]
       |
       v
  [Tool: analyze_review_sentiment] --> overall sentiment, positive/negative split, recurring themes
       |
       v
  [Agent thinks: "Now I should summarize the pros and cons"]
       |
       v
  [Tool: summarize_pros_and_cons] --> structured Pros / Cons list + actionable takeaway
       |
       v
  Final summary returned to user
```

## Prerequisites

- Python 3.10 or higher
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/abhishek-singh16/product-review-summarizer.git
cd product-review-summarizer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy the example env file and add your real key:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your actual OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-key-here
```

## Run

```bash
python product_review_summarizer.py
```

You'll see an interactive prompt:

```
============================================================
  PRODUCT REVIEW SUMMARIZER AGENT
  Powered by LangChain + OpenAI
============================================================

Describe the product reviews you want to analyze, and the agent will
create a summary for you.

Type 'quit' to exit.

Your product reviews (separate multiple reviews with '|'):
```

Paste your reviews separated by `|` and the agent will analyze sentiment and generate a structured pros-and-cons summary. You'll also see detailed logs showing the agent's reasoning and tool calls.

## Example

**Input:**
```
This hand wash is amazing! The scent is so refreshing.|I didn't like the texture, it felt too thick.|Great value for the price. Will buy again.|The packaging is beautiful and eco-friendly.|Not moisturizing enough for my dry skin.
```

**Output:**
```
Pros:
1. Refreshing and pleasant scent
2. Great value for the price
3. Beautiful, eco-friendly packaging

Cons:
1. Texture is too thick for some users
2. Not moisturizing enough for dry skin

Takeaway: Consider offering a lighter-formula variant to address texture and moisturization concerns while retaining the popular scent and eco-friendly packaging.
```

## Project Structure

```
.
├── product_review_summarizer.py   # Main agent code (fully commented)
├── requirements.txt               # Python dependencies
├── .env.example                   # API key template
├── .gitignore                     # Keeps secrets and venv out of git
└── README.md                      # This file
```

## Tech Stack

- [LangChain](https://python.langchain.com/) - Framework for building LLM applications
- [OpenAI GPT-4.1-mini](https://platform.openai.com/) - The LLM powering the agent
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management
