from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

from app.gemini_generator import generate_fitness_plan
from app.updated_plan import update_workout_plan

from app.database import (
    save_user,
    save_plan,
    get_all_users,
    get_all_plans,
    get_original_plan,
    get_user,
    update_plan
)


app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ----------------------------------------
# HOME PAGE
# ----------------------------------------

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# ----------------------------------------
# GENERATE WORKOUT PLAN
# ----------------------------------------

@app.post("/generate-workout")
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    generation_success = True

    # One Gemini request:
    # workout plan + nutrition tip
    try:

        workout_plan, nutrition_tip = generate_fitness_plan(
            age,
            weight,
            goal,
            intensity
        )

    except Exception as e:

        print("Gemini Error:", e)

        generation_success = False

        workout_plan = (
            "FitBuddy AI is temporarily unavailable. "
            "Please try generating your plan again later."
        )

        nutrition_tip = (
            "Nutrition advice is temporarily unavailable."
        )


    # Save user details
    save_user(
        user_id,
        username,
        age,
        weight,
        goal,
        intensity
    )


    # Save plan only if Gemini successfully generated it
    if generation_success:

        save_plan(
            user_id,
            workout_plan,
            nutrition_tip
        )


    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip,
            "updated": False
        }
    )


# ----------------------------------------
# VIEW ALL USERS
# ----------------------------------------

@app.get("/view-all-users")
async def view_all_users(request: Request):

    users = get_all_users()

    plans = get_all_plans()

    plan_dict = {
        plan.user_id: plan
        for plan in plans
    }

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users,
            "plan_dict": plan_dict
        }
    )


# ----------------------------------------
# SUBMIT FEEDBACK / UPDATE PLAN
# ----------------------------------------

@app.post("/submit-feedback")
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):

    # Get user details
    user = get_user(user_id)

    # Get original workout plan
    original_plan = get_original_plan(user_id)


    # If user or plan does not exist
    if user is None or original_plan is None:

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "username": "User not found",
                "user_id": user_id,
                "age": "-",
                "weight": "-",
                "goal": "-",
                "intensity": "-",
                "workout_plan": (
                    "No original workout plan "
                    "was found for this User ID."
                ),
                "nutrition_tip": "",
                "updated": False
            }
        )


    update_success = True


    # One Gemini request:
    # updated workout + updated nutrition tip
    try:

        updated_workout, nutrition_tip = update_workout_plan(
            original_plan,
            feedback,
            user.age,
            user.goal,
            user.intensity
        )

    except Exception as e:

        print("Plan Update Error:", e)

        update_success = False

        updated_workout = (
            "FitBuddy could not update the workout plan "
            "right now. Please try again later."
        )

        nutrition_tip = (
            "Nutrition advice is temporarily unavailable."
        )


    # Save update only if Gemini succeeded
    if update_success:

        update_plan(
            user_id,
            updated_workout,
            nutrition_tip
        )


    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "username": user.username,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": updated_workout,
            "nutrition_tip": nutrition_tip,
            "updated": True
        }
    )