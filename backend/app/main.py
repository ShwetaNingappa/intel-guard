from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Dict, Any

from .core.config import get_settings, Settings
from .models.schemas import (
    ThreatCheckResponse,
    ReportIPRequest,
    ReportIPResponse
)
from .services.threat_apis import ThreatAPIClient
from .services.normalizer import DataNormalizer
from .services.gemini_analyzer import GeminiAnalyzer

app = FastAPI(
    title="IP Threat Aggregator API",
    description="Aggregate threat intelligence from multiple sources with AI-powered analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "IP Threat Aggregator API",
        "version": "1.0.0"
    }


@app.get("/api/v1/check-ip/{ip_address}", response_model=ThreatCheckResponse)
async def check_ip(ip_address: str, settings: Settings = Depends(get_settings)):
    """
    Main endpoint: Aggregate threat intelligence and generate AI-powered threat score.
    
    Process:
    1. Fetch data from 7 external APIs concurrently
    2. Normalize data into unified report
    3. Analyze with Gemini AI to generate threat score
    4. Return complete response
    """
    try:
        import traceback
        print(f"\n=== Processing IP: {ip_address} ===")
        
        # Step 1: Initial data collection to get ISP/Org (for News API)
        threat_client = ThreatAPIClient(settings)
        print("Step 1: Fetching initial geo data...")
        try:
            initial_geo = await threat_client.fetch_ipinfo(ip_address)
            print(f"IPinfo result: {initial_geo.get('success')}")
        except Exception as e:
            print(f"IPinfo failed: {e}")
            traceback.print_exc()
            initial_geo = {"success": False}
        
        isp = None
        org = None
        if initial_geo.get("success"):
            org = initial_geo.get("data", {}).get("org")
        print(f"Organization: {org}")
        
        # Step 2: Concurrent data collection - ISOLATED FOR DEBUGGING
        print("Step 2: Gathering threat data...")
        try:
            raw_results = await threat_client.gather_all_sources(ip_address, isp, org)
            print(f"Gathered results from {len(raw_results)} sources")
        except Exception as e:
            print(f"Gather failed: {e}")
            traceback.print_exc()
            raise
        
        # Step 3: Normalize data into unified structure
        print("Step 3: Normalizing data...")
        try:
            unified_report = DataNormalizer.normalize_data(ip_address, raw_results)
            print("Normalization complete")
        except Exception as e:
            print(f"Normalization failed: {e}")
            traceback.print_exc()
            raise
        
        # Step 4: AI Analysis with Gemini (includes news campaigns)
        print("Step 4: Running Gemini AI analysis...")
        try:
            gemini_analyzer = GeminiAnalyzer(settings)
            threat_analysis, news_campaigns = gemini_analyzer.analyze_threat(unified_report)
            print(f"AI Score: {threat_analysis.final_threat_score}")
        except Exception as e:
            print(f"Gemini analysis failed: {e}")
            traceback.print_exc()
            raise
        
        # Step 4: Build final response
        response = ThreatCheckResponse(
            ip_address=unified_report.ip_address,
            reputation=unified_report.reputation,
            geolocation=unified_report.geolocation,
            ownership=unified_report.ownership,
            news_articles=unified_report.news_articles,
            raw_data=unified_report.raw_data,
            final_threat_score=threat_analysis.final_threat_score,
            ai_rationale=threat_analysis.ai_rationale,
            related_campaign_news=news_campaigns.campaigns
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing IP threat check: {str(e)}"
        )


@app.post("/api/v1/report-ip", response_model=ReportIPResponse)
async def report_ip(
    report_request: ReportIPRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Report an IP address to AbuseIPDB.
    
    Args:
        report_request: IP address, abuse categories, and comment
        
    Returns:
        Success status and AbuseIPDB response
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.abuseipdb.com/api/v2/report",
                headers={
                    "Key": settings.abuseipdb_key,
                    "Accept": "application/json"
                },
                data={
                    "ip": report_request.ip,
                    "categories": ",".join(map(str, report_request.categories)),
                    "comment": report_request.comment
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            return ReportIPResponse(
                success=True,
                message="IP successfully reported to AbuseIPDB",
                abuseipdb_response=result
            )
    
    except httpx.HTTPStatusError as e:
        return ReportIPResponse(
            success=False,
            message=f"Failed to report IP: {e.response.status_code} - {e.response.text}",
            abuseipdb_response=None
        )
    
    except Exception as e:
        return ReportIPResponse(
            success=False,
            message=f"Error reporting IP: {str(e)}",
            abuseipdb_response=None
        )


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
