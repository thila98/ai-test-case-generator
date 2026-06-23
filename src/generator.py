import os
import anthropic
from dotenv import load_dotenv
from src.prompt_builder import build_prompt

load_dotenv()

def generate_test_cases(feature_description: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env file")

    client = anthropic.Anthropic(api_key=api_key)

    print("Connecting to Claude AI...")
    print("Generating test cases for your feature...")
    print("-" * 50)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": build_prompt(feature_description)
            }
        ]
    )

    return message.content[0].text


def run(feature_description: str) -> str:
    raw_output = generate_test_cases(feature_description)
    return raw_output


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.generator 'your feature description'")
        sys.exit(1)

    feature = sys.argv[1]
    result = run(feature)
    print(result)
