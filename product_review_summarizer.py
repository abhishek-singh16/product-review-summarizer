"""
===========================================================================
 Product Review Summarizer Agent
===========================================================================

Use Case: A user pastes a batch of customer reviews. The agent analyses the overall sentiment and then produces a clean pros-and-cons summary.

Tool 1 — analyze_review_sentiment
Input: a collection of customer reviews (mixed positive and negative)
Task: Determine the overall sentiment, the rough positive/negative split, and the most frequently mentioned themes
Output: A sentiment summary with overall rating impression and the top recurring topics

Tool 2 — summarize_pros_and_cons
Input: the reviews + the sentiment analysis from Tool 1
Task: Distil the reviews into a balanced list of the most common pros and cons, plus one actionable takeaway for the seller
Output: A clean Pros / Cons summary with a short recommendation

System Prompt: The agent acts as a product analyst who turns scattered customer reviews into a clear list of pros and cons. Also provide a balanced summary for shoppers and sellers.

===========================================================================
"""

import logging
import sys
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ProductReviewerAgent")

logger.info("Starting Product Reviewer Agent...")

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key.startswith("sk-your"):
    logger.error("OPENAI_API_KEY not set! Copy .env.example to .env and add your key.")
    sys.exit(1)

logger.info("API key loaded successfully")
logger.info("All LangChain components imported")
logger.info("Initializing the LLM (OpenAI GPT)...")

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7,
    verbose=True,
)

logger.info("LLM initialized: model=gpt-4.1-mini, temperature=0.7")
logger.info("Defining agent tools...")


@tool
def analyze_review_sentiment(reviews: str) -> str:
    """
    Analyzes the sentiment of a batch of customer reviews.
    Input should be a list of reviews (strings separated by '|')
    Returns a sentiment summary with overall rating impression and top recurring topics.
    """
    logger.info(f"[Tool: analyze_review_sentiment] Received reviews: {reviews}")

    sentiment_prompt = PromptTemplate(
        input_variables=["reviews"],
        template="""You are a product review analyst.
        Given the following customer reviews (a string with multiple reviews separated by '|'), analyze the overall sentiment, the rough positive/negative split, and identify key themes.

        Reviews: {reviews}

        Your analysis should include:
        - Overall sentiment (positive/negative/neutral)
        - Rough positive/negative split (e.g., 70% positive, 30% negative)
        - Most frequently mentioned themes (e.g., "battery life", "screen quality")

        Return only the analysis output, nothing else.
        """,
    )

    formatted_prompt = sentiment_prompt.format(reviews=reviews)

    logger.info("[Tool: analyze_review_sentiment] Sending prompt to LLM...")

    response = llm.invoke(formatted_prompt)

    logger.info("[Tool: analyze_review_sentiment] Sentiment analysis completed!")
    logger.info(f"[Tool: analyze_review_sentiment] Analysis output: {response.content}")

    return response.content

@tool
def summarize_pros_and_cons(reviews: str, sentiment: str) -> str:
    """
    Takes a batch of customer reviews and the sentiment analysis result,
    and distills them into a balanced list of the most common pros and cons.
    Also provides one actionable takeaway for the seller.
    """
    logger.info("[Tool: summarize_pros_and_cons] Summarizing pros and cons...")

    summarize_prompt = PromptTemplate(
        input_variables=["reviews", "sentiment"],
        template="""You are a product review summarizer.
        Given the following customer reviews and the sentiment analysis result,
        distill them into a balanced list of the most common pros and cons.

        Reviews: {reviews}
        Sentiment Analysis: {sentiment}

        Your output should include:
        - A list of pros (positive aspects)
        - A list of cons (negative aspects)
        - One actionable takeaway for the seller or shopper

        Return your output in a clear, structured format, point wise manner with section wise. For example: 
        <paragraph 1>Pros: 1. ..., 2. ... 
        <paragraph 2>Cons: 1. ..., 2. ... 
        <paragraph 3>Takeaway: ...
        """,
    )

    formatted_prompt = summarize_prompt.format(reviews=reviews, sentiment=sentiment)

    logger.info("[Tool: summarize_pros_and_cons] Sending prompt to LLM...")

    response = llm.invoke(formatted_prompt)

    logger.info("[Tool: summarize_pros_and_cons] Summary completed!")
    return response.content

tools = [analyze_review_sentiment, summarize_pros_and_cons]
logger.info(f"Tools registered: {[t.name for t in tools]}")
logger.info("Creating the agent...")

SYSTEM_PROMPT = """You are a Product Review Summarizer assistant. Your job is to help users
summarize customer reviews into clear insights.

When the user provides a batch of reviews, follow these steps:
1. First, use the analyze_review_sentiment tool to assess the overall sentiment.
2. Then, use the summarize_pros_and_cons tool to distill the reviews into key insights.
3. Return the final output to the user.

Always use both tools in order: analyze_review_sentiment first, then summarize_pros_and_cons."""

agent_graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    debug=True,
)

logger.info("Agent created and ready to run!")


def run_product_review_summarizer(reviews: str) -> str:
    """
    Main function to run the product review summarizer agent.

    Args:
        reviews: A list of customer reviews to analyze.

    Returns:
        A summary of the product reviews.
    """
    logger.info("=" * 60)
    logger.info(f"USER'S REVIEWS: {reviews}")
    logger.info("=" * 60)
    logger.info("Agent is now thinking... watch the tool-calling loop below!")
    logger.info("-" * 60)

    result = agent_graph.invoke(
        {"messages": [HumanMessage(content=reviews)]}
    )

    final_summary = result["messages"][-1].content

    logger.info("-" * 60)
    logger.info("Agent finished! Here's your product review summary:")
    logger.info("=" * 60)

    return final_summary


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PRODUCT REVIEW SUMMARIZER AGENT")
    print("  Powered by LangChain + OpenAI")
    print("=" * 60)
    print("\nDescribe the product reviews you want to analyze, and the agent will")
    print("create a summary for you.\n")
    print("Type 'quit' to exit.\n")

    while True:
        reviews = input("Your product reviews (separate multiple reviews with '|'): ").strip()

        if not reviews:
            print("Please enter product reviews.\n")
            continue

        if reviews.lower() in ("quit", "exit", "q"):
            print("\nGoodbye!")
            break

        try:
            final_summary = run_product_review_summarizer(reviews)

            print("\n" + "=" * 60)
            print("YOUR PRODUCT REVIEW SUMMARY:")
            print("=" * 60)
            print(final_summary)
            print("=" * 60 + "\n")

        except Exception as e:
            logger.error(f"Something went wrong: {e}")
            print(f"\nError: {e}")
            print("Please check your API key and try again.\n")

# example_reviews = "This hand wash is amazing! The scent is so refreshing.|I didn't like the texture, it felt too thick.|Great value for the price. Will buy again.|The packaging is beautiful and eco-friendly.|Not moisturizing enough for my dry skin.|Love the natural ingredients used in this product.|The pump dispenser is a bit flimsy.|Perfect for everyday use, my family loves it.|I wish it had a stronger fragrance.|Overall, a solid hand wash that gets the job done."