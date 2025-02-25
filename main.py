from fastapi import FastAPI
import ast
import requests
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# ✅ Load Hugging Face API key from environment variable
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    print("❌ No API key found! Please set HUGGINGFACE_API_KEY as an environment variable.")

app = FastAPI()

# ✅ Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://snehatakkar.github.io", "http://localhost:3000"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],
)

# ✅ Define request model
class CodeRequest(BaseModel):
    code: str

# ✅ Function to check Python syntax
def analyze_python_code(code: str):
    try:
        ast.parse(code)  # ✅ Parse the code to check for syntax errors
        return "✅ No syntax errors detected."
    except SyntaxError as e:
        return f"❌ Syntax Error: {e.msg} at line {e.lineno}, column {e.offset}"

# ✅ Function to get AI suggestions from Hugging Face
def get_ai_suggestions(code: str):
    if not HUGGINGFACE_API_KEY:
        return "❌ AI suggestions unavailable: API key not set."

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": f"Improve this Python code:\n{code}"}

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/bigcode/starcoder",
            headers=headers,
            json=payload
        )

        # ✅ Debugging logs for API response
        print(f"🔹 API Response Status: {response.status_code}")  
        print(f"🔹 API Response Data: {response.text}")

        if response.status_code == 200:
            ai_response = response.json()
            return ai_response[0].get("generated_text", "No suggestion provided.")
        else:
            return f"❌ AI suggestion failed: {response.text}"

    except requests.exceptions.RequestException as e:
        return f"❌ AI request error: {str(e)}"

# ✅ API Endpoint for Syntax Check & AI Suggestion
@app.post("/analyze-code")
async def analyze_code(request: CodeRequest):
    syntax_check = analyze_python_code(request.code)
    ai_suggestions = get_ai_suggestions(request.code)
    
    return {"syntax_check": syntax_check, "ai_suggestions": ai_suggestions}

# ✅ Root endpoint to verify FastAPI is running
@app.get("/")
async def root():
    return {"message": "🚀 AI Code Suggestion Backend is Running!"}
