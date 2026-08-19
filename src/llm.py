import os
import requests
from dotenv import load_dotenv

load_dotenv()


def build_context(results):

    context_parts = []

    for result in results:

        context_parts.append(
            "DOCUMENT: "
            + result["name"]
            + "\n"
            + result["text"]
        )

    return "\n\n".join(context_parts)


def generate_answer(question, results):

    if not results:
        return "No relevant documents were found."

    context = build_context(results)

    prompt = f"""
You are an intelligent document assistant.

Answer the user's question using ONLY the information
contained in the documents.

Do not invent information.

If the answer is not available in the documents, say:

"The answer is not available in the uploaded documents."

USER QUESTION:
{question}

DOCUMENT CONTEXT:
{context}

ANSWER:
"""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "ERROR: OPENAI_API_KEY was not found."

    try:

        response = requests.post(
            "https://api.openai.com/v1/responses",

            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },

            json={
                "model": "gpt-4.1-mini",
                "input": prompt
            },

            timeout=60
        )

        # Show the actual OpenAI error
        if response.status_code != 200:

            return (
                f"ERROR: OpenAI API returned "
                f"{response.status_code}\n\n"
                f"{response.text}"
            )

        data = response.json()

        # Get generated answer
        if "output_text" in data:
            return data["output_text"]

        # Fallback for response structure
        return data["output"][0]["content"][0]["text"]

    except requests.exceptions.ConnectionError:

        return (
            "ERROR: Cannot connect to OpenAI API. "
            "Check your internet connection or firewall."
        )

    except requests.exceptions.Timeout:

        return (
            "ERROR: OpenAI API request timed out."
        )

    except requests.RequestException as error:

        return f"ERROR: Request failed: {error}"

    except Exception as error:

        return f"ERROR: {error}"