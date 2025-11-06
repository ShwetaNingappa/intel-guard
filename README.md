# IP Threat Aggregator with AI Analyst 🛡️

A full-stack **cybersecurity dashboard** that aggregates threat intelligence from **6 external APIs** and uses **Google Gemini AI** to generate comprehensive threat scores and identify related cyber campaigns.

## 🎯 Features

- **Multi-Source Intelligence**: Aggregates data from 6 different threat intelligence APIs concurrently
- **AI-Powered Analysis**: Uses Google Gemini 2.0 to synthesize findings and generate threat scores (0-100)
- **Threat Campaign Intelligence**: AI identifies related APT groups, campaigns, and security news
- **Dark Mode UI**: Professional cybersecurity-themed dashboard with stunning visualizations
- **Real-Time Analysis**: Interactive charts and detailed breakdowns using Recharts
- **IP Reporting**: Submit malicious IPs directly to AbuseIPDB

## 🏗️ Architecture

### Backend (FastAPI + Python)
- **Concurrent API Calls**: Uses `asyncio.gather()` to query 6 APIs simultaneously
- **Data Normalization**: Unified report structure for AI analysis
- **AI Scoring Engine**: Gemini AI analyzes consensus and generates threat scores + campaign intelligence
- **RESTful API**: FastAPI with automatic OpenAPI documentation

### Frontend (React + Vite)
- **Dark Mode Theme**: Professional cybersecurity dashboard aesthetic
- **Component-Based**: Modular React components for maintainability
- **Chakra UI**: Beautiful, accessible design system
- **Data Visualization**: Recharts for threat metrics

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- API Keys for:
  - AbuseIPDB
  - VirusTotal
  - IP-API (free tier, no key needed)
  - IPStack
  - WhoisXML
  - SecurityTrails
  - Google Gemini AI

## 🚀 Quick Start

### 1. Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env

# Edit .env and add your API keys
notepad .env
```

### 2. Configure API Keys

Edit `backend/.env` and add your API keys:

```env
ABUSEIPDB_KEY=your_key_here
VIRUSTOTAL_KEY=your_key_here
IPAPI_KEY=your_key_here
IPSTACK_KEY=your_key_here
WHOISXML_KEY=your_key_here
SECURITYTRAILS_KEY=your_key_here
GEMINI_API_KEY=your_gemini_key_here
NEWS_API_KEY=your_newsapi_key_here
```

### 3. Start Backend Server

```powershell
# From backend directory
python -m app.main

# Or use uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### 4. Frontend Setup

```powershell
# Navigate to frontend directory (new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## 📡 API Endpoints

### Check IP Threat Intelligence
```
GET /api/v1/check-ip/{ip_address}
```

**Process Flow:**
1. Concurrent data collection from 6 APIs
2. Data normalization into unified structure
3. Gemini AI analysis (threat score + related campaigns)
4. Final response with score, rationale, and campaign news

**Response:**
```json
{
  "ip_address": "8.8.8.8",
  "final_threat_score": 15,
  "ai_rationale": "Detailed AI analysis...",
  "related_campaign_news": [
    "Campaign 1 description",
    "Campaign 2 description",
    "Campaign 3 description"
  ],
  "reputation": { ... },
  "geolocation": { ... },
  "ownership": { ... },
  "raw_data": { ... }
}
```

### Report IP to AbuseIPDB
```
POST /api/v1/report-ip
```

**Request Body:**
```json
{
  "ip": "192.168.1.1",
  "categories": [14, 15, 18],
  "comment": "Detailed abuse description"
}
```

## 🧠 AI Threat Scoring Logic

The Gemini AI Analyst follows this scoring methodology:

- **CRITICAL (75-100)**: Strong consensus across sources, recent abuse reports, suspicious ownership
- **HIGH (50-74)**: Multiple concerning indicators, moderate consensus
- **MEDIUM (25-49)**: Mixed signals, some concerns but not definitive
- **LOW (0-24)**: Clean reports across sources, legitimate organization

### Key Analysis Factors:
1. AbuseIPDB confidence score and report volume
2. VirusTotal detection ratio
3. Geolocation and hosting type (cloud vs. bulletproof)
4. WHOIS ownership legitimacy
5. Historical activity patterns
6. Cross-source consensus/discrepancies
7. **Related threat campaigns and APT groups**

## 📊 Data Sources (6 APIs)

| API | Purpose | Data Provided |
|-----|---------|---------------|
| AbuseIPDB | Reputation | Abuse reports, confidence score |
| VirusTotal | Security | Malware detections, threat votes |
| IP-API | Geolocation | Country, ISP, hosting flag |
| IPStack | Geolocation | Detailed location, ISP |
| WhoisXML | Ownership | Registrar, organization, contacts |
| SecurityTrails | Historical | IP history, domain associations |

## 🎨 Frontend Components

### 🆕 Key Features:
- **Dark Mode Theme**: Professional cybersecurity aesthetic with gray.900 background
- **ThreatScore**: Large, prominent score display with AI rationale
- **NewsCampaigns**: Displays related threat intelligence news and campaigns (NEW!)
- **DetectionChart**: Bar chart for VirusTotal detection breakdown
- **DataPanel**: Accordion view for reputation, geolocation, and ownership
- **ReportIPForm**: Form to submit abuse reports to AbuseIPDB

### Color Scheme:
- Background: `gray.900` (dark)
- Cards: `gray.800`
- Accents: `blue.400`, `cyan.400`, `orange.500`
- Critical alerts: `red.500`

## 🆕 News/Campaigns Feature

The application now uses Gemini AI to identify **related cyber campaigns, APT groups, and security news** based on:
- IP's ISP and ASN
- Organization ownership patterns
- Abuse categories detected
- Known threat intelligence patterns

This provides context about:
- Active APT campaigns using similar infrastructure
- Recent security incidents involving the IP range
- Known botnets or malware families
- Historical threat campaigns

## 🔧 Development

### Backend Development
```powershell
# Run with auto-reload
uvicorn app.main:app --reload

# Run tests (if implemented)
pytest
```

### Frontend Development
```powershell
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📦 Project Structure

```
ip-threat-aggregator/
├── backend/
│   ├── app/
│   │   ├── api/           # API route handlers
│   │   ├── core/          # Configuration
│   │   ├── models/        # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   │   ├── threat_apis.py      # 6 API clients
│   │   │   ├── normalizer.py       # Data normalization
│   │   │   └── gemini_analyzer.py  # AI scoring + news
│   │   └── main.py        # FastAPI app
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── NewsCampaigns.jsx  # NEW!
│   │   │   ├── ThreatScore.jsx
│   │   │   ├── DetectionChart.jsx
│   │   │   ├── DataPanel.jsx
│   │   │   └── ReportIPForm.jsx
│   │   ├── services/      # API communication
│   │   ├── types/         # Type definitions
│   │   ├── App.jsx        # Main app (dark mode)
│   │   └── main.jsx       # Entry point
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🐛 Troubleshooting

### Backend Issues

**API Key Errors:**
- Verify all keys are correctly set in `.env`
- Check API key quotas and rate limits

**Import Errors:**
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

### Frontend Issues

**Module Not Found:**
- Delete `node_modules` and run `npm install`
- Clear cache: `npm cache clean --force`

**CORS Errors:**
- Verify backend CORS settings in `app/main.py`
- Check frontend proxy configuration in `vite.config.js`

## 🔒 Security Notes

- Never commit `.env` files with real API keys
- Use environment variables in production
- Implement rate limiting for production deployments
- Validate and sanitize all IP address inputs

## 📝 What's New in This Version

✅ **Reduced to 6 APIs** (removed Risk/Blocklist API)
✅ **News/Campaigns Feature** - AI identifies related threats
✅ **Dark Mode Theme** - Professional cybersecurity dashboard
✅ **Enhanced UI** - Better visualizations and layout
✅ **Improved AI Prompts** - More accurate threat assessment

## 📧 Support

For issues or questions, please refer to the API documentation at `http://localhost:8000/docs` when the backend is running.

---

**Built with ❤️ for the cybersecurity community**
