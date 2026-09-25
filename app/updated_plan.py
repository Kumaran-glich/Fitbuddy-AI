import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def update_workout_plan(
    original_plan,
    feedback,
    age,
    goal,
    intensity
):

    if age < 18:
        safety_instruction = """
        The user is under 18.

        Keep all advice age-appropriate and health-focused.

        Do not provide calorie restriction,
        weight-loss dieting, extreme exercise,
        supplement recommendations,
        or appearance-focused advice.

        Focus on general fitness, strength,
        mobility, recovery, hydration,
        sleep, and balanced meals.
        """
    else:
        safety_instruction = """
        Keep the workout practical,
        balanced, and health-focused.
        """

    prompt = f"""
    You are FitBuddy, an AI fitness planning assistant.

    USER DETAILS

    Age: {age}
    Fitness Goal: {goal}
    Workout Intensity: {intensity}

    {safety_instruction}

    ORIGINAL WORKOUT PLAN:

    {original_plan}

    USER FEEDBACK:

    {feedback}

    Update the complete 7-day workout plan
    based on the user's feedback.

    Also generate one short nutrition
    or recovery tip.

    Use clean plain text only.

    Do not use Markdown symbols such as:
    #, ##, ###, **, *, or ---

    Use this EXACT structure:

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

    Give one practical nutrition or recovery tip
    in about 2 to 4 sentences.

    NUTRITION_TIP_END
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    text = response.text

    try:
        updated_workout = (
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
        updated_workout = text

        nutrition_tip = (
            "Nutrition tip could not be separated "
            "from the generated response."
        )

    return updated_workout, nutrition_tip