# Chatbot Server - Render.com Learning Project

A cloud-deployed chatbot server adapted from local_chatbot for learning Render.com deployment. This project migrates an existing Python/Flask chatbot with Ollama integration to a cloud-native architecture.

## Project Overview

This project adapts the local_chatbot implementation (originally designed for local Ollama + WhatsApp) to a cloud-deployed chatbot server on Render.com. The migration focuses on replacing local Ollama with cloud-based LLM APIs while preserving the modular architecture and WhatsApp integration capabilities.

**Source**: Adapted from `/Users/ogeiger/git/local_chatbot`

## Technology Stack

- **Runtime**: Python 3.12+
- **Framework**: Flask
- **LLM Backend**:
  - Local: Ollama (local_chatbot)
  - Cloud: Anthropic Claude API or OpenAI API (Render deployment)
- **Messaging**: WhatsApp Business API (Meta)
- **Deployment**: Render.com
- **API Format**: RESTful JSON API + Webhooks

## Features

### Already Implemented (from local_chatbot)
- ✅ Modular OOP architecture
- ✅ Conversation history management (ChatSession)
- ✅ Multi-user session support (ConversationManager)
- ✅ WhatsApp webhook server (Flask)
- ✅ WhatsApp message sending/receiving
- ✅ Command system (/history, /reset, /models, /quit)
- ✅ Terminal display formatting
- ✅ Ngrok tunnel support (for local testing)
- ✅ Health check endpoint
- ✅ Conversation persistence (JSON files)

### Phase 1: Cloud Migration (Render Deployment)
- 🔄 Replace Ollama with cloud LLM API (Anthropic Claude or OpenAI)
- 🔄 Remove ngrok dependency (Render provides public URLs)
- 🔄 Add API key configuration for cloud LLM
- 🔄 Update chatbot_core.py to use cloud API client
- 🔄 Configure environment variables for Render
- 🔄 Deploy Flask webhook server to Render
- 🔄 Test WhatsApp integration with Render public URL

### Phase 2: Cloud Enhancements (Post-Deployment)
- ⏳ Replace JSON file storage with PostgreSQL (Render)
- ⏳ Add Redis for session caching
- ⏳ Implement rate limiting
- ⏳ Add comprehensive logging (structured JSON logs)
- ⏳ Set up monitoring/alerts on Render
- ⏳ Add authentication for non-WhatsApp endpoints
- ⏳ Optimize for Render's free tier (auto-sleep handling)

## Development Plan

### Step 1: Project Setup & Code Migration ✓ (Current Step)
- Copy local_chatbot code to learning_render directory
- Review existing architecture and dependencies
- Update README with migration plan
- Identify cloud vs local dependencies

### Step 2: LLM Provider Migration
- Create new CloudLLMClient class (similar to ChatClient)
- Implement Anthropic Claude API integration
  - Option A: Use Anthropic Python SDK
  - Option B: Use OpenAI API (alternative)
- Update chatbot_core.py to support both Ollama and Cloud clients
- Add cloud API key to environment variables
- Test locally with cloud LLM before Render deployment

### Step 3: Render-Specific Configuration
- Remove ngrok dependency (not needed on Render)
- Update webhook server to work without ngrok
- Configure PORT from environment (Render provides this)
- Update requirements.txt for cloud deployment
- Create render.yaml for automated deployment (optional)
- Update .env.example with cloud LLM credentials

### Step 4: Local Testing with Cloud LLM
- Set up cloud LLM API keys locally
- Test chatbot functionality with cloud API
- Verify WhatsApp webhook works without ngrok (use Render later)
- Ensure conversation persistence still works
- Test all slash commands

### Step 5: Deploy to Render
- Create Render.com account
- Create new Web Service on Render
- Connect GitHub repository or manual deployment
- Configure environment variables:
  - ANTHROPIC_API_KEY or OPENAI_API_KEY
  - META_WA_ACCESS_TOKEN
  - META_WA_PHONE_ID
  - META_WA_WEBHOOK_VERIFY_TOKEN
- Set build and start commands
- Deploy and monitor build logs

### Step 6: WhatsApp Integration on Render
- Get Render public URL
- Update Meta WhatsApp webhook URL to Render endpoint
- Test webhook verification
- Send test WhatsApp message
- Verify end-to-end flow
- Monitor conversation logs

### Step 7: Production Optimization
- Set up persistent storage (upgrade from JSON files)
- Configure Render health checks
- Add error monitoring/logging
- Document production API endpoints
- Plan database migration (Phase 2)

## Project Structure

```
learning_render/
├── README.md                   # This file
├── requirements.txt            # Python dependencies (migrated from local_chatbot)
├── .env.example               # Environment template with cloud LLM keys
├── .gitignore                 # Ignore .env, conversations/, __pycache__
├── run.py                     # Main entry point (adapted for Render)
├── render.yaml                # Optional: Render deployment config
├── src/
│   ├── __init__.py
│   ├── chatbot_core.py        # Core chatbot (MODIFIED for cloud LLM)
│   ├── cloud_llm_client.py    # NEW: Cloud LLM API client
│   ├── commands.py            # Slash commands (unchanged)
│   ├── conversation_manager.py # Session management (unchanged initially)
│   ├── response_handlers.py   # Response formatting (unchanged)
│   ├── terminal_display.py    # Console output (unchanged)
│   ├── whatsapp_handler.py    # WhatsApp API client (unchanged)
│   ├── whatsapp_webhook.py    # Flask webhook server (MODIFIED: remove ngrok)
│   └── main.py                # Mode orchestration (adapted for cloud)
├── conversations/             # Conversation history (gitignored)
└── tests/                     # Future: Unit tests
```

## Setup Instructions

### Prerequisites

1. **Python 3.12+**: Required for Flask application
   - Download from [python.org](https://www.python.org/)
   - Verify installation: `python3 --version`

2. **Git**: For version control and Render deployment
   - Download from [git-scm.com](https://git-scm.com/)
   - Verify installation: `git --version`

3. **Cloud LLM API Key**: Choose one:
   - **Anthropic Claude** (Recommended)
     - Sign up at [console.anthropic.com](https://console.anthropic.com/)
     - Get API key from API Keys section
     - Free tier: $5 credit for testing
   - **OpenAI** (Alternative)
     - Sign up at [platform.openai.com](https://platform.openai.com/)
     - Get API key from API section

4. **WhatsApp Business API** (Optional for Phase 1):
   - Set up at [developers.facebook.com](https://developers.facebook.com/)
   - See original local_chatbot/WHATSAPP_SETUP.md for details
   - Can skip initially and use direct API testing

5. **Render Account**: Sign up at [render.com](https://render.com/)
   - Free tier available (750 hours/month)
   - GitHub/GitLab integration recommended

### Local Development Setup

1. **Copy local_chatbot code**
   ```bash
   cd /Users/ogeiger/git/learning_render

   # Copy source files from local_chatbot
   cp -r /Users/ogeiger/git/local_chatbot/src ./
   cp /Users/ogeiger/git/local_chatbot/run.py ./
   cp /Users/ogeiger/git/local_chatbot/requirements.txt ./
   cp /Users/ogeiger/git/local_chatbot/.gitignore ./
   cp /Users/ogeiger/git/local_chatbot/.env.example ./

   # Create conversations directory
   mkdir -p conversations
   ```

2. **Set up Python virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

   # Add cloud LLM SDK (choose one or both)
   pip install anthropic        # For Claude
   pip install openai          # For OpenAI
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your credentials:
   ```bash
   # Cloud LLM (choose one)
   ANTHROPIC_API_KEY=your_anthropic_key_here
   # or
   OPENAI_API_KEY=your_openai_key_here

   # WhatsApp (optional for initial testing)
   META_WA_ACCESS_TOKEN=your_token
   META_WA_PHONE_ID=your_phone_id
   META_WA_WEBHOOK_VERIFY_TOKEN=your_verify_token

   # Server config (Render sets PORT automatically)
   WEBHOOK_HOST=0.0.0.0
   WEBHOOK_PORT=8000
   ```

5. **Update chatbot_core.py for cloud LLM**
   - Create src/cloud_llm_client.py (Step 2 of Development Plan)
   - Modify chatbot_core.py to use CloudLLMClient
   - See implementation guide below

6. **Test locally with cloud LLM**
   ```bash
   # Terminal mode (after cloud LLM implementation)
   python3 run.py

   # Webhook server mode
   python3 run.py --whatsapp-server
   ```

7. **Test endpoints manually**
   ```bash
   # Health check
   curl http://localhost:8000/health

   # Webhook verification (simulating Meta's verification)
   curl "http://localhost:8000/webhook?hub.mode=subscribe&hub.verify_token=your_verify_token&hub.challenge=test123"
   ```

### Deployment to Render.com

#### Option A: GitHub Integration (Recommended)

1. **Initialize Git repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Migrated local_chatbot to Render with cloud LLM"
   ```

2. **Create GitHub repository and push**
   ```bash
   # Create repo on GitHub first, then:
   git remote add origin <your-github-repo-url>
   git branch -M main
   git push -u origin main
   ```

3. **Create Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: `chatbot-render` (or your choice)
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python run.py --whatsapp-server`
     - **Plan**: `Free` tier

4. **Set environment variables in Render**
   - In the Render dashboard, go to "Environment" tab
   - Add the following variables:
     ```
     ANTHROPIC_API_KEY=your_actual_api_key
     META_WA_ACCESS_TOKEN=your_whatsapp_token
     META_WA_PHONE_ID=your_phone_id
     META_WA_WEBHOOK_VERIFY_TOKEN=your_verify_token
     WEBHOOK_HOST=0.0.0.0
     ```
   - Note: `PORT` is automatically set by Render (don't add it)

5. **Update run.py for Render**
   - Ensure server reads PORT from environment
   - Remove ngrok tunnel initialization
   - See code modifications below

6. **Deploy**
   - Render automatically deploys on push to main
   - Monitor build logs in dashboard
   - Wait for "Live" status
   - Get your public URL: `https://chatbot-render.onrender.com`

#### Option B: Manual Deployment (Not Recommended)

- Use GitHub integration for easier updates and CI/CD

### Testing the Deployed Service

```bash
# Health check
curl https://chatbot-render.onrender.com/health

# Webhook verification (Meta will call this during setup)
curl "https://chatbot-render.onrender.com/webhook?hub.mode=subscribe&hub.verify_token=your_verify_token&hub.challenge=test123"

# For WhatsApp testing:
# 1. Configure webhook URL in Meta Developer Console
# 2. Set webhook URL to: https://chatbot-render.onrender.com/webhook
# 3. Send a WhatsApp message to your test number
# 4. Check Render logs to see message processing
```

### Configure WhatsApp Webhook on Meta

1. Go to [Meta Developer Console](https://developers.facebook.com/)
2. Select your app → WhatsApp → Configuration
3. Update webhook URL:
   - **Callback URL**: `https://chatbot-render.onrender.com/webhook`
   - **Verify Token**: (same as META_WA_WEBHOOK_VERIFY_TOKEN in Render env)
4. Subscribe to webhook fields: `messages`
5. Test by sending a WhatsApp message to your business number

## API Documentation

### Endpoints

#### GET /health
Health check endpoint to verify server is running.

**Response**:
```json
{
  "status": "healthy"
}
```

#### GET /webhook
WhatsApp webhook verification endpoint (called by Meta during setup).

**Query Parameters**:
- `hub.mode`: Should be "subscribe"
- `hub.verify_token`: Must match META_WA_WEBHOOK_VERIFY_TOKEN
- `hub.challenge`: Random string to echo back

**Response**: Returns the challenge value if verification succeeds

#### POST /webhook
WhatsApp webhook endpoint for receiving messages.

**Request Body** (from Meta):
```json
{
  "entry": [
    {
      "changes": [
        {
          "value": {
            "messages": [
              {
                "from": "1234567890",
                "type": "text",
                "text": {
                  "body": "Hello, bot!"
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

**Response**:
```json
{
  "status": "ok"
}
```

**Behavior**:
1. Receives message from WhatsApp user
2. Retrieves or creates conversation session for user
3. Sends message to cloud LLM (Anthropic Claude)
4. Saves conversation to disk
5. Sends response back to user via WhatsApp API

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| PORT | Server port | 8000 | No (Render sets automatically) |
| ANTHROPIC_API_KEY | Anthropic Claude API key | - | Yes (cloud LLM) |
| OPENAI_API_KEY | OpenAI API key (alternative to Anthropic) | - | No |
| META_WA_ACCESS_TOKEN | WhatsApp Business API access token | - | Yes (for WhatsApp) |
| META_WA_PHONE_ID | WhatsApp phone number ID | - | Yes (for WhatsApp) |
| META_WA_WEBHOOK_VERIFY_TOKEN | Webhook verification secret | - | Yes (for WhatsApp) |
| WEBHOOK_HOST | Host to bind server | 0.0.0.0 | No |
| WEBHOOK_PORT | Port (overridden by PORT on Render) | 8000 | No |

## Key Code Modifications for Cloud Deployment

### 1. Create src/cloud_llm_client.py

New file to abstract cloud LLM APIs:

```python
"""Cloud LLM Client for Anthropic Claude or OpenAI."""
import os
from anthropic import Anthropic

class CloudLLMClient:
    def __init__(self, provider="anthropic", model=None):
        self.provider = provider

        if provider == "anthropic":
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = model or "claude-3-5-sonnet-20241022"
        # Add OpenAI support later if needed

    def send_message(self, messages, stream=False):
        """Send messages to cloud LLM (compatible with Ollama interface)."""
        # Convert format and call Anthropic API
        # Implementation details in Step 2
        pass
```

### 2. Update src/whatsapp_webhook.py

Remove ngrok dependency:

```python
def run(self, host='0.0.0.0', port=8000, use_ngrok=False):
    # On Render, use_ngrok should always be False
    # Port comes from os.getenv('PORT', 8000)
    port = int(os.getenv('PORT', port))
    # Remove all ngrok code
    self.app.run(host=host, port=port, debug=False)
```

### 3. Update run.py

Ensure proper port configuration:

```python
# In main_whatsapp_server function
port = int(os.getenv('PORT', 8000))
server.run(host='0.0.0.0', port=port, use_ngrok=False)
```

## Common Issues & Troubleshooting

### Local Development

- **Ollama replaced**: This version uses cloud LLM, not local Ollama
- **API key errors**: Ensure ANTHROPIC_API_KEY is set in .env
- **Import errors**: Run `pip install anthropic` or `pip install openai`
- **Port already in use**: Change WEBHOOK_PORT in .env

### Render Deployment

- **Build fails**:
  - Check requirements.txt includes all dependencies
  - Ensure Python 3.12+ is specified
  - Check build logs for missing packages

- **Server won't start**:
  - Verify start command: `python run.py --whatsapp-server`
  - Check environment variables are set correctly
  - Look for errors in Render logs

- **502 Bad Gateway / Service Unavailable**:
  - Free tier spins down after 15 min inactivity
  - First request takes 30-60s to wake up
  - This is normal behavior on free tier

- **WhatsApp webhook verification fails**:
  - Ensure META_WA_WEBHOOK_VERIFY_TOKEN matches in both Render and Meta Console
  - Check webhook URL is exact: `https://yourapp.onrender.com/webhook`
  - Verify GET endpoint is working: test with curl

- **Messages not processing**:
  - Check Render logs for incoming webhook POSTs
  - Verify ANTHROPIC_API_KEY is valid and has credits
  - Check conversation files are being created (may need persistent disk)

- **Conversation persistence issues**:
  - Render's free tier has ephemeral storage
  - Files in conversations/ directory may be lost on restart
  - Solution: Upgrade to Phase 2 (PostgreSQL database)

## Free Tier Limitations (Render)

- Service spins down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- 750 hours/month free tier limit
- Good for learning and development, consider paid tier for production

## Migration Summary: Local vs Cloud

| Aspect | Local (local_chatbot) | Cloud (learning_render) |
|--------|----------------------|-------------------------|
| **LLM** | Ollama (local models) | Anthropic Claude API |
| **Deployment** | Local machine | Render.com (cloud) |
| **Public Access** | ngrok tunnel | Render public URL |
| **Storage** | JSON files (persistent) | JSON files (ephemeral*) |
| **Startup** | Manual (`python run.py`) | Auto-deployed on git push |
| **Cost** | Free (local compute) | Free tier (750 hrs/mo) + API costs |
| **Dependencies** | Ollama + Python | Python + Cloud API SDK |

*Note: Render free tier has ephemeral storage. Conversations may be lost on restart. Upgrade to PostgreSQL in Phase 2 for persistence.

## Next Steps After Deployment

### Immediate (Phase 1)
1. ✅ Deploy to Render successfully
2. ✅ Verify health check endpoint
3. ✅ Test WhatsApp webhook verification
4. ✅ Send test WhatsApp message end-to-end
5. ✅ Monitor Render logs for conversation flow

### Short-term (Phase 2)
1. 🔄 Add PostgreSQL database for conversation persistence
2. 🔄 Implement Redis caching for sessions
3. 🔄 Add structured logging (JSON logs)
4. 🔄 Set up monitoring/alerts
5. 🔄 Implement rate limiting per user

### Long-term (Future)
1. 📊 Analytics dashboard for conversation metrics
2. 🤖 Support multiple LLM providers (Claude, GPT-4, etc.)
3. 🎨 Add rich media support (images, documents)
4. 🔒 Add API authentication for direct API access
5. 🌍 Multi-language support
6. 📱 Build web interface for testing (non-WhatsApp)

## Resources

### Deployment & Hosting
- [Render Documentation](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/deploy-flask)
- [Render Environment Variables](https://render.com/docs/environment-variables)

### Cloud LLM APIs
- [Anthropic Claude API Docs](https://docs.anthropic.com/)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [OpenAI API Docs](https://platform.openai.com/docs/)

### WhatsApp Business API
- [Meta WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [WhatsApp Webhooks Guide](https://developers.facebook.com/docs/whatsapp/webhooks)
- [Original WHATSAPP_SETUP.md](https://github.com/yourusername/local_chatbot/blob/main/WHATSAPP_SETUP.md)

### Python & Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Best Practices](https://flask.palletsprojects.com/en/stable/patterns/)
- [Python Logging Guide](https://docs.python.org/3/howto/logging.html)

## Implementation Guide: Cloud LLM Client

The key to migrating from Ollama to cloud LLM is creating a compatible interface. Here's the strategy:

### Original Ollama Interface
```python
# chatbot_core.py - ChatClient
response = ollama.chat(model=self.model, messages=messages, stream=stream)
```

### New Cloud LLM Interface (compatible)
```python
# cloud_llm_client.py
class CloudLLMClient:
    def send_message(self, messages, stream=False):
        # Convert Ollama message format to Anthropic format
        # Call Anthropic API
        # Return response in same format as Ollama
```

### Strategy
1. Keep ChatSession and message format unchanged
2. Create CloudLLMClient that mimics Ollama's chat() interface
3. Update chatbot_core.py to accept CloudLLMClient OR ChatClient
4. Handle streaming vs non-streaming responses identically

This allows minimal changes to existing code while swapping the LLM provider.

## License

MIT License - Feel free to use this for your own learning projects.

## Contributing

This is a learning project. Feedback and suggestions welcome!

---

**Status**: 📝 Planning Complete → **Next: Copy files and implement cloud LLM client**

**Original Source**: `/Users/ogeiger/git/local_chatbot`
**Target Deployment**: Render.com with Anthropic Claude API
