# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Run Setup Script
```powershell
.\setup.ps1
```
This will:
- Check Python and Node.js installations
- Create Python virtual environment
- Install all dependencies
- Create `.env` template

### Step 2: Add API Keys
Edit `backend\.env` and add your API keys:
```env
ABUSEIPDB_KEY=your_actual_key
VIRUSTOTAL_KEY=your_actual_key
GEMINI_API_KEY=your_actual_key
# ... add all keys
```

### Step 3: Start Servers
```powershell
.\start.ps1
```
This opens two new windows:
- Backend server on port 8000
- Frontend server on port 5173

### Step 4: Use the App
Open browser to: **http://localhost:5173**

Enter an IP address (e.g., `8.8.8.8`) and click "Analyze IP"

## 📝 API Keys You Need

### Free Tier Available:
1. **AbuseIPDB** - https://www.abuseipdb.com/api
2. **VirusTotal** - https://www.virustotal.com/gui/join-us
3. **IP-API** - http://ip-api.com (no key needed for basic)
4. **IPStack** - https://ipstack.com/signup/free
5. **Google Gemini** - https://makersuite.google.com/app/apikey

### Paid/Trial:
6. **WhoisXML** - https://whoisxmlapi.com
7. **SecurityTrails** - https://securitytrails.com

**Note:** Version 2.0 uses 6 threat intelligence APIs (Risk API removed)

## 🔍 Test the API

### Check IP via API:
```powershell
curl http://localhost:8000/api/v1/check-ip/8.8.8.8
```

### View API Documentation:
http://localhost:8000/docs

## ⚡ Common Commands

### Start Backend Only:
```powershell
cd backend
.\venv\Scripts\Activate
python -m app.main
```

### Start Frontend Only:
```powershell
cd frontend
npm run dev
```

### Restart After Code Changes:
- Backend: Just save file (auto-reload enabled)
- Frontend: Just save file (hot module replacement)

## 🐛 Quick Troubleshooting

**"Module not found" error:**
```powershell
cd backend
.\venv\Scripts\Activate
pip install -r requirements.txt
```

**Frontend won't start:**
```powershell
cd frontend
rm -r node_modules
npm install
```

**API returns 500 error:**
- Check that all API keys are valid in `.env`
- Check backend console for specific error messages

## 📊 Example Test IPs

Try these IPs to see different threat levels:

- **Safe**: `8.8.8.8` (Google DNS)
- **Safe**: `1.1.1.1` (Cloudflare DNS)
- **Test with caution**: Look up known malicious IPs on AbuseIPDB

## 🎯 What to Expect

1. **Analysis takes 5-15 seconds** - We're calling 6 APIs + Gemini AI
2. **Threat score**: 0-100 (AI-generated based on all sources)
3. **AI rationale**: Detailed explanation of the score
4. **Related campaigns**: AI-identified threat intelligence news
5. **Charts**: VirusTotal detection breakdown
6. **Details**: Geolocation, ownership, abuse reports
7. **Dark mode**: Professional cybersecurity dashboard theme

## 📖 Next Steps

- Read full README.md for architecture details
- Explore API documentation at http://localhost:8000/docs
- Customize AI prompt in `backend/app/services/gemini_analyzer.py`
- Modify frontend styling in React components

---

**Need Help?** Check the main README.md or API documentation
