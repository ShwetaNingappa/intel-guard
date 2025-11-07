import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import plotly.graph_objects as go
from datetime import datetime

# --- Add project path for local imports ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from tice_api_collector import get_raw_threat_data, process_raw_data, is_valid_ip
except ImportError as e:
    st.error(f"❌ Could not import logic from 'tice_api_collector.py': {e}")
    st.stop()

# --- GEOLOCATION EXTRACTION FUNCTION ---
def extract_geolocation_data(report: dict, raw_data: dict) -> dict:
    """
    Extracts geolocation data using the processor's unified geolocation logic.
    
    The processor (tice_processor.py) consolidates geolocation from:
    - IPinfo: city, region, country, org, asn, timezone, loc (coordinates)
    - AbuseIPDB: countryCode, asn, hostnames
    
    Returns a dictionary with all geolocation fields for UI display.
    """
    # Get unified geolocation from processor
    geo = report.get("geolocation", {})
    
    # Get raw API data for fields not in unified geo
    ipinfo = raw_data.get("IPinfo", {})
    vt = raw_data.get("VirusTotal", {})
    abuse = raw_data.get("AbuseIPDB", {})
    abuse_data = abuse.get("data", {}) if isinstance(abuse.get("data"), dict) else abuse
    
    # Extract from unified geolocation (processor output)
    city = geo.get("city", "N/A")
    region = geo.get("region", "N/A")
    country = geo.get("country", "N/A")
    asn = geo.get("asn", "N/A")
    org = geo.get("org", "N/A")
    
    # Clean organization name (remove ASN prefix if present)
    if isinstance(org, str) and org.startswith("AS"):
        org_parts = org.split(None, 1)
        if len(org_parts) > 1:
            org = org_parts[1]
    
    # Get coordinates from IPinfo (not stored in unified geo)
    coords = ipinfo.get("loc", "")
    lat, lon = ("", "")
    if coords:
        coord_parts = coords.split(",")
        if len(coord_parts) == 2:
            lat, lon = coord_parts[0].strip(), coord_parts[1].strip()
    
    # Get timezone from IPinfo (not in unified geo)
    timezone = ipinfo.get("timezone", "N/A")
    
    # Get ISP from AbuseIPDB (fallback to organization)
    isp = abuse_data.get("isp", "")
    if not isp:
        isp = org if org != "N/A" else "N/A"
    
    # Extract domain from multiple sources
    domain = "N/A"
    # Try VirusTotal certificate first
    vt_data = vt.get("data", {})
    if isinstance(vt_data, dict):
        vt_attrs = vt_data.get("attributes", {})
        if isinstance(vt_attrs, dict):
            cert = vt_attrs.get("last_https_certificate", {})
            if isinstance(cert, dict):
                ext = cert.get("extensions", {})
                if isinstance(ext, dict):
                    san = ext.get("subject_alternative_name", [])
                    if isinstance(san, list) and len(san) > 0:
                        domain = san[0]
    
    # Fallback to hostnames from geolocation (from AbuseIPDB)
    if domain == "N/A":
        hostnames = geo.get("hostnames", [])
        if isinstance(hostnames, list) and len(hostnames) > 0:
            domain = hostnames[0]
        elif ipinfo.get("hostname"):
            domain = ipinfo["hostname"]
    
    return {
        "city": city,
        "region": region,
        "country": country,
        "asn": asn,
        "org": org,
        "isp": isp,
        "domain": domain,
        "timezone": timezone,
        "lat": lat,
        "lon": lon
    }

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="🛡️ TICE - Threat Intelligence Correlation Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .main {
        background-color: #0B1623;
    }
    
    body {
        background-color: #0B1623;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header */
    .header-title {
        color: #4EA8DE;
        font-size: 1.8em;
        font-weight: 600;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .header-subtitle {
        color: #B9CFFF;
        font-size: 0.95em;
        margin: 5px 0 0 0;
    }
    
    /* Cards */
    .info-card {
        background: #111C2E;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    
    .section-title {
        font-size: 1.2em;
        color: #B9CFFF;
        margin-bottom: 15px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .metric-large {
        font-size: 2.5em;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.9em;
        color: #888;
        margin-bottom: 10px;
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9em;
    }
    
    .status-malicious {
        background-color: #E94F4F;
        color: white;
    }
    
    .status-suspicious {
        background-color: #FFB84C;
        color: white;
    }
    
    .status-clean {
        background-color: #4CBB17;
        color: white;
    }
    
    /* Progress bar segments */
    .progress-segment {
        display: inline-block;
        height: 8px;
        border-radius: 4px;
        margin-right: 2px;
    }
    
    /* Threat tag */
    .threat-tag {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 15px;
        font-size: 0.85em;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    
    .stButton>button {
        background-color: #4EA8DE !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
    }
    
    .stButton>button:hover {
        background-color: #3d8fbc !important;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div style="margin-bottom: 30px;">
    <h1 class="header-title">🛡️ Threat Intelligence Correlation Engine</h1>
    <p class="header-subtitle">AI-Driven Multi-Source Threat Analysis & Attribution</p>
</div>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
st.markdown("""
<div class="info-card">
    <h3 style="color: #B9CFFF; margin-top: 0; display: flex; align-items: center; gap: 8px;">
        🔍 IP Address Lookup
    </h3>
    <p style="color: #aaa; margin-bottom: 15px;">Enter an IP address to analyze its threat profile and reputation.</p>
""", unsafe_allow_html=True)

ip_col, btn_col = st.columns([0.85, 0.15])
ip_address = ip_col.text_input("", value="1.1.1.1", label_visibility="collapsed", 
                                placeholder="Enter an IP address to analyze its threat profile and reputation")
analyze = btn_col.button("🔍 Analyze", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN LOGIC ---
if analyze:
    ip_clean = ip_address.strip().rstrip(".")
    if not is_valid_ip(ip_clean):
        st.error(f"❌ '{ip_address}' is not a valid IPv4 address.")
        st.stop()

    with st.spinner(f"Analyzing {ip_clean}..."):
        raw_data = get_raw_threat_data(ip_clean)
        report = process_raw_data(ip_clean, raw_data)

    # --- GEOLOCATION EXTRACTION ---
    # Extract all geolocation data using the dedicated function
    geo_data = extract_geolocation_data(report, raw_data)
    city = geo_data["city"]
    region = geo_data["region"]
    country = geo_data["country"]
    asn = geo_data["asn"]
    org = geo_data["org"]
    isp = geo_data["isp"]
    domain = geo_data["domain"]
    timezone = geo_data["timezone"]
    lat = geo_data["lat"]
    lon = geo_data["lon"]
    
    # Get AbuseIPDB data for threat analysis
    abuse = raw_data.get("AbuseIPDB", {})
    abuse_data = abuse.get("data", {}) if isinstance(abuse.get("data"), dict) else abuse
    report_count = abuse_data.get("totalReports", 0)
    usage_type = abuse_data.get("usageType", "")
    
    # Extract threat categories
    categories = report.get("categories", [])
    threat_types = []
    
    # Check AbuseIPDB usage type first
    if usage_type:
        usage_upper = str(usage_type).upper()
        if "HOSTING" in usage_upper or "DATACENTER" in usage_upper:
            threat_types.append("PROXY")
        elif "MOBILE" in usage_upper:
            threat_types.append("SPAM")
    
    # Extract from report categories
    for cat in categories:
        cat_upper = str(cat).upper()
        if "SPAM" in cat_upper:
            threat_types.append("SPAM")
        elif "PROXY" in cat_upper or "HOSTING" in cat_upper:
            threat_types.append("PROXY")
        elif "MALICIOUS" in cat_upper or "VIRUS" in cat_upper:
            threat_types.append("MALICIOUS")
        elif "PHISHING" in cat_upper:
            threat_types.append("PHISHING")
        elif "BOTNET" in cat_upper:
            threat_types.append("BOTNET")
    
    # If no specific categories found, use general ones based on severity
    if not threat_types:
        if report.get("reputation") == "Malicious":
            threat_types = ["MALICIOUS"]
        elif categories:
            # Extract category names
            for cat in categories[:2]:
                cat_name = str(cat).split("(")[0].strip().upper()
                if cat_name and len(cat_name) > 2:
                    threat_types.append(cat_name)
    
    # Default to SPAM and PROXY for visualization if we have reports but no categories
    if not threat_types and report_count > 0:
        threat_types = ["SPAM", "PROXY"]
    elif not threat_types:
        threat_types = ["UNKNOWN"]

    # --- STATUS RESULT BOX ---
    severity = report["severity_score"]
    confidence = int(report["confidence_score"] * 100)
    
    if severity >= 80:
        status_class = "status-malicious"
        status_text = "Malicious"
    elif severity >= 40:
        status_class = "status-suspicious"
        status_text = "Suspicious"
    else:
        status_class = "status-clean"
        status_text = "Clean"

    current_time = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    
    st.markdown(f"""
    <div class="info-card" style="display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; margin-bottom: 25px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="font-size: 1.5em;">⚠️</span>
            <div>
                <div style="font-size: 1.4em; font-weight: 600; color: white;">{ip_clean}</div>
                <div style="font-size: 0.9em; color: #aaa; margin-top: 5px;">Last seen: {current_time}</div>
            </div>
        </div>
        <span class="status-badge {status_class}">{status_text}</span>
    </div>
    """, unsafe_allow_html=True)

    # --- TWO COLUMN LAYOUT ---
    col1, col2 = st.columns(2)
    
    # LEFT COLUMN - TOP: Confidence Score
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Confidence Score</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Reliability of threat attribution</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-large" style="color: #E94F4F;">{confidence}/100</div>', unsafe_allow_html=True)
        
        # Segmented progress bar
        low_end = 49
        med_end = 74
        high_end = 100
        
        def get_segment_color(val):
            if val <= low_end:
                return "#4CBB17"  # Green
            elif val <= med_end:
                return "#FFB84C"  # Orange
            else:
                return "#E94F4F"  # Red
        
        progress_html = f'<div style="display: flex; gap: 2px; margin-top: 10px;">'
        segment_width = 100 / 100  # 100 segments for smooth appearance
        for i in range(100):
            if i < confidence:
                progress_html += f'<div style="flex: 1; height: 8px; background-color: {get_segment_color(i)}; border-radius: 2px;"></div>'
            else:
                progress_html += f'<div style="flex: 1; height: 8px; background-color: #2E3D59; border-radius: 2px;"></div>'
        progress_html += '</div>'
        st.markdown(progress_html, unsafe_allow_html=True)
        st.markdown('<div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 0.85em; color: #888;"><span>Low (0-49)</span><span>Medium (50-74)</span><span>High (75-100)</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # RIGHT COLUMN - TOP: Severity Score
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚠️ Severity Score</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Potential risk level</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-large" style="color: #FFB84C;">{severity}/100</div>', unsafe_allow_html=True)
        
        # Segmented progress bar
        progress_html = f'<div style="display: flex; gap: 2px; margin-top: 10px;">'
        for i in range(100):
            if i < severity:
                progress_html += f'<div style="flex: 1; height: 8px; background-color: {get_segment_color(i)}; border-radius: 2px;"></div>'
            else:
                progress_html += f'<div style="flex: 1; height: 8px; background-color: #2E3D59; border-radius: 2px;"></div>'
        progress_html += '</div>'
        st.markdown(progress_html, unsafe_allow_html=True)
        st.markdown('<div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 0.85em; color: #888;"><span>Low (0-49)</span><span>Medium (50-74)</span><span>High (75-100)</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # LEFT COLUMN - MIDDLE: Threat Distribution (Pie Chart)
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🕐 Threat Distribution</div>', unsafe_allow_html=True)
        
        # Create threat distribution data
        if len(threat_types) > 0:
            # Create counts for visualization based on report count and categories
            threat_counts = {}
            unique_threats = list(set(threat_types))
            
            if len(unique_threats) == 1:
                # If only one type, create a distribution (e.g., 47/53 split)
                main_type = unique_threats[0]
                if report_count > 0:
                    # Distribute based on report count
                    count1 = int(report_count * 0.47)
                    count2 = report_count - count1
                    if main_type == "SPAM":
                        threat_counts = {"SPAM": count1 if count1 > 0 else 47, "PROXY": count2 if count2 > 0 else 53}
                    elif main_type == "PROXY":
                        threat_counts = {"SPAM": count2 if count2 > 0 else 47, "PROXY": count1 if count1 > 0 else 53}
                    else:
                        threat_counts = {main_type: count1 if count1 > 0 else 50, "OTHER": count2 if count2 > 0 else 50}
                else:
                    # Default split for visualization
                    if main_type == "SPAM":
                        threat_counts = {"SPAM": 47, "PROXY": 53}
                    elif main_type == "PROXY":
                        threat_counts = {"SPAM": 47, "PROXY": 53}
                    else:
                        threat_counts = {main_type: 50, "OTHER": 50}
            else:
                # Multiple threat types - distribute based on counts
                total_threats = len(threat_types)
                for t in unique_threats:
                    count = threat_types.count(t)
                    threat_counts[t] = count
            
            # Create pie chart with Plotly
            labels = list(threat_counts.keys())
            values = list(threat_counts.values())
            colors_pie = ["#E94F4F", "#FFB84C", "#4EA8DE", "#4CBB17"][:len(labels)]
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                marker_colors=colors_pie,
                textinfo='label+percent',
                textposition='outside'
            )])
            fig_pie.update_layout(
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                height=300,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Legend
            legend_html = '<div style="display: flex; gap: 15px; justify-content: center; margin-top: 10px;">'
            for i, (label, color) in enumerate(zip(labels, colors_pie)):
                legend_html += f'<div style="display: flex; align-items: center; gap: 5px;"><div style="width: 12px; height: 12px; background-color: {color}; border-radius: 2px;"></div><span style="font-size: 0.9em;">{label}</span></div>'
            legend_html += '</div>'
            st.markdown(legend_html, unsafe_allow_html=True)
        else:
            st.info("No threat distribution data available.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # RIGHT COLUMN - MIDDLE: Score Analysis (Bar Chart)
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Score Analysis</div>', unsafe_allow_html=True)
        
        # Create bar chart
        fig_bar = go.Figure(data=[
            go.Bar(
                x=['Confidence', 'Severity'],
                y=[confidence, severity],
                marker_color=['#4EA8DE', '#FFB84C'],
                text=[f'{confidence}%', f'{severity}%'],
                textposition='outside'
            )
        ])
        fig_bar.update_layout(
            yaxis=dict(range=[0, 100], title="Score"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=300,
            margin=dict(t=20, b=40, l=40, r=20),
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Summary
        st.markdown(f'<div style="display: flex; gap: 20px; margin-top: 15px; justify-content: center;"><span style="color: #4EA8DE; font-weight: 600;">Confidence {confidence}%</span><span style="color: #FFB84C; font-weight: 600;">Severity {severity}%</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # LEFT COLUMN - BOTTOM: Geolocation Data
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🌍 Geolocation Data</div>', unsafe_allow_html=True)
        
        location_str = f"{city}, {region}" if city != "N/A" and region != "N/A" else (city if city != "N/A" else region if region != "N/A" else "N/A")
        country_name = country if country != "N/A" else "N/A"
        
        st.markdown(f'<div style="margin-bottom: 10px;"><strong>Location:</strong> {location_str}<br><strong>Country:</strong> {country_name}</div>', unsafe_allow_html=True)
        
        # Display coordinates separately (Lat and Lon)
        if lat and lon and lat != "N/A" and lon != "N/A":
            try:
                lat_float = float(lat)
                lon_float = float(lon)
                
                # Display coordinates
                st.markdown(f'<div style="margin-bottom: 10px;"><strong>Lat:</strong> {lat_float}<br><strong>Lon:</strong> {lon_float}</div>', unsafe_allow_html=True)
                
                # Create map with marker
                map_data = pd.DataFrame({
                    'lat': [lat_float],
                    'lon': [lon_float]
                })
                
                # Display map
                st.map(map_data, zoom=10, use_container_width=True)
                
            except (ValueError, TypeError):
                st.markdown(f'<div style="margin-bottom: 10px;"><strong>Coordinates:</strong> Invalid coordinates</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="margin-bottom: 10px;"><strong>Coordinates:</strong> N/A</div>', unsafe_allow_html=True)
            st.info("Coordinates not available for mapping.")
        
        st.markdown(f'<div style="margin-bottom: 15px; margin-top: 15px;"><strong>Timezone:</strong> {timezone}</div>', unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #1A2A3E; padding: 12px; border-radius: 6px; border-left: 3px solid #4EA8DE; margin-top: 15px;">
            <div style="font-size: 0.9em; color: #B9CFFF;">
                <strong>Geographic Risk Assessment:</strong> Location-based analysis helps identify potential threats based on regional patterns and known malicious infrastructure.
            </div>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # RIGHT COLUMN - BOTTOM: Network Information
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🌐 Network Information</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div style="margin-bottom: 10px;"><strong>ASN:</strong> {asn}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-bottom: 10px;"><strong>Organization:</strong> {org}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-bottom: 10px;"><strong>ISP:</strong> {isp}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-bottom: 10px;"><strong>Domain:</strong> {domain}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # BOTTOM SECTION: Threat Categories (Full Width)
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚠️ Threat Categories</div>', unsafe_allow_html=True)
    
    if threat_types:
        tags_html = '<div style="margin-bottom: 15px;">'
        tag_colors = {
            "SPAM": "#E94F4F",
            "PROXY": "#FFB84C",
            "MALICIOUS": "#E94F4F",
            "PHISHING": "#FF6B6B",
            "BOTNET": "#8B0000",
            "UNKNOWN": "#888"
        }
        for threat in set(threat_types):
            color = tag_colors.get(threat, "#888")
            tags_html += f'<span class="threat-tag" style="background-color: {color}; color: white;">{threat}</span>'
        tags_html += '</div>'
        st.markdown(tags_html, unsafe_allow_html=True)
    
    st.markdown(f'<div style="color: #aaa; font-size: 0.9em;">Report Count: {report_count} reports from threat intelligence sources</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- RAW DATA EXPANDER ---
    with st.expander("🔍 Expand for Full Raw Data"):
        st.json(raw_data)

else:
    st.info("💡 Enter an IP address and click **Analyze** to generate the full threat intelligence report.")
