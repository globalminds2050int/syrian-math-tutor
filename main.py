from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import base64
import os
from typing import Optional
import json

app = FastAPI(title="Syrian Math Tutor API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Master Tutor System Prompt
MASTER_TUTOR_PROMPT = """You are a revolutionary AI math tutor for Syrian students that adapts like a master teacher.

🎯 CORE PRINCIPLE: ADAPTIVE INTELLIGENCE

You constantly adapt based on:
- Student's comprehension level
- Problem difficulty
- Student's language level (Arabic/English, beginner → advanced)
- Learning style (visual, verbal, story-based)
- Prior knowledge

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🇸🇾 LANGUAGE DETECTION & RESPONSE:

CRITICAL: Detect the language of the problem and respond in the SAME language!

If problem contains Arabic text → RESPOND IN SYRIAN DIALECT (اللهجة الشامية)
If problem is in English → Respond in English

SYRIAN DIALECT REQUIREMENTS when responding in Arabic:
- Use natural Syrian expressions: "تعا نحل" (not "لنحل")
- Use "بدنا" (we want), "منطرح" (we subtract), "شايف؟" (you see?)
- Use "يلا بينا", "شو رأيك", "هلأ", "شوي", "كتير"
- Always use English letters for variables: x, y, z (NEVER س، ص، ع)
- Use Western numerals: 1, 2, 3 (not ١، ٢، ٣)
- Encouragement: "برافو!", "يا سلام!", "ولك روعة!", "تمام!"

Example in Syrian:
"أهلا فيك! تعا نحل هالمسألة سوا 😊
عندنا: 2x + 5 = 13
شايف؟ بدنا نشيل ال 5 من الطرفين...
يلا بينا!"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌍 BILINGUAL TEACHING (Math Language ↔ Real World)

Simple problems: One language sufficient
Medium problems: Blend both languages  
Complex problems: Full bilingual explanation

When confused → Switch language approach
When mastering → Use advanced math language

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 LANGUAGE LEVELS (Adapt strategically):

LEVEL 1 - Pure Real-World: "You have 5 apples, get 3 more..."
LEVEL 2 - Story Math: "Let x be cookies. Add 5. Total is 12."
LEVEL 3 - Simple Math: "Solve x + 5 = 12"
LEVEL 4 - Standard Math: "Solve using inverse operations"
LEVEL 5 - Advanced Math: "Determine solution set preserving equivalence"

Choose based on problem complexity and student level.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎭 TEACHING MODES (Switch as needed):

STORY_MODE: Use real-world scenarios (money, pizza, backpacks)
VISUAL_MODE: Balance scales, diagrams, step-by-step visual
SOCRATIC_MODE: Guide with questions (Why? How? What if?)
STEP_BY_STEP: Clear numbered instructions
FORMAL_LECTURE: Structured comprehensive explanation
ERROR_ANALYSIS: Gentle correction with understanding

Switch modes if student struggles!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 GOLDEN RULES (Repeat with variation):

1. Balance: "Whatever you do to one side, MUST do to other" ⚖️
2. No Zero Division: "IN OTHER WORDS: Exclude values making denominator zero" 🚫
3. Always Verify: "Substitute back to check" ✅
4. Order Matters: "PEMDAS / Undo in reverse order" 🔄

Vary phrasing each time!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 CREATIVE METAPHORS (Rotate through):

Money: wallets, savings, debt
Food: pizza, apples, chocolate
School: backpacks, pencils, books
Balance: scales, seesaws
Containers: boxes, bags, jars
Temperature: above/below zero
Sports: scores, teams
Travel: distance, speed

Match to Syrian context when relevant!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 RESPONSE STRUCTURE:

1. Identify problem type & difficulty
2. Choose teaching mode & language level
3. Build intuition (if needed - story/visual)
4. Solve step-by-step with WHY explanations
5. Verify answer (math + logic check)
6. Extension questions (if appropriate)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❤️ EMOTIONAL INTELLIGENCE:

Frustrated → Encourage, simplify
Confident → Challenge, extend
Confused → Slow down, use stories
Bored → Add complexity, make interesting

Be encouraging, patient, and excited about math!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 GOAL: Not just solve problems → TEACH UNDERSTANDING
Build confidence, create mathematicians! 🚀

Respond in Arabic if problem is in Arabic, English if in English, or mix as needed."""


async def call_groq_api(messages: list, model: str = "llama-3.3-70b-versatile") -> dict:
    """Call Groq API directly using httpx"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Syrian Math Tutor API",
        "version": "3.0",
        "features": [
            "Adaptive teaching (5 language levels)",
            "Bilingual (Math ↔ Real World)",
            "Multiple teaching modes",
            "Creative explanations",
            "Emotional intelligence",
            "Syrian curriculum aligned"
        ]
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api_key_configured": bool(GROQ_API_KEY),
        "groq_api_url": GROQ_API_URL
    }


@app.post("/solve")
async def solve_problem(
    problem_text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    """
    Solve a math problem from text or image
    
    Args:
        problem_text: Text description of the problem
        image: Image file containing the problem
    
    Returns:
        JSON with solution, explanation, and teaching content
    """
    try:
        if not problem_text and not image:
            raise HTTPException(
                status_code=400,
                detail="Either problem_text or image must be provided"
            )
        
        # Prepare messages for Groq API
        messages = [
            {"role": "system", "content": MASTER_TUTOR_PROMPT}
        ]
        
        # Handle image upload
        if image:
            try:
                # Read image and convert to base64
                image_data = await image.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
                
                # Determine image mime type
                mime_type = image.content_type or "image/jpeg"
                
                # Detect language from problem_text
                is_arabic = problem_text and any('\u0600' <= c <= '\u06FF' for c in problem_text)
                instruction = "حل هذه المسألة من الصورة بالتفصيل بالعربي." if is_arabic else problem_text or "Solve this math problem from the image."
                
                user_message = {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": instruction
                        }
                    ]
                }
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Image processing error: {str(e)}")
        else:
            # Text-only problem - detect language
            is_arabic = any('\u0600' <= c <= '\u06FF' for c in problem_text)
            
            if is_arabic:
                instruction = f"{problem_text}\n\nمهم: أجب بالكامل باللهجة الشامية السورية فقط!"
            else:
                instruction = f"{problem_text}\n\nProvide adaptive teaching based on the problem difficulty."
            
            user_message = {
                "role": "user",
                "content": instruction
            }
        
        messages.append(user_message)
        
        # Call Groq API
        response_data = await call_groq_api(messages)
        
        # Extract solution from response
        if "choices" not in response_data or not response_data["choices"]:
            raise HTTPException(
                status_code=500,
                detail="Invalid response from AI service"
            )
        
        solution = response_data["choices"][0]["message"]["content"]
        
        return JSONResponse(content={
            "success": True,
            "solution": solution,
            "model": response_data.get("model", "llama-3.3-70b-versatile"),
            "usage": response_data.get("usage", {}),
            "metadata": {
                "has_image": image is not None,
                "has_text": problem_text is not None,
                "teaching_mode": "adaptive"
            }
        })
        
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calling AI service: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/chat")
async def chat(
    message: str = Form(...),
    conversation_history: Optional[str] = Form(None)
):
    """
    Continue a conversation with the tutor
    
    Args:
        message: User's message/question
        conversation_history: JSON string of previous messages
    
    Returns:
        JSON with tutor's response
    """
    try:
        messages = [
            {"role": "system", "content": MASTER_TUTOR_PROMPT}
        ]
        
        # Add conversation history if provided
        if conversation_history:
            try:
                history = json.loads(conversation_history)
                messages.extend(history)
            except json.JSONDecodeError:
                pass  # Invalid JSON, ignore
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Call Groq API
        response_data = await call_groq_api(messages)
        
        # Extract response
        if "choices" not in response_data or not response_data["choices"]:
            raise HTTPException(
                status_code=500,
                detail="Invalid response from AI service"
            )
        
        response_text = response_data["choices"][0]["message"]["content"]
        
        return JSONResponse(content={
            "success": True,
            "response": response_text,
            "model": response_data.get("model", "llama-3.3-70b-versatile")
        })
        
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calling AI service: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
