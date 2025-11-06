import google.generativeai as genai
import json
from typing import Dict, Any
from ..models.schemas import UnifiedReport, ThreatAnalysis, NewsCampaigns
from ..core.config import Settings


class GeminiAnalyzer:
    """AI-powered threat analysis using Google Gemini."""
    
    SYSTEM_INSTRUCTION = """You are a highly-qualified Cyber Threat Intelligence Analyst. Your task is to review the aggregated data provided from EIGHT different threat intelligence sources. Synthesize findings, evaluate consensus and discrepancies across the sources, and generate a final, justified threat score. 

The score must be an integer between 0 (safe) and 100 (malicious). 

Scoring Guidelines:
- HIGH SCORE (75-100): Strong consensus across multiple sources indicating malicious activity, recent abuse reports, suspicious ownership patterns, high OTX pulse count, or indicators of bulletproof hosting.
- MEDIUM SCORE (40-74): Mixed signals, some concerning indicators but not strong consensus, or transient cloud hosting with moderate reputation issues.
- LOW SCORE (0-39): Clean reports across multiple sources, legitimate organization ownership, and no significant threat indicators.

Always analyze the WHOIS/Ownership data to determine if the IP belongs to a generic cloud provider (like AWS/GCP/Azure, which are often transient and used by both legitimate and malicious actors) versus a dedicated bulletproof host or suspicious organization.

Consider these 8 sources:
1. AbuseIPDB score and number of reports
2. OTX (AlienVault) pulse count and pulse details - HIGH IMPORTANCE
3. IPinfo organization and location data
4. IP-API geolocation and hosting type
5. IPStack detailed location data
6. WhoisXML registration details and organization legitimacy
7. SecurityTrails historical data
8. News API articles mentioning cyber attacks related to this infrastructure - HIGH IMPORTANCE

CRITICAL ANALYSIS POINTS:
- If OTX pulse count is HIGH (>10), this strongly indicates the IP is involved in malicious activity
- If News API returns articles about cyber attacks involving this infrastructure/organization, this significantly increases the threat score
- The rationale MUST explicitly state: "The News API returned X articles mentioning cyber attacks related to this infrastructure, strongly supporting the high OTX pulse count" when applicable

Additionally, based on the IP's ISP, ASN, organization, abuse patterns, OTX pulses, and News articles, identify 2-3 famous cyber campaigns, APT groups, or recent security incidents related to this infrastructure or abuse type. Use your knowledge of cybersecurity threat landscape.

Provide a detailed rationale that references specific data points from the sources, especially OTX pulse data and News API findings."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        genai.configure(api_key=settings.gemini_api_key)
        # Using gemini-2.5-flash for modern, fast analysis
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={
                "temperature": 0.3,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        )
    
    def analyze_threat(self, unified_report: UnifiedReport) -> tuple[ThreatAnalysis, NewsCampaigns]:
        """
        Analyze the unified threat report using Gemini AI.
        
        Args:
            unified_report: Normalized threat intelligence data
            
        Returns:
            Tuple of (ThreatAnalysis with final score and rationale, NewsCampaigns with related threats)
        """
        # Prepare the prompt with structured data
        prompt = self._build_analysis_prompt(unified_report)
        
        try:
            # Generate analysis
            response = self.model.generate_content(prompt)
            
            # Extract JSON string from response (structured output access)
            json_string = response.candidates[0].content.parts[0].text
            
            # Parse JSON response
            analysis_data = json.loads(json_string)
            
            # Validate and create ThreatAnalysis object
            threat_analysis = ThreatAnalysis(
                final_threat_score=int(analysis_data.get("final_threat_score", 50)),
                ai_rationale=analysis_data.get("ai_rationale", "Analysis could not be completed.")
            )
            
            # Extract news campaigns
            news_campaigns = NewsCampaigns(
                campaigns=analysis_data.get("related_campaigns", [])
            )
            
            return threat_analysis, news_campaigns
        
        except Exception as e:
            # Fallback in case of error
            return (
                ThreatAnalysis(
                    final_threat_score=50,
                    ai_rationale=f"AI analysis encountered an error: {str(e)}. Manual review recommended."
                ),
                NewsCampaigns(campaigns=[])
            )
    
    def _build_analysis_prompt(self, report: UnifiedReport) -> str:
        """Build the analysis prompt from unified report data."""
        
        prompt = f"""{self.SYSTEM_INSTRUCTION}

Analyze the following threat intelligence data for IP address {report.ip_address}:

REPUTATION DATA:
- AbuseIPDB Score: {report.reputation.abuseipdb_score}
- AbuseIPDB Reports: {len(report.reputation.abuseipdb_reports or [])} recent reports
- OTX Pulse Count: {report.reputation.otx_pulse_count} (CRITICAL INDICATOR)
- OTX Pulses: {json.dumps(report.reputation.otx_pulses[:3] if report.reputation.otx_pulses else [], indent=2)}
- VirusTotal Detections (summary): {json.dumps(report.reputation.virustotal_detections)}
- VirusTotal Related URLs (top 5): {json.dumps(report.virustotal_related_urls[:5] if report.virustotal_related_urls else [], indent=2)}

GEOLOCATION DATA:
- Country (IPinfo): {report.geolocation.ipinfo_country}
- Organization (IPinfo): {report.geolocation.ipinfo_org}
- Country (IP-API): {report.geolocation.ip_api_country}
- ISP (IP-API): {report.geolocation.ip_api_isp}
- Country (IPStack): {report.geolocation.ipstack_country}
- ISP (IPStack): {report.geolocation.ipstack_isp}
- Hosting/Datacenter Flag: {report.geolocation.consensus_hosting_flag}

OWNERSHIP DATA:
- Registrar: {report.ownership.whoisxml_registrar}
- Organization: {report.ownership.whoisxml_organization}
- Admin Email: {report.ownership.whois_admin_email}
- Historical Records Count: {report.ownership.securitytrails_historical_count}

NEWS API ARTICLES (CRITICAL INDICATOR):
{json.dumps(report.news_articles[:3] if report.news_articles else [], indent=2)}
Article Count: {len(report.news_articles)} articles found mentioning cyber attacks related to this infrastructure

RECENT ABUSE REPORTS:
{json.dumps(report.reputation.abuseipdb_reports[:3] if report.reputation.abuseipdb_reports else [], indent=2)}

Based on this data, provide your analysis in the following JSON format:
{{
  "final_threat_score": <integer 0-100>,
  "ai_rationale": "<detailed paragraph explaining the score, referencing specific data points and cross-source consensus/discrepancies>",
  "related_campaigns": ["Campaign/APT/News item 1", "Campaign/APT/News item 2", "Campaign/APT/News item 3"]
}}"""
        
        return prompt
