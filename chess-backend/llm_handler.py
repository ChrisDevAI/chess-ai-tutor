import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import APIConnectionError, AuthenticationError, OpenAIError

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def query_openai(prompt: str, fen: str = None) -> str:
    try:
        full_prompt = prompt
        if fen:
            full_prompt = f"The current board position (FEN) is: {fen}\n{prompt}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}]
        )
        return response.choices[0].message.content.strip()

    except AuthenticationError:
        return "❌ OpenAI authentication failed. Check your API key."
    except APIConnectionError:
        return "❌ Failed to connect to OpenAI servers. Are you online?"
    except OpenAIError as e:
        return f"❌ OpenAI error: {e}"
    except Exception as e:
        return f"❌ Unexpected error: {e}"
