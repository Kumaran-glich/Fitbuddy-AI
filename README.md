# 🏋️ FitBuddy AI

FitBuddy is an AI-powered fitness plan generator built using Python, FastAPI, Google Gemini AI, SQLite, SQLAlchemy, HTML, CSS, and Jinja2.

The application creates personalized 7-day workout plans and nutrition/recovery tips based on the user's age, weight, fitness goal, and preferred workout intensity.

Users can also provide feedback to modify their existing workout plan.

---

## ✨ Features

- 🤖 AI-generated 7-day workout plans
- 🥗 AI-generated nutrition and recovery tips
- 👤 Multiple user support
- 💾 SQLite database storage
- 🔄 Update workout plans using user feedback
- 📋 Stores original and updated workout plans
- 🥗 Stores original and updated nutrition tips
- 👥 View All Users dashboard
- 🎯 Fitness goal selection
- 💪 Workout intensity selection
- 🌙 Modern dark purple user interface
- 🔁 Backup Gemini model support

---

## 🧠 How FitBuddy Works

The user enters:

- Name
- User ID
- Age
- Weight
- Fitness Goal
- Workout Intensity

FitBuddy sends this information to Google Gemini AI.

Gemini generates:

1. A personalized 7-day workout plan
2. A nutrition or recovery tip

The results are displayed to the user and stored in the SQLite database.

### Workflow

```text
User
 ↓
FitBuddy Form
 ↓
FastAPI Backend
 ↓
Google Gemini AI
 ↓
Workout Plan + Nutrition Tip
 ↓
SQLite Database
 ↓
Result Page