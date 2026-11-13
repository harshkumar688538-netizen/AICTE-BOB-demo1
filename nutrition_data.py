"""
Nutritional data: food database, macros, allergen tags, and swap logic.
Used as a lightweight in-memory reference alongside LLM reasoning.
"""
from dataclasses import dataclass, field

FOOD_DB: dict[str, dict] = {
    "oatmeal": {
        "calories": 150, "protein": 5, "carbs": 27, "fat": 3, "fiber": 4,
        "vitamins": ["B1", "Iron", "Magnesium"],
        "allergens": ["gluten"], "category": "breakfast", "cuisine": "universal",
    },
    "brown rice": {
        "calories": 215, "protein": 5, "carbs": 45, "fat": 2, "fiber": 4,
        "vitamins": ["B1", "B3", "Magnesium"],
        "allergens": [], "category": "grain", "cuisine": "universal",
    },
    "quinoa": {
        "calories": 222, "protein": 8, "carbs": 39, "fat": 4, "fiber": 5,
        "vitamins": ["Iron", "Magnesium", "B2"],
        "allergens": [], "category": "grain", "cuisine": "universal",
    },
    "chicken breast": {
        "calories": 165, "protein": 31, "carbs": 0, "fat": 4, "fiber": 0,
        "vitamins": ["B6", "B12", "Niacin"],
        "allergens": [], "category": "protein", "cuisine": "universal",
    },
    "tofu": {
        "calories": 144, "protein": 15, "carbs": 3, "fat": 9, "fiber": 2,
        "vitamins": ["Calcium", "Iron", "Manganese"],
        "allergens": ["soy"], "category": "protein", "cuisine": "Asian",
    },
    "lentils": {
        "calories": 230, "protein": 18, "carbs": 40, "fat": 1, "fiber": 16,
        "vitamins": ["Iron", "B9", "Manganese"],
        "allergens": [], "category": "protein", "cuisine": "universal",
    },
    "salmon": {
        "calories": 208, "protein": 20, "carbs": 0, "fat": 13, "fiber": 0,
        "vitamins": ["D", "B12", "Omega-3"],
        "allergens": ["fish"], "category": "protein", "cuisine": "universal",
    },
    "spinach": {
        "calories": 23, "protein": 3, "carbs": 4, "fat": 0, "fiber": 2,
        "vitamins": ["K", "A", "C", "Iron"],
        "allergens": [], "category": "vegetable", "cuisine": "universal",
    },
    "broccoli": {
        "calories": 55, "protein": 4, "carbs": 11, "fat": 1, "fiber": 5,
        "vitamins": ["C", "K", "B9"],
        "allergens": [], "category": "vegetable", "cuisine": "universal",
    },
    "avocado": {
        "calories": 234, "protein": 3, "carbs": 12, "fat": 21, "fiber": 10,
        "vitamins": ["K", "B9", "C", "E"],
        "allergens": [], "category": "healthy_fat", "cuisine": "universal",
    },
    "banana": {
        "calories": 105, "protein": 1, "carbs": 27, "fat": 0, "fiber": 3,
        "vitamins": ["B6", "C", "Potassium"],
        "allergens": [], "category": "fruit", "cuisine": "universal",
    },
    "greek yogurt": {
        "calories": 100, "protein": 17, "carbs": 6, "fat": 1, "fiber": 0,
        "vitamins": ["B12", "Calcium", "Probiotics"],
        "allergens": ["dairy"], "category": "dairy", "cuisine": "universal",
    },
    "eggs": {
        "calories": 155, "protein": 13, "carbs": 1, "fat": 11, "fiber": 0,
        "vitamins": ["B12", "D", "Choline"],
        "allergens": ["eggs"], "category": "protein", "cuisine": "universal",
    },
    "sweet potato": {
        "calories": 103, "protein": 2, "carbs": 24, "fat": 0, "fiber": 4,
        "vitamins": ["A", "B6", "C", "Potassium"],
        "allergens": [], "category": "carbohydrate", "cuisine": "universal",
    },
    "almonds": {
        "calories": 164, "protein": 6, "carbs": 6, "fat": 14, "fiber": 4,
        "vitamins": ["E", "Magnesium", "B2"],
        "allergens": ["tree_nuts"], "category": "snack", "cuisine": "universal",
    },
}

SMART_SWAPS: dict[str, list[dict]] = {
    "white rice": [
        {"swap": "brown rice", "reason": "Higher fiber, more nutrients, lower glycemic index"},
        {"swap": "quinoa", "reason": "Complete protein source with more fiber and iron"},
        {"swap": "cauliflower rice", "reason": "Very low-calorie, great for weight loss"},
    ],
    "white bread": [
        {"swap": "whole wheat bread", "reason": "More fiber and B vitamins, lower glycemic response"},
        {"swap": "oat bread", "reason": "Rich in beta-glucan fiber, heart-healthy"},
        {"swap": "lettuce wrap", "reason": "Carb-free option, high in water content"},
    ],
    "butter": [
        {"swap": "avocado", "reason": "Healthy monounsaturated fats, fiber, and potassium"},
        {"swap": "olive oil", "reason": "Rich in polyphenols, heart-protective"},
        {"swap": "almond butter", "reason": "Plant protein, vitamin E, healthy fats"},
    ],
    "sugary drinks": [
        {"swap": "infused water", "reason": "Zero calories, keeps you hydrated"},
        {"swap": "green tea", "reason": "Antioxidants, slight metabolism boost"},
        {"swap": "coconut water", "reason": "Natural electrolytes, low sugar"},
    ],
    "potato chips": [
        {"swap": "almonds", "reason": "Protein and healthy fats keep you fuller longer"},
        {"swap": "air-popped popcorn", "reason": "Whole grain, high fiber, low calorie"},
        {"swap": "roasted chickpeas", "reason": "High protein and fiber, satisfying crunch"},
    ],
    "red meat": [
        {"swap": "chicken breast", "reason": "Lower saturated fat, same high protein"},
        {"swap": "salmon", "reason": "Omega-3 fatty acids, anti-inflammatory"},
        {"swap": "lentils", "reason": "Plant protein, iron-rich, zero cholesterol"},
    ],
    "ice cream": [
        {"swap": "frozen banana nice cream", "reason": "Natural sweetness, potassium, zero added sugar"},
        {"swap": "greek yogurt parfait", "reason": "Protein-rich, probiotics, controlled sugar"},
        {"swap": "coconut milk ice cream", "reason": "Dairy-free, medium-chain triglycerides"},
    ],
    "mayo": [
        {"swap": "hummus", "reason": "Plant protein, fiber, B vitamins"},
        {"swap": "mashed avocado", "reason": "Heart-healthy fats, potassium"},
        {"swap": "greek yogurt", "reason": "High protein, probiotics, lower fat"},
    ],
}

HEALTH_GOAL_MACROS: dict[str, dict] = {
    "weight_loss": {"calories": 1500, "protein_pct": 35, "carbs_pct": 35, "fat_pct": 30},
    "muscle_gain": {"calories": 2800, "protein_pct": 35, "carbs_pct": 45, "fat_pct": 20},
    "maintenance": {"calories": 2000, "protein_pct": 25, "carbs_pct": 50, "fat_pct": 25},
    "diabetes_management": {"calories": 1800, "protein_pct": 25, "carbs_pct": 40, "fat_pct": 35},
    "heart_health": {"calories": 1900, "protein_pct": 20, "carbs_pct": 50, "fat_pct": 30},
    "athletic_performance": {"calories": 3200, "protein_pct": 30, "carbs_pct": 50, "fat_pct": 20},
}


def get_food_info(food_name: str) -> dict | None:
    return FOOD_DB.get(food_name.lower().strip())


def get_swaps(food_name: str) -> list[dict]:
    return SMART_SWAPS.get(food_name.lower().strip(), [])


def get_goal_macros(goal: str) -> dict:
    return HEALTH_GOAL_MACROS.get(goal.lower().replace(" ", "_"), HEALTH_GOAL_MACROS["maintenance"])


def filter_foods_by_allergens(allergens: list[str]) -> list[str]:
    """Return food names that are safe (contain none of the specified allergens)."""
    safe = []
    for name, info in FOOD_DB.items():
        if not any(a in info.get("allergens", []) for a in allergens):
            safe.append(name)
    return safe
