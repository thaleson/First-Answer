"""Prompt helpers for the Groq extraction request."""

from typing import TypedDict


class MessagePayload(TypedDict):
    """Represent a chat message payload expected by the Groq API."""

    role: str
    content: str


SYSTEM_PROMPT = """You are a brand extraction API.
Extract whether the monitored brand appears in the text and list other brands mentioned.
Return only valid JSON.
Do not return markdown.
Do not return explanations.
Do not include keys other than:
{
  "monitored_brand_found": true,
  "other_brands": ["Brand A", "Brand B"]
}
Rules:
- monitored_brand_found must be a boolean.
- other_brands must always be an array of strings.
- Never include the monitored brand inside other_brands.
- Remove duplicates from other_brands.
- If no other brands are found, return an empty array.
"""


def build_extraction_messages(text: str, monitored_brand: str) -> list[MessagePayload]:
    """Build the chat message sequence sent to the extraction model.

    Args:
        text (str): Source text that should be analyzed.
        monitored_brand (str): Brand that must be checked explicitly.

    Returns:
        list[MessagePayload]: Ordered chat messages with system instructions and user content.
    """

    user_prompt = f"""Analyze the text below.

Monitored brand:
{monitored_brand}

Text:
{text}
"""
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]
