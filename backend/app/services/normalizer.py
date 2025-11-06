from typing import Dict, Any, List
from ..models.schemas import UnifiedReport, ReputationData, GeolocationData, OwnershipData


class DataNormalizer:
    """Normalize raw API responses into unified report structure."""
    
    @staticmethod
    def normalize_data(ip: str, raw_results: Dict[str, Any]) -> UnifiedReport:
        """
        Process raw API responses into a unified report structure.
        
        Args:
            ip: The IP address being analyzed
            raw_results: Dictionary containing responses from all external APIs
            
        Returns:
            UnifiedReport object with normalized data
        """
        # Extract reputation data
        reputation = DataNormalizer._extract_reputation(raw_results)
        
        # Extract geolocation data
        geolocation = DataNormalizer._extract_geolocation(raw_results)
        
        # Extract ownership data
        ownership = DataNormalizer._extract_ownership(raw_results)
        
        # Extract news articles
        news_articles = DataNormalizer._extract_news_articles(raw_results)

        # Extract VirusTotal related URLs
        vt_related_urls = DataNormalizer._extract_virustotal_related_urls(raw_results)
        
        return UnifiedReport(
            ip_address=ip,
            reputation=reputation,
            geolocation=geolocation,
            ownership=ownership,
            news_articles=news_articles,
            virustotal_related_urls=vt_related_urls,
            raw_data=raw_results
        )
    
    @staticmethod
    def _extract_reputation(raw_results: Dict[str, Any]) -> ReputationData:
        """Extract and normalize reputation data from AbuseIPDB, OTX, and VirusTotal."""
        reputation = ReputationData()
        
        # AbuseIPDB data
        if raw_results.get("abuseipdb", {}).get("success"):
            abuseipdb_data = raw_results["abuseipdb"].get("data", {}).get("data", {})
            reputation.abuseipdb_score = abuseipdb_data.get("abuseConfidenceScore")
            
            # Extract recent reports
            reports = abuseipdb_data.get("reports", [])
            if reports:
                reputation.abuseipdb_reports = [
                    {
                        "reportedAt": report.get("reportedAt"),
                        "comment": report.get("comment"),
                        "categories": report.get("categories", [])
                    }
                    for report in reports[:5]  # Limit to 5 most recent
                ]
        
        # OTX (AlienVault Open Threat Exchange) data
        if raw_results.get("otx", {}).get("success"):
            otx_data = raw_results["otx"].get("data", {})
            pulse_info = otx_data.get("pulse_info", {})
            pulses = pulse_info.get("pulses", [])
            
            reputation.otx_pulse_count = pulse_info.get("count", 0)
            if pulses:
                reputation.otx_pulses = [
                    {
                        "name": pulse.get("name"),
                        "description": pulse.get("description"),
                        "tags": pulse.get("tags", []),
                        "created": pulse.get("created")
                    }
                    for pulse in pulses[:5]  # Limit to 5 most relevant pulses
                ]
        
        # VirusTotal detections (summary if available)
        if raw_results.get("virustotal", {}).get("success"):
            vt = raw_results["virustotal"].get("data", {})
            # Some VT endpoints return {"data": {"attributes": {"last_analysis_stats": {...}}}}
            attrs = vt.get("data", {}).get("attributes") if isinstance(vt.get("data"), dict) else vt.get("attributes")
            stats = None
            if isinstance(attrs, dict):
                stats = attrs.get("last_analysis_stats")
            # Fallback to zeroed structure if not present
            if isinstance(stats, dict):
                reputation.virustotal_detections = stats
            else:
                reputation.virustotal_detections = {
                    "malicious": 0,
                    "suspicious": 0,
                    "harmless": 0,
                    "undetected": 0,
                }
        else:
            reputation.virustotal_detections = {
                "malicious": 0,
                "suspicious": 0,
                "harmless": 0,
                "undetected": 0,
            }
        
        return reputation
    
    @staticmethod
    def _extract_geolocation(raw_results: Dict[str, Any]) -> GeolocationData:
        """Extract and normalize geolocation data from IP-API and IPStack."""
        geolocation = GeolocationData()
        
        # IPinfo data
        if raw_results.get("ipinfo", {}).get("success"):
            ipinfo_data = raw_results["ipinfo"].get("data", {})
            geolocation.ipinfo_country = ipinfo_data.get("country")
            geolocation.ipinfo_org = ipinfo_data.get("org")
        
        # IP-API data
        if raw_results.get("ipapi", {}).get("success"):
            ipapi_data = raw_results["ipapi"].get("data", {})
            geolocation.ip_api_country = ipapi_data.get("country")
            geolocation.ip_api_isp = ipapi_data.get("isp")
            ipapi_hosting = ipapi_data.get("hosting", False)
        else:
            ipapi_hosting = None
        
        # IPStack data
        if raw_results.get("ipstack", {}).get("success"):
            ipstack_data = raw_results["ipstack"].get("data", {})
            geolocation.ipstack_country = ipstack_data.get("country_name")
            geolocation.ipstack_isp = ipstack_data.get("connection", {}).get("isp")
        
        # Determine consensus hosting flag
        # Check if multiple sources indicate hosting/datacenter
        hosting_indicators = []
        
        if ipapi_hosting is not None:
            hosting_indicators.append(ipapi_hosting)
        
        # Check ISP names for common hosting providers
        isp_names = [geolocation.ip_api_isp, geolocation.ipstack_isp]
        hosting_keywords = ["amazon", "aws", "google", "microsoft", "azure", "digitalocean", 
                           "linode", "vultr", "ovh", "hetzner", "cloudflare"]
        
        for isp in isp_names:
            if isp:
                isp_lower = isp.lower()
                if any(keyword in isp_lower for keyword in hosting_keywords):
                    hosting_indicators.append(True)
                    break
        
        # Consensus: if any indicator suggests hosting, mark as true
        geolocation.consensus_hosting_flag = any(hosting_indicators) if hosting_indicators else None
        
        return geolocation
    
    @staticmethod
    def _extract_ownership(raw_results: Dict[str, Any]) -> OwnershipData:
        """Extract and normalize ownership/WHOIS data from WhoisXML and SecurityTrails."""
        ownership = OwnershipData()
        
        # WhoisXML data
        if raw_results.get("whoisxml", {}).get("success"):
            whois_data = raw_results["whoisxml"].get("data", {})
            whois_record = whois_data.get("WhoisRecord", {})
            
            registrar_info = whois_record.get("registrarName")
            if registrar_info:
                ownership.whoisxml_registrar = registrar_info
            
            registrant = whois_record.get("registrant", {})
            ownership.whoisxml_organization = registrant.get("organization")
            
            contact_email = whois_record.get("contactEmail") or whois_record.get("administrativeContact", {}).get("email")
            if contact_email:
                ownership.whois_admin_email = contact_email
        
        # SecurityTrails data
        if raw_results.get("securitytrails", {}).get("success"):
            st_data = raw_results["securitytrails"].get("data", {})
            # Count historical records
            blocks = st_data.get("blocks", [])
            ownership.securitytrails_historical_count = len(blocks) if blocks else 0
        
        return ownership
    
    @staticmethod
    def _extract_news_articles(raw_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract and format news articles from News API."""
        articles = []
        
        if raw_results.get("news", {}).get("success"):
            news_data = raw_results["news"].get("data", {})
            news_articles = news_data.get("articles", [])
            
            for article in news_articles[:5]:  # Limit to 5 most relevant
                articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "source": article.get("source", {}).get("name"),
                    "url": article.get("url"),
                    "publishedAt": article.get("publishedAt")
                })
        
        return articles

    @staticmethod
    def _extract_virustotal_related_urls(raw_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract related URLs from VirusTotal response if available."""
        urls: List[Dict[str, Any]] = []
        vt = raw_results.get("virustotal", {})
        if vt.get("success"):
            vt_data = vt.get("data", {})
            # The relationships endpoint typically returns {"data": [ {...}, ... ]}
            items = vt_data.get("data") if isinstance(vt_data, dict) else None
            if isinstance(items, list):
                for item in items[:50]:  # cap to 50 for UI/AI prompt size
                    attrs = item.get("attributes", {}) if isinstance(item, dict) else {}
                    stats = attrs.get("last_analysis_stats", {}) if isinstance(attrs, dict) else {}
                    url_value = item.get("id") or attrs.get("url")
                    last_submission = attrs.get("last_submission_date")
                    urls.append({
                        "url": url_value,
                        "last_analysis_stats": stats,
                        "last_submission_date": last_submission,
                    })
        return urls
