# Learning Render - Flask Server with WhatsApp Integration

A minimal Flask server deployed on Render.com with WhatsApp Business API integration for learning cloud deployment and webhook handling.

## 🚀 Live Server

**Production URL:** https://learning-render-ut2u.onrender.com

**Endpoints:**
- `GET /status` - Health check
- `POST /write` - Echo endpoint
- `GET /webhook` - WhatsApp webhook verification
- `POST /webhook` - WhatsApp message receiver

## 📋 Common Procedures

### Gather WhatsApp Credentials from Meta

**Purpose:** Get API credentials needed for WhatsApp integration.

**You need three credentials:**

1. **META_WA_PHONE_ID** - Your WhatsApp Business phone number ID
2. **META_WA_ACCESS_TOKEN** - API access token
3. **META_WA_VERIFY_TOKEN** - Webhook verification secret (you create this)

---

#### Step 1: Access Meta Developer Console

1. Go to: https://developers.facebook.com/apps
2. Sign in with your Meta/Facebook account
3. Select your WhatsApp Business app (or create one if needed)

---

#### Step 2: Get Phone Number ID

1. In left sidebar: **WhatsApp** → **API Setup** (or **Getting Started**)
2. Look for **"Phone number ID"** section
3. Copy the number (example: `1034072156454424`)
4. Save as: `META_WA_PHONE_ID=1034072156454424`

---

#### Step 3: Get Access Token

**Temporary Token (for testing - expires in 24 hours):**

1. Same page as above (**API Setup**)
2. Find **"Temporary access token"** section
3. Click **"Copy"** or select the token text
4. Token starts with `EAA...`
5. Save as: `META_WA_ACCESS_TOKEN=EAAxxxxxxxxxxxxx`

**Permanent Token (for production):**

1. Go to **Settings** → **Basic**
2. Copy your **App ID** and **App Secret**
3. Generate a User Access Token via Graph API Explorer
4. Exchange for long-lived token using:
   ```
   https://graph.facebook.com/oauth/access_token?
   grant_type=fb_exchange_token&
   client_id={app-id}&
   client_secret={app-secret}&
   fb_exchange_token={short-lived-token}
   ```
5. Use Graph API Explorer or follow Meta's documentation for system user tokens

**For learning:** Use the temporary token. It's simpler.

---

#### Step 4: Create Verify Token

**This is NOT from Meta - you create it yourself.**

1. Choose a random, secure string (like a password)
2. Example: `my_secret_webhook_verify_token_12345`
3. Save as: `META_WA_VERIFY_TOKEN=my_secret_webhook_verify_token_12345`

**Important:**
- Remember this token - you'll enter it in Meta Console later
- Keep it secret (don't commit to GitHub)
- Use letters, numbers, and special characters

---

#### Step 5: Verify You Have All Three

You should now have:

```bash
META_WA_PHONE_ID=1034072156454424
META_WA_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxx
META_WA_VERIFY_TOKEN=my_secret_webhook_verify_token_12345
```

**Next:** Add these to your `.env` file (local) or Render environment variables (production).

---

### Deploy Updates to Render

**When you make code changes and want to deploy:**

1. **Commit changes locally:**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

2. **Push to GitHub:**
   ```bash
   git push origin main
   ```

3. **Render auto-deploys:**
   - Go to Render Dashboard
   - Your service will show "Deploying..."
   - Wait for "Live" status (1-3 minutes)
   - Check logs for any errors

---

### Add Environment Variables to Render

**When you need to add secrets/config to production:**

1. Go to: https://dashboard.render.com
2. Select your service: **learning-render-ut2u**
3. Click **"Environment"** tab (left sidebar)
4. Click **"Add Environment Variable"**
5. Enter:
   - **Key:** `META_WA_ACCESS_TOKEN`
   - **Value:** `EAAxxxxxxxxxxxxx`
6. Click **"Save Changes"**
7. Repeat for each variable
8. Service will auto-restart with new variables

**Important:** Never commit secrets to Git! Only use environment variables.

---

### Test Server Health

**Run remote server health tests:**

```bash
python tests/test_remote_server.py
```

**Run local server tests:**

```bash
# Start server first in one terminal
python app.py

# Run tests in another terminal
python tests/test_local_server.py
```

**Expected output:**
- All tests show ✅
- Final message: "🎉 ALL TESTS PASSED!"

**If tests fail:**
- Check Render logs for errors (remote)
- Verify server is running (local)
- Check environment variables are set correctly

---

### View Render Logs

**When debugging issues:**

1. Go to Render Dashboard
2. Select your service
3. Click **"Logs"** tab
4. View real-time logs
5. Look for errors, warnings, or request logs

**Useful log commands:**
- Filter by time period
- Search for specific text
- Download logs for offline analysis

---

### Configure WhatsApp Webhook

**After deploying webhook endpoints:**

1. Go to: https://developers.facebook.com/apps
2. Select your app → **WhatsApp** → **Configuration**
3. Find **"Webhook"** section
4. Click **"Edit"**
5. Enter:
   - **Callback URL:** `https://learning-render-ut2u.onrender.com/webhook`
   - **Verify Token:** (the token you created in META_WA_VERIFY_TOKEN)
6. Click **"Verify and Save"**
7. Subscribe to **"messages"** webhook field
8. Click **"Save"**

**If verification fails:**
- Check Render logs for incoming GET request
- Verify VERIFY_TOKEN matches exactly
- Ensure GET /webhook endpoint is working

---

### Test WhatsApp Integration

**End-to-end test:**

1. Get your test phone number from Meta Console
   - **WhatsApp** → **API Setup**
   - Look for test number (e.g., +1 555-0100)

2. Add your personal phone as a recipient:
   - Click **"Add phone number"**
   - Verify with SMS code

3. Send a test message:
   - Use WhatsApp on your phone
   - Send message to the test number
   - You should receive an echo response

4. Check Render logs:
   - See incoming webhook POST
   - See message processing
   - See outgoing API call to WhatsApp

---

## 🛠️ Local Development

### Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials
```

### Run Locally

```bash
# Activate virtual environment
source .venv/bin/activate

# Run server
python app.py
```

Server runs at: http://localhost:5000

### Test Locally

```bash
# Health check
curl http://localhost:5000/status

# Echo test
curl -X POST http://localhost:5000/write \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello!"}'
```

---

## 📁 Project Structure

```
learning_render/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── .env                      # Local environment variables (gitignored)
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
├── README.md                # This file (main documentation)
│
├── tests/                   # Test scripts
│   ├── test_local_server.py  # Local server tests
│   └── test_remote_server.py # Remote server health tests
│
└── docs/                    # Documentation
    ├── learn_render.md       # Render deployment tutorial
    └── full_app_plan.md      # Full chatbot migration plan
```

---

## 🔒 Environment Variables

### Required for WhatsApp

| Variable | Description | Example |
|----------|-------------|---------|
| `META_WA_PHONE_ID` | WhatsApp phone number ID | `1034072156454424` |
| `META_WA_ACCESS_TOKEN` | Meta API access token | `EAAxxxxxxxxx` |
| `META_WA_VERIFY_TOKEN` | Webhook verification secret | `my_secret_token` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `5000` (Render sets this) |

---

## 🧪 Testing

### Remote Server Health Test

```bash
python tests/test_remote_server.py
```

Tests:
- ✅ GET /status endpoint
- ✅ POST /write endpoint (echo functionality)
- ✅ Error handling (invalid requests)
- ✅ GET /webhook verification (success & failure)

### Local Server Test

```bash
# Start server first
python app.py

# In another terminal
python tests/test_local_server.py
```

Tests:
- ✅ GET /status endpoint
- ✅ POST /write endpoint
- ✅ GET /webhook verification (success)
- ✅ GET /webhook verification (failure)

### Manual Testing

```bash
# Production
curl https://learning-render-ut2u.onrender.com/status

# Local
curl http://localhost:5000/status
```

---

## 📚 Resources

- [Render Documentation](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Meta WhatsApp API Docs](https://developers.facebook.com/docs/whatsapp)
- [WhatsApp Cloud API Guide](https://developers.facebook.com/docs/whatsapp/cloud-api)

---

## 🐛 Troubleshooting

### Server won't start on Render
- Check build logs for Python/pip errors
- Verify `requirements.txt` is correct
- Check start command: `python app.py`

### WhatsApp webhook verification fails
- Verify token must match exactly (case-sensitive)
- Check Render logs for incoming GET request
- Ensure GET /webhook endpoint returns the challenge

### Messages not echoing
- Check Render logs for POST /webhook requests
- Verify access token is valid (not expired)
- Check phone number ID is correct
- Ensure webhook is subscribed to "messages"

### 502 Bad Gateway on Render
- Normal after 15 min inactivity (free tier)
- Server spins down to save resources
- Wait 30-60 seconds for wake-up
- First request after sleep is slower

---

## 📝 License

MIT License - Free to use for learning and personal projects.

---

**Status:** ✅ Deployed and operational
**Last Updated:** 2026-03-08
