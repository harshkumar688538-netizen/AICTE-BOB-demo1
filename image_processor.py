"""
Multimodal input processor: handles image uploads (food photos, grocery labels).
Extracts food items using basic heuristics + prepares data for LLM analysis.
"""
import io
import base64
from PIL import Image


# Common food colors for basic heuristic detection (fallback when no vision model)
FOOD_COLOR_HINTS = {
    "green": ["spinach", "broccoli", "lettuce", "avocado", "cucumber", "peas", "kale"],
    "orange": ["sweet potato", "carrot", "orange", "mango", "pumpkin"],
    "red": ["tomato", "red pepper", "strawberry", "apple", "watermelon"],
    "yellow": ["banana", "corn", "lemon", "pineapple", "egg yolk"],
    "brown": ["rice", "bread", "meat", "nuts", "chocolate", "beans"],
    "white": ["rice", "milk", "tofu", "egg white", "cauliflower", "onion"],
    "purple": ["blueberry", "eggplant", "purple cabbage", "grape", "beetroot"],
}

# Common nutrition label keywords to parse
LABEL_KEYWORDS = [
    "calories", "total fat", "saturated fat", "trans fat", "cholesterol",
    "sodium", "total carbohydrate", "dietary fiber", "total sugars",
    "added sugars", "protein", "vitamin d", "calcium", "iron", "potassium",
    "serving size", "servings per container", "ingredients",
]


def decode_image(image_bytes: bytes) -> Image.Image:
    """Decode image bytes into a PIL Image."""
    return Image.open(io.BytesIO(image_bytes))


def image_to_base64(image_bytes: bytes) -> str:
    """Convert image bytes to base64 string for LLM multimodal inputs."""
    return base64.b64encode(image_bytes).decode("utf-8")


def analyze_image_colors(img: Image.Image) -> list[str]:
    """
    Heuristic: sample dominant colors from the image and
    map to likely food categories.
    """
    img_resized = img.resize((50, 50)).convert("RGB")
    pixels = list(img_resized.getdata())

    color_counts = {"green": 0, "orange": 0, "red": 0, "yellow": 0,
                    "brown": 0, "white": 0, "purple": 0}

    for r, g, b in pixels:
        if g > r and g > b and g > 80:
            color_counts["green"] += 1
        elif r > 180 and g > 100 and b < 80:
            color_counts["orange"] += 1
        elif r > 180 and g < 100 and b < 100:
            color_counts["red"] += 1
        elif r > 200 and g > 200 and b < 100:
            color_counts["yellow"] += 1
        elif r > 200 and g > 200 and b > 200:
            color_counts["white"] += 1
        elif r > 60 and r < 160 and g > 40 and g < 120 and b < 80:
            color_counts["brown"] += 1
        elif b > r and b > g and r > 80:
            color_counts["purple"] += 1

    # Return top 3 dominant colors
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
    dominant = [c for c, count in sorted_colors[:3] if count > 20]
    return dominant


def detect_food_items_from_image(image_bytes: bytes) -> list[str]:
    """
    Detect food items from an image using color heuristics.
    In production, this would call a vision model (e.g., IBM visual recognition).
    Returns a list of likely food items for LLM analysis.
    """
    img = decode_image(image_bytes)
    dominant_colors = analyze_image_colors(img)

    detected = []
    seen = set()
    for color in dominant_colors:
        for food in FOOD_COLOR_HINTS.get(color, [])[:2]:
            if food not in seen:
                detected.append(food)
                seen.add(food)

    # Fallback: if nothing detected, return generic description
    if not detected:
        detected = ["mixed food items", "unknown ingredients"]

    return detected


def get_image_metadata(image_bytes: bytes) -> dict:
    """Extract basic metadata from an image."""
    img = decode_image(image_bytes)
    return {
        "width": img.width,
        "height": img.height,
        "format": img.format or "unknown",
        "mode": img.mode,
        "size_kb": round(len(image_bytes) / 1024, 2),
    }


def parse_nutrition_label_text(raw_text: str) -> dict:
    """
    Parse structured data from a nutrition label OCR text.
    Extracts key nutritional values.
    """
    parsed = {}
    lines = raw_text.lower().split("\n")

    for i, line in enumerate(lines):
        for keyword in LABEL_KEYWORDS:
            if keyword in line:
                # Try to find a numeric value near the keyword
                parts = line.replace(keyword, "").strip()
                # Extract numbers
                numbers = []
                for part in parts.split():
                    part_clean = part.replace("g", "").replace("mg", "").replace("%", "")
                    try:
                        numbers.append(float(part_clean))
                    except ValueError:
                        pass
                if numbers:
                    parsed[keyword] = numbers[0]
                else:
                    parsed[keyword] = "see label"

    return parsed


def process_food_image(image_bytes: bytes, image_type: str = "food_photo") -> dict:
    """
    Main entry point for image processing.
    image_type: 'food_photo' | 'grocery_label'
    """
    metadata = get_image_metadata(image_bytes)

    if image_type == "grocery_label":
        # For label images, we return metadata and ask user to also paste label text
        return {
            "type": "grocery_label",
            "metadata": metadata,
            "message": "Image received. For best analysis, please also paste the nutrition label text.",
            "detected_items": [],
        }
    else:
        detected_items = detect_food_items_from_image(image_bytes)
        return {
            "type": "food_photo",
            "metadata": metadata,
            "detected_items": detected_items,
        }
