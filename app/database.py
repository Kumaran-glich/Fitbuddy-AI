from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Text,
    ForeignKey
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)


# ----------------------------------------
# DATABASE SETUP
# ----------------------------------------

DATABASE_URL = "sqlite:///./fitbuddy.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


# ----------------------------------------
# USER TABLE
# ----------------------------------------

class User(Base):

    __tablename__ = "users"

    user_id = Column(
        String,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    weight = Column(
        Float,
        nullable=False
    )

    goal = Column(
        String,
        nullable=False
    )

    intensity = Column(
        String,
        nullable=False
    )


# ----------------------------------------
# WORKOUT PLAN TABLE
# ----------------------------------------

class WorkoutPlan(Base):

    __tablename__ = "workout_plans"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String,
        ForeignKey("users.user_id"),
        unique=True,
        nullable=False
    )

    # Original AI workout plan
    original_plan = Column(
        Text,
        nullable=False
    )

    # Original nutrition/recovery tip
    nutrition_tip = Column(
        Text,
        nullable=True
    )

    # Updated workout after feedback
    updated_plan = Column(
        Text,
        nullable=True
    )

    # Updated nutrition/recovery tip
    updated_nutrition_tip = Column(
        Text,
        nullable=True
    )


# Create tables
Base.metadata.create_all(
    bind=engine
)


# ----------------------------------------
# SAVE USER
# ----------------------------------------

def save_user(
    user_id,
    username,
    age,
    weight,
    goal,
    intensity
):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.user_id == user_id
        ).first()


        # Existing user
        if user:

            user.username = username
            user.age = age
            user.weight = weight
            user.goal = goal
            user.intensity = intensity


        # New user
        else:

            user = User(
                user_id=user_id,
                username=username,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity
            )

            db.add(user)


        db.commit()


    finally:

        db.close()


# ----------------------------------------
# SAVE ORIGINAL PLAN
# ----------------------------------------

def save_plan(
    user_id,
    workout_plan,
    nutrition_tip
):

    db = SessionLocal()

    try:

        plan = db.query(WorkoutPlan).filter(
            WorkoutPlan.user_id == user_id
        ).first()


        # Existing plan
        if plan:

            plan.original_plan = workout_plan

            plan.nutrition_tip = nutrition_tip

            # Reset previous feedback update
            plan.updated_plan = None

            plan.updated_nutrition_tip = None


        # New plan
        else:

            plan = WorkoutPlan(
                user_id=user_id,
                original_plan=workout_plan,
                nutrition_tip=nutrition_tip
            )

            db.add(plan)


        db.commit()


    finally:

        db.close()


# ----------------------------------------
# UPDATE WORKOUT PLAN
# ----------------------------------------

def update_plan(
    user_id,
    updated_plan,
    updated_nutrition_tip
):

    db = SessionLocal()

    try:

        plan = db.query(WorkoutPlan).filter(
            WorkoutPlan.user_id == user_id
        ).first()


        if plan:

            plan.updated_plan = updated_plan

            plan.updated_nutrition_tip = (
                updated_nutrition_tip
            )

            db.commit()


    finally:

        db.close()


# ----------------------------------------
# GET ORIGINAL PLAN
# ----------------------------------------

def get_original_plan(user_id):

    db = SessionLocal()

    try:

        plan = db.query(WorkoutPlan).filter(
            WorkoutPlan.user_id == user_id
        ).first()


        if plan:

            return plan.original_plan


        return None


    finally:

        db.close()


# ----------------------------------------
# GET USER
# ----------------------------------------

def get_user(user_id):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.user_id == user_id
        ).first()


        if user is None:

            return None


        # Copy data so it can safely be used
        # after the database session closes
        user_data = User(
            user_id=user.user_id,
            username=user.username,
            age=user.age,
            weight=user.weight,
            goal=user.goal,
            intensity=user.intensity
        )

        return user_data


    finally:

        db.close()


# ----------------------------------------
# GET ALL USERS
# ----------------------------------------

def get_all_users():

    db = SessionLocal()

    try:

        users = db.query(User).all()


        result = []

        for user in users:

            result.append(
                User(
                    user_id=user.user_id,
                    username=user.username,
                    age=user.age,
                    weight=user.weight,
                    goal=user.goal,
                    intensity=user.intensity
                )
            )


        return result


    finally:

        db.close()


# ----------------------------------------
# GET ALL PLANS
# ----------------------------------------

def get_all_plans():

    db = SessionLocal()

    try:

        plans = db.query(WorkoutPlan).all()


        result = []

        for plan in plans:

            result.append(
                WorkoutPlan(
                    id=plan.id,
                    user_id=plan.user_id,
                    original_plan=plan.original_plan,
                    nutrition_tip=plan.nutrition_tip,
                    updated_plan=plan.updated_plan,
                    updated_nutrition_tip=(
                        plan.updated_nutrition_tip
                    )
                )
            )


        return result


    finally:

        db.close()