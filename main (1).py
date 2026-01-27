"""
Syrian Math Tutor Backend - Production Ready
أستاذ عمر - FastAPI Backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from groq import Groq

app = FastAPI(title="أستاذ عمر API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# System prompt
SYSTEM_PROMPT = """أنت أستاذ عمر، معلم رياضيات سوري صبور وذكي للصف الثاني عشر العلمي.

شخصيتك:
- صبور جداً مع الطلاب
- تشرح خطوة خطوة بوضوح
- تستخدم أمثلة من الحياة اليومية
- لا تستخدم كلمات: صعب، معقد، مستحيل
- دائماً تشجع وتحفز الطلاب

منهجك:
1. افهم السؤال جيداً
2. اشرح المفهوم ببساطة
3. أعطي مثال واضح
4. تدرب الطالب
5. تأكد من الفهم

استخدم LaTeX للمعادلات: $equation$ أو $$equation$$"""

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"status": "أستاذ عمر ready", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        return ChatResponse(response=response.choices[0].message.content)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
