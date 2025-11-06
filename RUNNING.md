# 🚀 Application Running - Quick Reference

## ✅ Current Status

Both servers have been started in separate PowerShell windows:

### Backend Server (FastAPI)
- **Status**: Starting... ⏳
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Window**: Check separate PowerShell window for logs
- **Expected startup time**: 10-15 seconds

### Frontend Server (React + Vite)
- **Status**: Starting... ⏳
- **URL**: http://localhost:5173
- **Window**: Check separate PowerShell window for logs
- **Expected startup time**: 5-10 seconds

---

## 📍 Access the Application

Once both servers are running (check the PowerShell windows for "Application startup complete"):

1. **Open your web browser**
2. **Navigate to**: http://localhost:5173
3. **Start analyzing IPs!**

---

## 🔍 Verify Servers Are Running

### Check Backend:
```powershell
curl http://localhost:8000
# Should return: {"status":"online","service":"IP Threat Aggregator API","version":"1.0.0"}
```

### Check Frontend:
Open http://localhost:5173 in your browser
- You should see the dark-themed IP Threat Aggregator dashboard

---

## 📊 Test the Application

### Example IPs to Test:

1. **Safe IP (Google DNS)**:
   - IP: `8.8.8.8`
   - Expected: Low threat score (0-30)
   - Source: Google LLC

2. **Safe IP (Cloudflare)**:
   - IP: `1.1.1.1`
   - Expected: Low threat score (0-30)
   - Source: Cloudflare

3. **Your Public IP**:
   - Find your IP: https://whatismyipaddress.com
   - Check your own IP's reputation

### What to Expect:

**Analysis Time**: 5-15 seconds
- Calling 8 external APIs concurrently
- AI analysis with Gemini
- News article searching

**Results Display**:
1. ✅ **Threat Score** (0-100) with color coding
2. ✅ **AI Rationale** explaining the score
3. ✅ **Related Threat Campaigns** (AI-generated)
4. ✅ **News Articles** (from News API)
5. ✅ **Detection Charts** (VirusTotal data)
6. ✅ **Detailed Data** (Geolocation, Ownership, Reputation)

---

## 🎯 Features to Try

### 1. IP Analysis
- Enter any IPv4 address
- Click "Analyze IP"
- Review comprehensive threat intelligence

### 2. View News Articles
- Check the blue-bordered "Related Security News" section
- Click article links to read full stories
- See how news correlates with threat data

### 3. OTX Pulse Data
- Open "Reputation Intelligence" accordion
- See OTX pulse count (critical indicator)
- High count (>10) = likely malicious

### 4. Report Malicious IP
- Click "Report IP" tab
- Fill out form with categories and comment
- Submit to AbuseIPDB

### 5. View Raw Data
- Click "Raw Data" tab
- See all 8 API responses
- Useful for debugging or detailed analysis

---

## 🖥️ Server Logs

Both servers are running in separate PowerShell windows. Check them for:

### Backend Logs Show:
```
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Frontend Logs Show:
```
  VITE v5.0.11  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

---

## 🛑 Stop the Servers

To stop the application:

1. **Find the two PowerShell windows**
2. **Press `Ctrl + C`** in each window
3. **Or close the windows**

---

## 🔄 Restart the Servers

If you need to restart:

```powershell
# From the hackathon directory
.\start.ps1
```

Or manually:

### Backend:
```powershell
cd backend
.\venv\Scripts\Activate
python -m app.main
```

### Frontend:
```powershell
cd frontend
npm run dev
```

---

## 📋 API Endpoints Available

### Main Endpoint:
```
GET /api/v1/check-ip/{ip_address}
```
Example: http://localhost:8000/api/v1/check-ip/8.8.8.8

### Report Endpoint:
```
POST /api/v1/report-ip
Body: {"ip": "...", "categories": [...], "comment": "..."}
```

### Health Check:
```
GET /
```
Example: http://localhost:8000/

---

## 🔑 API Keys Status

All 8 API keys are configured in `backend\.env`:
- ✅ Gemini AI
- ✅ AbuseIPDB
- ✅ OTX (AlienVault)
- ✅ IPinfo
- ✅ IPstack
- ✅ IP-API
- ✅ SecurityTrails
- ✅ WhoisXML
- ✅ News API

**Note**: These are real API keys. Monitor your usage to stay within free tier limits.

---

## 💡 Tips for Best Experience

1. **Wait for full startup**: Backend needs 10-15 seconds to initialize all services
2. **Use Chrome/Firefox**: Best compatibility with Chakra UI
3. **Dark mode**: Application uses dark theme by default
4. **Network required**: All 8 APIs require internet connection
5. **Rate limits**: Be aware of free tier limits (especially News API: 100 req/day)

---

## 🐛 Troubleshooting

### Backend won't start:
- Check if port 8000 is already in use
- Verify `.env` file exists in backend folder
- Check Python virtual environment is activated

### Frontend won't start:
- Check if port 5173 is already in use
- Verify `node_modules` folder exists
- Run `npm install` again if needed

### API returns errors:
- Check API keys in `.env` are correct
- Verify internet connection
- Check API rate limits haven't been exceeded

### CORS errors:
- Backend CORS is configured for localhost:5173
- If using different port, update `main.py`

---

## 📚 Additional Documentation

- **Full README**: `README.md`
- **API Integration Details**: `API_INTEGRATION.md`
- **Feature Showcase**: `FEATURES.md`
- **Changelog**: `CHANGELOG.md`

---

**Enjoy analyzing IP threats with AI-powered intelligence!** 🛡️

**Version**: 3.0  
**Status**: ✅ Running  
**Last Updated**: 2025-11-06
