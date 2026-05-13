# 🛡️ Threat Intelligence Correlation Engine (TICE)

**AI-Driven Multi-Source Threat Analysis & Attribution**

A comprehensive threat intelligence platform that aggregates and analyzes IP address data from multiple security sources to provide unified threat intelligence reports with geolocation mapping, risk scoring, and visual analytics.

![Version](https://img.shields.io/badge/version-2.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Integration](#-api-integration)
- [Features Overview](#-features-overview)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Capabilities

- **Multi-Source Threat Intelligence**: Aggregates data from AbuseIPDB, VirusTotal, and IPinfo
- **Unified Threat Scoring**: Calculates confidence and severity scores (0-100)
- **Geolocation Mapping**: Interactive maps with precise coordinate visualization
- **Real-time Analysis**: Fast IP address threat assessment
- **Visual Analytics**: 
  - Threat distribution pie charts
  - Score analysis bar charts
  - Segmented progress indicators
- **Comprehensive Reporting**: Detailed threat categories, network information, and geolocation data

### Threat Intelligence Features

- **Confidence Score**: Reliability of threat attribution (0-100)
- **Severity Score**: Potential risk level assessment (0-100)
- **Threat Categories**: SPAM, PROXY, MALICIOUS, PHISHING, BOTNET detection
- **Network Intelligence**: ASN, Organization, ISP, Domain information
- **Geographic Risk Assessment**: Location-based threat pattern analysis

## 🖼️ Screenshots

The application features a modern dark-themed interface with:
- Interactive IP address lookup
- Real-time threat analysis results
- Interactive geolocation maps
- Comprehensive threat intelligence visualization

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- API keys for:
  - [AbuseIPDB](https://www.abuseipdb.com/)
  - [VirusTotal](https://www.virustotal.com/)
  - [IPinfo](https://ipinfo.io/)

### Step 1: Clone the Repository

```bash
git clone https://github.com/vaish173/TechSpark_18.git
cd TechSpark_18/ip-search-engine
```

### Step 2: Install Dependencies

```bash
pip install streamlit pandas numpy plotly requests python-dotenv
```

Or install from requirements file (if available):

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

Create a `.env` file in the project root:

```env
ABUSEIPDB_API_KEY=your_abuseipdb_api_key_here
VT_API_KEY=your_virustotal_api_key_here
IPINFO_TOKEN=your_ipinfo_token_here
```

**Note**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

## ⚙️ Configuration

### API Keys Setup

1. **AbuseIPDB API Key**:
   - Sign up at [AbuseIPDB](https://www.abuseipdb.com/)
   - Get your API key from the dashboard
   - Add to `.env` as `ABUSEIPDB_API_KEY`

2. **VirusTotal API Key**:
   - Register at [VirusTotal](https://www.virustotal.com/)
   - Obtain API key from your account settings
   - Add to `.env` as `VT_API_KEY`

3. **IPinfo Token**:
   - Create account at [IPinfo](https://ipinfo.io/)
   - Generate access token
   - Add to `.env` as `IPINFO_TOKEN`

## 💻 Usage

### Web Interface (Streamlit)

Run the Streamlit web application:

```bash
python -m streamlit run tice_app_ui.py
```

Or on Windows PowerShell:

```bash
streamlit run tice_app_ui.py
```

The application will open in your default browser at `http://localhost:8501`

### Command Line Interface

You can also use the CLI for quick IP analysis:

```bash
python tice_api_collector.py <IP_ADDRESS>
```

Example:

```bash
python tice_api_collector.py 8.8.8.8
```

For debug mode:

```bash
python tice_api_collector.py 8.8.8.8 --debug
```

## 📁 Project Structure

```
ip-search-engine/
│
├── tice_app_ui.py          # Streamlit web interface
├── tice_api_collector.py   # API integration and CLI
├── tice_processor.py       # Threat intelligence processing logic
├── .env                    # Environment variables (not in repo)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

### File Descriptions

- **`tice_app_ui.py`**: Main Streamlit application with interactive UI, visualizations, and geolocation mapping
- **`tice_api_collector.py`**: Handles API calls to threat intelligence sources and CLI interface
- **`tice_processor.py`**: Core processing logic that unifies data from multiple sources and calculates threat scores

## 🔌 API Integration

### Supported APIs

1. **AbuseIPDB API v2**
   - Provides abuse confidence scores
   - Reports count and usage type
   - Country and ASN information

2. **VirusTotal API v3**
   - Malicious detection counts
   - Certificate information
   - Domain associations

3. **IPinfo API**
   - Detailed geolocation data
   - City, region, country
   - Organization and ASN
   - Timezone and coordinates

### API Rate Limits

- **AbuseIPDB**: Varies by plan (free tier: 1,000 requests/day)
- **VirusTotal**: 4 requests/minute (free tier)
- **IPinfo**: 50,000 requests/month (free tier)

## 📊 Features Overview

### Threat Intelligence Dashboard

- **Confidence Score**: Measures the reliability of threat attribution based on successful API responses
- **Severity Score**: Weighted risk assessment (0-100) based on:
  - AbuseIPDB confidence score
  - VirusTotal malicious detections
  - Reputation indicators

### Geolocation Features

- **Interactive Maps**: Visual representation of IP location
- **Coordinate Display**: Precise latitude and longitude
- **Location Details**: City, region, country, timezone
- **Network Information**: ASN, organization, ISP, domain

### Threat Categories

- Automatic categorization of threats:
  - SPAM
  - PROXY
  - MALICIOUS
  - PHISHING
  - BOTNET

### Visual Analytics

- **Threat Distribution**: Pie charts showing threat category breakdown
- **Score Analysis**: Bar charts comparing confidence and severity
- **Progress Indicators**: Segmented progress bars with color coding

## 🛠️ Development

### Running in Development Mode

```bash
# Set debug mode
export RICE_DEBUG=True  # Linux/Mac
set RICE_DEBUG=True     # Windows

# Run with debug output
python tice_api_collector.py 8.8.8.8 --debug
```

### Code Structure

The project follows a modular architecture:

1. **UI Layer** (`tice_app_ui.py`): Streamlit interface and visualizations
2. **API Layer** (`tice_api_collector.py`): External API integration
3. **Processing Layer** (`tice_processor.py`): Data unification and scoring

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to functions
- Include error handling
- Test with multiple IP addresses
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [AbuseIPDB](https://www.abuseipdb.com/) for threat intelligence data
- [VirusTotal](https://www.virustotal.com/) for malware detection
- [IPinfo](https://ipinfo.io/) for geolocation services
- [Streamlit](https://streamlit.io/) for the web framework
- [Plotly](https://plotly.com/) for interactive visualizations

## 📧 Support

For issues, questions, or contributions, please open an issue on the [GitHub repository](https://github.com/ShwetaNingappa/intel-guard.git).

## 🔒 Security Note

- Never commit API keys or `.env` files
- Keep your API keys secure and rotate them regularly
- Use environment variables for sensitive data
- Review API rate limits to avoid service disruption

---

**Made with ❤️ for cybersecurity professionals and threat researchers**