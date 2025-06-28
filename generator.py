import random
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

TEMPLATES = {
    "default": """
[HOOK]
{hook}

[INTRODUCTION]
{introduction}

[BODY]
{body}

[CALL_TO_ACTION]
{cta}
""",
}

def generate_hook(topic):
    return f"Have you ever wondered about {topic}? Today, you'll find out!"

def generate_cta():
    return "Subscribe for more amazing videos like this one!"

def generate_body(topic, length="short"):
    # If OpenAI key is configured, use GPT
    if OPENAI_API_KEY != "your_openai_api_key_here":
        prompt = (
            f"Write a {length} educational script about {topic}. "
            "Make it engaging and clear."
        )
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
        )
        return response.choices[0].text.strip()
    else:
        return f"Here are some facts about {topic}. It's fascinating!"

def generate_script(topic, length="short"):
    hook = generate_hook(topic)
    intro = f"In this video, let's explore {topic} together."
    body = generate_body(topic, length)
    cta = generate_cta()

    return TEMPLATES["default"].format(
        hook=hook,
        introduction=intro,
        body=body,
        cta=cta,
    )

