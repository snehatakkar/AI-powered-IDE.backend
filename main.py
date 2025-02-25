from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ Allow CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],
)

# ✅ Define the request model
class CodeRequest(BaseModel):
    code: str

# ✅ This endpoint should only accept POST requests
@app.post("/analyze-code")
async def analyze_code(request: CodeRequest):
    return {"message": "✅ POST request received!", "code": request.code}

# ✅ Root endpoint to check if the server is running
@app.get("/")
async def root():
    return {"message": "🚀 AI Code Suggestion Backend is Running!"}
