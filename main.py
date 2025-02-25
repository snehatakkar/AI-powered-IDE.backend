from fastapi import FastAPI
import ast
import requests
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# ✅ Ensure the API key is set correctly
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    print("❌ No API key found! Please set HUGGINGFACE_API_KEY as an environment variable.")

app = FastAPI()

# ✅ Enable CORS for frontend communication
# ✅ Allow CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://snehatakkar.github.io/AI-powered-IDE/"],  
    allow_origins=["*"],  # Change this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_methods=["*"],  # ✅ Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],
)

# ✅ Define input model
# ✅ Define the request model
class CodeRequest(BaseModel):
    code: str

# ✅ Function to check Python syntax
def analyze_python_code(code: str):
    try:
        ast.parse(code)  # ✅ Parse the code to check for syntax errors
        return "✅ No syntax errors detected."
    except SyntaxError as e:
        return f"❌ Syntax Error: {e.msg} at line {e.lineno}, column {e.offset}"

# ✅ Function to get AI code suggestions from Hugging Face
def get_ai_suggestions(code: str):
    if not HUGGINGFACE_API_KEY:
        return "❌ AI suggestions unavailable: API key not set."

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": f"Improve this Python code:\n{code}"}

    response = requests.post(
        "https://api-inference.huggingface.co/models/bigcode/starcoder",
        headers=headers,
        json=payload
    )

    # ✅ Debugging logs
    print(f"🔹 API Response Status: {response.status_code}")  
    print(f"🔹 API Response Data: {response.text}")

    if response.status_code == 200:
        try:
            ai_response = response.json()
            return ai_response[0].get("generated_text", "No suggestion provided.")
        except (IndexError, KeyError, ValueError):
            return "⚠️ AI suggestion response format error."
    else:
        return f"❌ AI suggestion failed: {response.text}"

# ✅ Endpoint for Syntax Check & AI Suggestion
# ✅ This endpoint should only accept POST requests
@app.post("/analyze-code")
async def analyze_code(request: CodeRequest):
    syntax_check = analyze_python_code(request.code)
    ai_suggestions = get_ai_suggestions(request.code)
    
    return {"syntax_check": syntax_check, "ai_suggestions": ai_suggestions}
    return {"message": "✅ POST request received!", "code": request.code}

# ✅ Root endpoint to verify FastAPI is running
# ✅ Root endpoint to check if the server is running
@app.get("/")
async def root():
    return {"message": "🚀 AI Code Suggestion Backend is Running!"}
