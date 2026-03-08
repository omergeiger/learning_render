# Learn Render - Minimal Server Deployment

A minimal HTTP server to learn Render.com deployment basics.

## Goal

Deploy a simple Flask server to Render.com with two endpoints:
- **GET /status** - Returns server status
- **POST /write** - Echoes back the input text

## Tech Stack

- Python 3.12+
- Flask (minimal web framework)
- Render.com (deployment platform)

## Project Structure

```
learning_render/
├── learn_render.md        # This file
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
└── README.md             # Project readme (optional)
```

## Implementation Plan

### Step 1: Create Flask Application

**app.py**:
```python
from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'message': 'Server is running'
    })

@app.route('/write', methods=['POST'])
def write():
    """Echo endpoint - returns input text"""
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({
            'error': 'Missing text field in request body'
        }), 400

    input_text = data['text']

    return jsonify({
        'echo': input_text,
        'length': len(input_text),
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

**requirements.txt**:
```
flask==3.1.0
```

**.gitignore**:
```
__pycache__/
*.pyc
.env
.venv/
venv/
```

### Step 2: Test Locally

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

Test endpoints:
```bash
# Test status endpoint
curl http://localhost:5000/status

# Test write endpoint
curl -X POST http://localhost:5000/write \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, Render!"}'
```

Expected responses:
```json
// GET /status
{
  "status": "ok",
  "timestamp": "2026-03-08T10:30:00.000000",
  "message": "Server is running"
}

// POST /write
{
  "echo": "Hello, Render!",
  "length": 14,
  "timestamp": "2026-03-08T10:30:00.000000"
}
```

### Step 3: Deploy to Render

#### 3.1 Prepare Git Repository

```bash
git init
git add app.py requirements.txt .gitignore
git commit -m "Initial commit: minimal Flask server for Render"

# Create GitHub repo and push
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

#### 3.2 Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `learn-render-server`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: `Free`
5. Click **"Create Web Service"**

#### 3.3 Wait for Deployment

- Monitor build logs in Render dashboard
- Wait for status to change to **"Live"**
- Note your public URL: `https://learn-render-server.onrender.com`

### Step 4: Test Production Deployment

```bash
# Test status endpoint
curl https://learn-render-server.onrender.com/status

# Test write endpoint
curl -X POST https://learn-render-server.onrender.com/write \
  -H "Content-Type: application/json" \
  -d '{"text": "Testing from production!"}'
```

## Success Criteria

✅ Server runs locally on port 5000
✅ GET /status returns JSON with status and timestamp
✅ POST /write echoes input text back
✅ Code pushed to GitHub
✅ Successfully deployed to Render
✅ Public URL is accessible
✅ Both endpoints work in production

## Render Free Tier Notes

- ⏰ Service spins down after 15 minutes of inactivity
- 🐌 First request after sleep takes 30-60 seconds to wake up
- 📊 750 hours/month free tier limit
- 💾 No persistent storage on free tier (ephemeral disk)
- 🔄 Auto-deploys on git push to main branch

## Troubleshooting

**Build fails on Render**:
- Check requirements.txt syntax
- Ensure Python 3 is selected as environment
- Review build logs for specific error

**Server won't start**:
- Verify start command is `python app.py`
- Check that app.py reads PORT from environment: `os.getenv('PORT', 5000)`
- Review Render logs for errors

**502 Bad Gateway**:
- Normal on free tier after 15 min inactivity
- Wait 30-60 seconds for server to wake up
- Retry request

**POST /write returns 400**:
- Ensure request has `Content-Type: application/json` header
- Verify JSON body has `text` field
- Check request body syntax

## Next Steps After Learning Render

Once comfortable with basic Render deployment:

1. Add more endpoints (PUT, DELETE)
2. Add request validation with JSON schemas
3. Implement logging
4. Add error handling middleware
5. Move to full chatbot deployment (see full_app_plan.md)

## Learning Objectives Achieved

- ✅ Understand Render.com deployment workflow
- ✅ Configure Python web service on Render
- ✅ Set up Git-based continuous deployment
- ✅ Test endpoints locally and in production
- ✅ Understand free tier limitations
- ✅ Read environment variables (PORT)
- ✅ Handle JSON requests and responses

---

**Estimated Time**: 30-45 minutes
**Difficulty**: Beginner
**Cost**: Free (Render free tier)
