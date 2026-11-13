"""
Core nutrition engine: orchestrates LLM calls + data lookups for all features.
"""
from watsonx_client import generate_text
from nutrition_data import get_food_info, get_swaps, get_goal_macros, filter_foods_by_allergens
from prompts import (
    meal_plan_prompt,
    food_analysis_prompt,
    food_swap_prompt,
    image_food_analysis_prompt,
    grocery_label_prompt,
    chat_prompt,
    why_food_better_prompt,
)


def generate_meal_plan(
    health_goal: str,
    dietary_preferences: list[str],
    allergies: list[str],
    medical_conditions: list[str],
    fitness_routine: str,
    cultural_background: str,
    days: int = 7,
) -> dict:
    """Generate a personalized meal plan using IBM Granite."""
    macros = get_goal_macros(health_goal)
    safe_foods = filter_foods_by_allergens(allergies)

    prompt = meal_plan_prompt(
        health_goal=health_goal,
        dietary_preferences=dietary_preferences,
        allergies=allergies,
        medical_conditions=medical_conditions,
        fitness_routine=fitness_routine,
        cultural_background=cultural_background,
        days=days,
    )

    llm_response = generate_text(prompt, max_tokens=1500)

    return {
        "meal_plan": llm_response,
        "macro_targets": macros,
        "safe_foods_count": len(safe_foods),
        "days": days,
        "personalization": {
            "health_goal": health_goal,
            "dietary_preferences": dietary_preferences,
            "allergies": allergies,
            "medical_conditions": medical_conditions,
            "fitness_routine": fitness_routine,
            "cultural_background": cultural_background,
        },
    }


def analyze_food(food_name: str, portion: str = "100g") -> dict:
    """Analyze nutritional value of a food item."""
    db_info = get_food_info(food_name)
    prompt = food_analysis_prompt(food_name, portion)
    llm_response = generate_text(prompt, max_tokens=800)

    return {
        "food": food_name,
        "portion": portion,
        "database_facts": db_info,
        "detailed_analysis": llm_response,
    }


def get_food_swaps(food_to_replace: str, reason: str, user_goal: str) -> dict:
    """Get smart food swap recommendations."""
    db_swaps = get_swaps(food_to_replace)
    prompt = food_swap_prompt(food_to_replace, reason, user_goal)
    llm_response = generate_text(prompt, max_tokens=800)

    return {
        "original_food": food_to_replace,
        "quick_swaps": db_swaps,
        "detailed_recommendations": llm_response,
        "user_goal": user_goal,
    }


def analyze_food_image(detected_items: list[str]) -> dict:
    """Analyze food items detected from an image."""
    prompt = image_food_analysis_prompt(detected_items)
    llm_response = generate_text(prompt, max_tokens=800)

    db_facts = {item: get_food_info(item) for item in detected_items if get_food_info(item)}

    return {
        "detected_items": detected_items,
        "database_facts": db_facts,
        "analysis": llm_response,
    }


def analyze_grocery_label(label_text: str) -> dict:
    """Analyze a grocery product's nutrition label."""
    prompt = grocery_label_prompt(label_text)
    llm_response = generate_text(prompt, max_tokens=800)

    return {
        "label_text": label_text,
        "analysis": llm_response,
    }


def chat_with_nutritionist(user_message: str, conversation_history: list[dict]) -> dict:
    """Interactive chat with the AI nutritionist."""
    prompt = chat_prompt(user_message, conversation_history)
    llm_response = generate_text(prompt, max_tokens=600)

    return {
        "response": llm_response,
        "user_message": user_message,
    }


def compare_foods(food_a: str, food_b: str, context: str = "") -> dict:
    """Compare two foods and explain which is better and why."""
    db_a = get_food_info(food_a)
    db_b = get_food_info(food_b)
    prompt = why_food_better_prompt(food_a, food_b, context)
    llm_response = generate_text(prompt, max_tokens=800)

    return {
        "food_a": {"name": food_a, "facts": db_a},
        "food_b": {"name": food_b, "facts": db_b},
        "comparison": llm_response,
    }
