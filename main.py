"""
FastAPI backend for the AI Nutrition Assistant.
Powered by IBM watsonx.ai (Granite) model.
"""
import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

from nutrition_engine import (
    generate_meal_plan,
    analyze_food,
    get_food_swaps,
    analyze_food_image,
    analyze_grocery_label,
    chat_with_nutritionist,
    compare_foods,
)
from image_processor import process_food_image, parse_nutrition_label_text

load_dotenv()

app = FastAPI(
    title="AI Nutrition Assistant",
    description="Powered by IBM Granite (watsonx.ai) — Personalized nutrition guidance",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────── Request Models ───────────────────────

class MealPlanRequest(BaseModel):
    health_goal: str = Field(..., example="weight_loss")
    dietary_preferences: list[str] = Field(default=[], example=["vegetarian"])
    allergies: list[str] = Field(default=[], example=["gluten", "dairy"])
    medical_conditions: list[str] = Field(default=[], example=["diabetes"])
    fitness_routine: str = Field(default="light exercise 3x/week", example="gym 5x/week")
    cultural_background: str = Field(default="no preference", example="South Indian")
    days: int = Field(default=7, ge=1, le=14)


class FoodAnalysisRequest(BaseModel):
    food_name: str = Field(..., example="quinoa")
    portion: str = Field(default="100g", example="1 cup (185g)")


class FoodSwapRequest(BaseModel):
    food_to_replace: str = Field(..., example="white rice")
    reason: str = Field(default="looking for healthier option", example="reduce calories")
    user_goal: str = Field(default="maintenance", example="weight_loss")


class ChatMessage(BaseModel):
    message: str = Field(..., example="What should I eat before a morning workout?")
    conversation_history: list[dict] = Field(default=[])


class FoodCompareRequest(BaseModel):
    food_a: str = Field(..., example="brown rice")
    food_b: str = Field(..., example="quinoa")
    context: str = Field(default="", example="for a diabetic person")


class GroceryLabelRequest(BaseModel):
    label_text: str = Field(..., example="Calories 250, Total Fat 12g, Sodium 480mg ...")


# ─────────────────────── API Endpoints ───────────────────────

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI Nutrition Assistant",
        "model": "IBM Granite (watsonx.ai)",
        "version": "1.0.0",
    }


@app.post("/api/meal-plan")
async def create_meal_plan(req: MealPlanRequest):
    """Generate a personalized multi-day meal plan."""
    try:
        result = generate_meal_plan(
            health_goal=req.health_goal,
            dietary_preferences=req.dietary_preferences,
            allergies=req.allergies,
            medical_conditions=req.medical_conditions,
            fitness_routine=req.fitness_routine,
            cultural_background=req.cultural_background,
            days=req.days,
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-food")
async def food_analysis(req: FoodAnalysisRequest):
    """Get detailed nutritional analysis of a specific food."""
    try:
        result = analyze_food(req.food_name, req.portion)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/food-swap")
async def food_swap(req: FoodSwapRequest):
    """Get smart food swap recommendations."""
    try:
        result = get_food_swaps(req.food_to_replace, req.reason, req.user_goal)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def nutritionist_chat(req: ChatMessage):
    """Chat with the AI nutritionist."""
    try:
        result = chat_with_nutritionist(req.message, req.conversation_history)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/compare-foods")
async def compare_food_items(req: FoodCompareRequest):
    """Compare two foods and explain which is better and why."""
    try:
        result = compare_foods(req.food_a, req.food_b, req.context)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-label")
async def analyze_label(req: GroceryLabelRequest):
    """Analyze a grocery nutrition label."""
    try:
        parsed = parse_nutrition_label_text(req.label_text)
        result = analyze_grocery_label(req.label_text)
        result["parsed_values"] = parsed
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-image")
async def analyze_image_upload(
    file: UploadFile = File(...),
    image_type: str = Form(default="food_photo"),
):
    """
    Upload a food photo or grocery label image for analysis.
    image_type: 'food_photo' | 'grocery_label'
    """
    try:
        image_bytes = await file.read()
        processed = process_food_image(image_bytes, image_type)

        if processed["type"] == "food_photo" and processed["detected_items"]:
            analysis = analyze_food_image(processed["detected_items"])
            return {
                "success": True,
                "data": {
                    "image_info": processed,
                    "nutrition_analysis": analysis,
                },
            }
        else:
            return {
                "success": True,
                "data": {
                    "image_info": processed,
                    "message": "Image processed. Use /api/analyze-label for detailed label analysis.",
                },
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Mount frontend static files
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", 8000)),
        reload=True,
    )
