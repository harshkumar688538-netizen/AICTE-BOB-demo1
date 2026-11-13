"""
Prompt engineering templates for IBM Granite LLM.
All prompts follow the Granite instruction format.
"""


def build_system_preamble() -> str:
    return (
        "You are NutriAI, an expert AI nutrition assistant powered by IBM Granite. "
        "You provide evidence-based, personalized nutrition guidance. "
        "You are empathetic, culturally aware, and always safety-conscious. "
        "Never diagnose medical conditions; always recommend consulting a doctor for medical concerns. "
        "Keep responses practical, structured, and actionable."
    )


def meal_plan_prompt(
    health_goal: str,
    dietary_preferences: list[str],
    allergies: list[str],
    medical_conditions: list[str],
    fitness_routine: str,
    cultural_background: str,
    days: int = 7,
) -> str:
    allergy_str = ", ".join(allergies) if allergies else "none"
    pref_str = ", ".join(dietary_preferences) if dietary_preferences else "no specific preference"
    condition_str = ", ".join(medical_conditions) if medical_conditions else "none"

    return f"""{build_system_preamble()}

### Task: Generate a {days}-day personalized meal plan

**User Profile:**
- Health Goal: {health_goal}
- Dietary Preferences: {pref_str}
- Allergies/Intolerances: {allergy_str}
- Medical Conditions: {condition_str}
- Fitness Routine: {fitness_routine}
- Cultural Background: {cultural_background}

### Instructions:
1. Create a detailed {days}-day meal plan with Breakfast, Morning Snack, Lunch, Afternoon Snack, and Dinner for each day.
2. Ensure meals respect all allergies and dietary preferences.
3. Align calorie and macro targets with the health goal.
4. Include cultural food preferences where possible.
5. For each meal, list: food items, estimated calories, key nutrients.
6. Add a brief daily tip related to the health goal.

### {days}-Day Meal Plan:
"""


def food_analysis_prompt(food_name: str, portion: str = "100g") -> str:
    return f"""{build_system_preamble()}

### Task: Nutritional Analysis

Provide a comprehensive nutritional analysis for: **{food_name}** ({portion} serving)

Include:
1. **Macronutrients** (calories, protein, carbohydrates, fat, fiber)
2. **Key Micronutrients** (vitamins and minerals)
3. **Health Benefits** (3-5 evidence-based benefits)
4. **Who should eat more of this** (target groups)
5. **Who should limit this** (contraindications)
6. **Best time to consume** and preparation tips

### Analysis:
"""


def food_swap_prompt(food_to_replace: str, reason: str, user_goal: str) -> str:
    return f"""{build_system_preamble()}

### Task: Smart Food Swap Recommendation

The user wants to replace: **{food_to_replace}**
Reason for swap: {reason}
User's health goal: {user_goal}

Provide:
1. **Top 3 Smart Swaps** with specific alternatives
2. For each swap: nutritional comparison, why it's better, how to use it
3. **Practical transition tips** to make the swap sustainable
4. **Recipe idea** using the best swap alternative

### Smart Swaps:
"""


def image_food_analysis_prompt(detected_items: list[str]) -> str:
    items_str = ", ".join(detected_items) if detected_items else "food items"
    return f"""{build_system_preamble()}

### Task: Food Image Analysis

Food items detected in the image: {items_str}

Provide:
1. **Nutritional breakdown** for each detected item
2. **Overall meal assessment**: calorie estimate, macro balance
3. **Health rating** (1-10) with justification
4. **Improvement suggestions**: what to add, reduce, or swap
5. **Portion guidance**: ideal serving sizes

### Analysis:
"""


def grocery_label_prompt(label_text: str) -> str:
    return f"""{build_system_preamble()}

### Task: Grocery Label Analysis

Nutrition label data:
{label_text}

Provide:
1. **Red flags**: concerning ingredients, excessive nutrients (sodium, sugar, saturated fat)
2. **Green flags**: beneficial ingredients, good nutrient profile
3. **Ingredient decode**: explain any complex/artificial ingredients
4. **Overall health score** (A/B/C/D/F) with reasoning
5. **Healthier alternative suggestions**

### Label Analysis:
"""


def chat_prompt(user_message: str, conversation_history: list[dict]) -> str:
    history_text = ""
    for turn in conversation_history[-6:]:  # Keep last 6 turns for context
        role = "User" if turn["role"] == "user" else "NutriAI"
        history_text += f"{role}: {turn['content']}\n"

    return f"""{build_system_preamble()}

### Conversation History:
{history_text}
### Current Question:
User: {user_message}

### NutriAI Response:
"""


def why_food_better_prompt(food_a: str, food_b: str, context: str = "") -> str:
    ctx = f" (Context: {context})" if context else ""
    return f"""{build_system_preamble()}

### Task: Comparative Food Analysis{ctx}

Compare **{food_a}** vs **{food_b}**

Explain:
1. **Nutritional comparison** (side-by-side key metrics)
2. **When {food_a} is better** (specific scenarios, goals, conditions)
3. **When {food_b} is better** (specific scenarios, goals, conditions)
4. **Verdict** for different user types (athlete, diabetic, weight loss, heart health)
5. **Can they be combined?** Synergistic benefits

### Comparison:
"""
