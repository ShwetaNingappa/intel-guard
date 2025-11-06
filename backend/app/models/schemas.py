from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ThreatAnalysis(BaseModel):
    """Gemini AI generated threat analysis."""
    final_threat_score: int = Field(..., ge=0, le=100, description="The synthesized threat score, an integer from 0 to 100.")
    ai_rationale: str = Field(..., description="A detailed, human-readable paragraph explaining the score based on the consensus and discrepancies in the source data.")


class NewsCampaigns(BaseModel):
    """Related cyber campaigns and news articles."""
    campaigns: List[str] = Field(default_factory=list, description="List of 2-3 famous cyber campaigns or news related to the IP's infrastructure or abuse type")


class ReputationData(BaseModel):
    """Reputation information from threat intelligence sources."""
    abuseipdb_score: Optional[int] = None
    abuseipdb_reports: Optional[List[Dict[str, Any]]] = None
    otx_pulse_count: Optional[int] = None
    otx_pulses: Optional[List[Dict[str, Any]]] = None
    virustotal_detections: Optional[Dict[str, Any]] = None


class GeolocationData(BaseModel):
    """Geolocation information from multiple sources."""
    ip_api_country: Optional[str] = None
    ip_api_isp: Optional[str] = None
    ipinfo_country: Optional[str] = None
    ipinfo_org: Optional[str] = None
    ipstack_country: Optional[str] = None
    ipstack_isp: Optional[str] = None
    consensus_hosting_flag: Optional[bool] = None


class OwnershipData(BaseModel):
    """Ownership and WHOIS information."""
    whoisxml_registrar: Optional[str] = None
    whoisxml_organization: Optional[str] = None
    securitytrails_historical_count: Optional[int] = None
    whois_admin_email: Optional[str] = None


class UnifiedReport(BaseModel):
    """Unified threat intelligence report structure."""
    ip_address: str
    reputation: ReputationData
    geolocation: GeolocationData
    ownership: OwnershipData
    news_articles: List[Dict[str, Any]] = Field(default_factory=list, description="News articles from News API")
    virustotal_related_urls: List[Dict[str, Any]] = Field(default_factory=list, description="URLs related to this IP from VirusTotal with detection stats")
    raw_data: Dict[str, Any] = Field(default_factory=dict, description="Raw API responses for detailed analysis")


class ThreatCheckResponse(BaseModel):
    """Complete response for IP threat check."""
    ip_address: str
    reputation: ReputationData
    geolocation: GeolocationData
    ownership: OwnershipData
    news_articles: List[Dict[str, Any]]
    virustotal_related_urls: List[Dict[str, Any]]
    raw_data: Dict[str, Any]
    final_threat_score: int
    ai_rationale: str
    related_campaign_news: List[str] = Field(default_factory=list, description="List of 2-3 famous cyber campaigns or news articles related to the IP's infrastructure or type of abuse")


class ReportIPRequest(BaseModel):
    """Request model for reporting an IP to AbuseIPDB."""
    ip: str = Field(..., description="The IP address to report")
    categories: List[int] = Field(..., description="List of abuse category IDs")
    comment: str = Field(..., description="Detailed comment about the abusive activity")


class ReportIPResponse(BaseModel):
    """Response model for IP reporting."""
    success: bool
    message: str
    abuseipdb_response: Optional[Dict[str, Any]] = None
