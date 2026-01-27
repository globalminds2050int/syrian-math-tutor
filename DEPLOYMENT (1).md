# Syrian Math Tutor - Backend Deployment Guide

## Files to Upload to GitHub

1. `main.py` - FastAPI backend
2. `requirements.txt` - Python dependencies
3. `.python-version` - Python version for Render

## Deployment Steps

### 1. Upload to GitHub

```bash
# In GitHub repo page, click "uploading an existing file"
# Upload all 3 files
# Commit
```

### 2. Connect to Render

1. Go to Render dashboard
2. Click "New Web Service"
3. Click "Connect repository"
4. Select "syrian-math-tutor"
5. Configure:
   - Name: `omar-tutor`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. Add Environment Variable

In Render dashboard:
- Key: `GROQ_API_KEY`
- Value: [Get from console.groq.com]

### 4. Deploy

Click "Create Web Service"

Wait 3-5 minutes.

Your API will be live at: `https://omar-tutor.onrender.com`

## Test API

```bash
curl https://omar-tutor.onrender.com/health
```

Should return: `{"status":"healthy"}`

## Next Steps

1. Get Groq API key from: https://console.groq.com
2. Build frontend on Hostinger
3. Connect frontend to this API

## Frontend Integration

```javascript
const API_URL = "https://omar-tutor.onrender.com";

async function askOmar(question) {
    const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            message: question,
            session_id: "user123"
        })
    });
    
    const data = await response.json();
    return data.response;
}
```

## Professional Features Included

✅ CORS enabled for web access
✅ Health check endpoint
✅ Proper error handling
✅ Production-ready structure
✅ Scalable architecture

## Cost

- Render Free Tier: 750 hours/month
- Groq Free Tier: 14,400 requests/day
- Total: $0 for testing phase

## When to Upgrade

- >500 active students
- Need faster response times
- Want custom domain

Then: Render paid ($7-25/mo)
