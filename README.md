# 🥦 NutriAI — AI Nutrition Assistant
### Powered by IBM Granite (watsonx.ai) · AICTE Problem Statement #8

An intelligent, interactive, and adaptive virtual nutrition assistant that leverages **IBM Granite LLM** via **IBM watsonx.ai** to deliver personalized nutrition guidance at scale.

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **AI Chat** | Natural language conversation with the AI nutritionist |
| 📅 **Meal Planner** | Personalized multi-day meal plans (health goals, allergies, culture) |
| 🔬 **Food Analysis** | Deep nutritional breakdown of any food with health insights |
| 🔄 **Smart Swaps** | Science-backed food substitution recommendations |
| 📸 **Food Photo Analysis** | Upload a meal photo for instant nutritional assessment |
| 🏷️ **Label Scanner** | Paste grocery labels for red-flag detection and health scoring |
| ⚖️ **Food Comparison** | Side-by-side evidence-based comparison of two foods |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   FRONTEND (HTML5)                   │
│   Chat · Meal Planner · Analysis · Swaps · Image    │
└────────────────────┬────────────────────────────────┘
                     │ REST API (FastAPI)
┌────────────────────▼────────────────────────────────┐
│              BACKEND (FastAPI / Python)               │
│                                                       │
│  main.py ──► nutrition_engine.py ──► prompts.py      │
│                     │                                 │
│         ┌───────────┴────────────┐                   │
│   watsonx_client.py         nutrition_data.py         │
│   (IBM Granite LLM)         (Food DB + Swaps)         │
│                                                       │
│         image_processor.py (Multimodal)               │
└───────────────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│          IBM watsonx.ai (IBM Cloud Lite)              │
│          Model: ibm/granite-13b-instruct-v2           │
└──────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11+
- IBM Cloud Lite account (free) → [cloud.ibm.com](https://cloud.ibm.com)
- IBM watsonx.ai project

### 2. Get IBM Credentials

1. Sign up at [IBM Cloud](https://cloud.ibm.com) (free Lite tier)
2. Go to [watsonx.ai](https://www.ibm.com/watsonx)
3. Create a project and note your **Project ID**
4. Generate an **API Key** from IAM → API keys

### 3. Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your credentials
WATSONX_API_KEY=your_actual_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

### 4. Install & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

Open **http://localhost:8000** in your browser.

### Windows (PowerShell one-liner)
```powershell
pip install -r requirements.txt; python main.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/chat` | Chat with AI nutritionist |
| POST | `/api/meal-plan` | Generate personalized meal plan |
| POST | `/api/analyze-food` | Nutritional analysis of a food |
| POST | `/api/food-swap` | Smart food swap recommendations |
| POST | `/api/analyze-image` | Upload food photo for analysis |
| POST | `/api/analyze-label` | Analyze grocery nutrition label |
| POST | `/api/compare-foods` | Compare two foods |

### Example: Generate Meal Plan
```bash
curl -X POST http://localhost:8000/api/meal-plan \
  -H "Content-Type: application/json" \
  -d '{
    "health_goal": "weight_loss",
    "dietary_preferences": ["vegetarian"],
    "allergies": ["gluten"],
    "medical_conditions": [],
    "fitness_routine": "yoga 3x/week",
    "cultural_background": "South Indian",
    "days": 7
  }'
```

### Example: Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What should I eat before a morning workout?", "conversation_history": []}'
```

---

## 📂 Project Structure

```
AICTE - Nutrition Agent/
├── main.py                # FastAPI server + all API endpoints
├── watsonx_client.py      # IBM Granite (watsonx.ai) client
├── nutrition_engine.py    # Core AI features orchestration
├── prompts.py             # LLM prompt templates (Granite format)
├── nutrition_data.py      # Food database, macros, smart swaps
├── image_processor.py     # Multimodal image analysis
├── frontend/
│   └── index.html         # Full-featured single-page UI
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🤖 IBM Granite Integration

This project uses **IBM Granite 13B Instruct v2** via IBM watsonx.ai:

- **Model**: `ibm/granite-13b-instruct-v2`
- **Platform**: IBM watsonx.ai (IBM Cloud Lite — free tier eligible)
- **SDK**: `ibm-watsonx-ai` Python SDK
- **Features used**: Text generation with custom system prompts

All prompts are engineered specifically for the Granite instruction format with a nutrition-expert system persona.

---

## 🌐 Technology Stack

| Layer | Technology |
|---|---|
| **LLM** | IBM Granite 13B Instruct (watsonx.ai) |
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript (ES2022) |
| **Image** | Pillow (PIL) |
| **Config** | python-dotenv |
| **Cloud** | IBM Cloud Lite (free tier) |

---

## 📋 AICTE Problem Statement Mapping

| Requirement | Implementation |
|---|---|
| Text input understanding | Chat API + NLP prompts |
| Voice input | Extend via Web Speech API (browser) |
| Image input (food photos) | `/api/analyze-image` + `image_processor.py` |
| Grocery label reading | `/api/analyze-label` + OCR text parsing |
| Personalized meal plans | `/api/meal-plan` with 8 profile parameters |
| Medical condition awareness | Included in meal plan prompts |
| Contextual explanations | "Why is this food better?" via compare endpoint |
| Dynamic feedback adaptation | Conversation history maintained in chat |
| Cultural preferences | Cultural background field in meal planner |
| IBM Cloud mandatory | IBM Granite via watsonx.ai (Lite tier) |

---

*Built for AICTE Internship — Problem Statement #8: Smartest AI Nutrition Assistant*
