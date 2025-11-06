import httpx
import asyncio
from typing import Dict, Any, Optional
from ..core.config import Settings


class ThreatAPIClient:
    """Client for querying external threat intelligence APIs."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.timeout = httpx.Timeout(30.0)
    
    async def fetch_abuseipdb(self, ip: str) -> Dict[str, Any]:
        """Query AbuseIPDB API for IP reputation."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    "https://api.abuseipdb.com/api/v2/check",
                    headers={"Key": self.settings.abuseipdb_key, "Accept": "application/json"},
                    params={"ipAddress": ip, "maxAgeInDays": 90, "verbose": ""}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    async def fetch_virustotal(self, ip: str) -> Dict[str, Any]:
        """Query VirusTotal API for IP analysis."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"https://www.virustotal.com/api/v3/ip_addresses/{ip}",
                    headers={"x-apikey": self.settings.virustotal_key}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    async def fetch_ipapi(self, ip: str) -> Dict[str, Any]:
        """Query IP-API for geolocation information (free tier, no key needed for basic)."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # IP-API free tier endpoint
                response = await client.get(
                    f"http://ip-api.com/json/{ip}",
                    params={"fields": "status,message,country,countryCode,region,city,isp,org,as,hosting,query"}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    async def fetch_ipstack(self, ip: str) -> Dict[str, Any]:
        """Query IPStack API for detailed geolocation."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"http://api.ipstack.com/{ip}",
                    params={"access_key": self.settings.ipstack_key}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    async def fetch_whoisxml(self, ip: str) -> Dict[str, Any]:
        """Query WhoisXML API for WHOIS information."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    "https://www.whoisxmlapi.com/whoisserver/WhoisService",
                    params={
                        "apiKey": self.settings.whoisxml_key,
                        "domainName": ip,
                        "outputFormat": "JSON"
                    }
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    async def fetch_securitytrails(self, ip: str) -> Dict[str, Any]:
        """Query SecurityTrails API for historical IP data."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"https://api.securitytrails.com/v1/ips/nearby/{ip}",
                    headers={"APIKEY": self.settings.securitytrails_key}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    async def fetch_otx(self, ip: str) -> Dict[str, Any]:
        """Query AlienVault OTX (Open Threat Exchange) for threat intelligence."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general",
                    headers={"X-OTX-API-KEY": self.settings.otx_key}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    async def fetch_ipinfo(self, ip: str) -> Dict[str, Any]:
        """Query IPinfo API for detailed IP information."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"https://ipinfo.io/{ip}/json",
                    params={"token": self.settings.ipinfo_key}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    async def fetch_news_campaigns(self, ip: str, isp: Optional[str] = None, org: Optional[str] = None) -> Dict[str, Any]:
        """Query News API for cyber security news related to the IP's infrastructure."""
        try:
            # Build search query based on ISP/Organization and cybersecurity keywords
            search_terms = []
            if org:
                search_terms.append(org)
            elif isp:
                search_terms.append(isp)
            
            # Add cybersecurity keywords
            search_terms.extend(["cyber attack", "malware", "DDoS", "exploit", "breach"])
            query = " OR ".join(search_terms[:3])  # Limit to avoid overly broad search
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    "https://newsapi.org/v2/everything",
                    params={
                        "q": query,
                        "apiKey": self.settings.news_api_key,
                        "language": "en",
                        "sortBy": "relevancy",
                        "pageSize": 5
                    }
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    async def gather_all_sources(self, ip: str, isp: Optional[str] = None, org: Optional[str] = None) -> Dict[str, Any]:
        """Execute all 8 API calls concurrently and return aggregated results."""
        results = await asyncio.gather(
            self.fetch_abuseipdb(ip),
            self.fetch_otx(ip),
            self.fetch_ipinfo(ip),
            self.fetch_ipapi(ip),
            self.fetch_ipstack(ip),
            self.fetch_whoisxml(ip),
            self.fetch_securitytrails(ip),
            self.fetch_news_campaigns(ip, isp, org),
            return_exceptions=True
        )
        
        return {
            "abuseipdb": results[0] if not isinstance(results[0], Exception) else {"success": False, "error": str(results[0])},
            "otx": results[1] if not isinstance(results[1], Exception) else {"success": False, "error": str(results[1])},
            "ipinfo": results[2] if not isinstance(results[2], Exception) else {"success": False, "error": str(results[2])},
            "ipapi": results[3] if not isinstance(results[3], Exception) else {"success": False, "error": str(results[3])},
            "ipstack": results[4] if not isinstance(results[4], Exception) else {"success": False, "error": str(results[4])},
            "whoisxml": results[5] if not isinstance(results[5], Exception) else {"success": False, "error": str(results[5])},
            "securitytrails": results[6] if not isinstance(results[6], Exception) else {"success": False, "error": str(results[6])},
            "news": results[7] if not isinstance(results[7], Exception) else {"success": False, "error": str(results[7])}
        }
