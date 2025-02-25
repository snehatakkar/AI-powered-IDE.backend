from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all HTTP methods (including POST)
    allow_headers=["*"],
)

# ✅ Define the request model
class CodeRequest(BaseModel):
    code: str

# ✅ Ensure this endpoint ONLY supports POST requests
@app.post("/analyze-code")
async def analyze_code(request: CodeRequest):
    print("✅ Received POST request to /analyze-code")
    return {"message": "✅ POST request received!", "code": request.code}

# ✅ Root endpoint to check if the server is running
@app.get("/")
async def root():
    return {"message": "🚀 AI Code Suggestion Backend is Running!"}
