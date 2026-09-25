import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY was not found in .env")

client = genai.Client(api_key=api_key)


# Try Gemini models one by one
def ask_gemini(prompt):

    models = [
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.5-flash"
    ]

    last_error = None

    for model in models:

        try:
            print(f"Trying model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            print(f"Success with: {model}")

            return response.text

        except Exception as e:

            print(f"{model} failed: {e}")

            last_error = e

    raise last_error


def generate_fitness_plan(age, weight, goal, intensity):

    if age < 18:

        safety_instruction = """
        The user is under 18.

        Keep all advice age-appropriate and health-focused.

        Do not provide calorie restriction,
        weight-loss dieting,
        extreme exercise,
        supplement recommendations,
        or appearance-focused advice.

        Focus on general fitness, strength,
        mobility, recovery, hydration,
        sleep, and balanced meals.
        """

    else:

        safety_instruction = f"""
        The user's fitness goal is {goal}.

        Keep recommendations practical,
        balanced, and health-focused.
        """

    prompt = f"""
    You are FitBuddy, an AI fitness planning assistant.

    USER DETAILS

    Age: {age}
    Weight: {weight} kg
    Fitness Goal: {goal}
    Workout Intensity: {intensity}

    {safety_instruction}

    Generate TWO things:

    1. A personalized 7-day workout plan.
    2. One short nutrition or recovery tip.

    For each workout day include:

    Day and workout focus
    Warm-up
    Main Workout
    Sets and repetitions or duration
    Rest guidance
    Cool-down or recovery

    Include suitable rest days.

    Use clean plain text only.

    Do not use Markdown symbols such as:
    #, ##, ###, **, *, or ---

    Use this exact structure:

    WORKOUT_PLAN_START

    DAY 1 - Workout Focus

    Warm-up:
    ...

    Main Workout:
    ...

    Rest:
    ...

    Cool-down:
    ...

    Continue through DAY 7.

    WORKOUT_PLAN_END

    NUTRITION_TIP_START

    Give one short practical nutrition or recovery tip.

    NUTRITION_TIP_END
    """

    text = ask_gemini(prompt)

    try:

        workout_plan = (
            text.split("WORKOUT_PLAN_START", 1)[1]
            .split("WORKOUT_PLAN_END", 1)[0]
            .strip()
        )

        nutrition_tip = (
            text.split("NUTRITION_TIP_START", 1)[1]
            .split("NUTRITION_TIP_END", 1)[0]
            .strip()
        )

    except Exception:

        workout_plan = text

        nutrition_tip = (
            "Nutrition tip could not be separated "
            "from the generated response."
        )

    return workout_plan, nutrition_tip