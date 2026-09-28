<<<<<<< HEAD
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_answer(question, context):

    prompt = f"""
Answer the user's question using ONLY the provided context.

If the answer is not available in the context,
say that the information was not found
in the uploaded documents.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content
=======
import os
import requests


def build_context(results):

    context_parts = []


    for result in results:

        context_parts.append(
            "DOCUMENT: "
            + result["name"]
            + "\n"
            + result["text"]
        )


    return "\n\n".join(
        context_parts
    )


def generate_answer(
    question,
    results
):

    if not results:

        return (
            "No relevant documents were found."
        )


    context = build_context(
        results
    )


    prompt = f"""
You are an intelligent document assistant.

Answer the user's question using ONLY
the information contained in the documents.

Do not invent information.

If the answer is not available in the
documents, say:

"The answer is not available in
the uploaded documents."

USER QUESTION:

{question}


DOCUMENT CONTEXT:

{context}


ANSWER:
"""


    api_key = os.getenv(
        "OPENAI_API_KEY"
    )


    if not api_key:

        return (
            "Relevant documents were found, "
            "but the LLM API key is not configured."
        )


    try:

        response = requests.post(

            "https://api.openai.com/v1/responses",

            headers={

                "Authorization":
                    f"Bearer {api_key}",

                "Content-Type":
                    "application/json"

            },

            json={

                "model":
                    "gpt-4.1-mini",

                "input":
                    prompt

            },

            timeout=60

        )


        response.raise_for_status()


        data = response.json()


        return data["output"][0][
            "content"
        ][0]["text"]


    except requests.RequestException as error:

        return (
            f"LLM request failed: {error}"
        )


    except (KeyError, IndexError):

        return (
            "Unable to read the LLM response."
        )
>>>>>>> 9e1028108555e57ec26c8f069a9f82063b18e4f7
