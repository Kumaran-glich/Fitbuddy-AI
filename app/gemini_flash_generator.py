import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def generate_nutrition_tip(age, goal):

    if age < 18:
        prompt = f"""
        You are FitBuddy.

        The user is under 18.
        Their fitness goal is: {goal}.

        Give one short, practical nutrition or recovery tip.

        Do not recommend:
        - calorie restriction
        - dieting for weight loss
        - supplements
        - extreme eating plans
        - body appearance goals

        Focus on healthy meals, hydration, sleep,
        recovery, and balanced nutrition.

        Keep the answer to about 2-4 sentences.
        """
    else:
        prompt = f"""
        You are FitBuddy.

        Fitness goal: {goal}

        Give one short and practical nutrition
        or recovery tip that supports this goal.

        Keep the advice general and health-focused.
        Do not diagnose medical conditions.

        Keep the answer to about 2-4 sentences.

        Do not use Markdown symbols.
        Return clean plain text only.
        """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text