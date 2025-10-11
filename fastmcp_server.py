#!/usr/bin/env python3

import httpx
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

# Initialize FastMCP
mcp = FastMCP("AppVector MCP Server")

API_URL = "https://appvector.io/external-apis/api"

def extract_token_from_auth() -> str:
    """Extract token from Authorization header using FastMCP dependencies"""
    try:
        headers = get_http_headers()
        auth_header = headers.get('authorization', '')
        print(f"🔍 DEBUG: Headers received: {dict(headers)}")
        print(f"🔍 DEBUG: Auth header: {auth_header[:20]}..." if auth_header else "🔍 DEBUG: No auth header")
        
        if not auth_header:
            return ""
        
        # Support multiple formats: "Bearer token", "Token token", or just "token"
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
        elif auth_header.startswith('Token '):
            token = auth_header[6:]
        else:
            token = auth_header
            
        print(f"✅ DEBUG: Extracted token: {token[:8]}...")
        return token
    except Exception as e:
        print(f"❌ DEBUG: Error extracting token: {e}")
        return ""

def get_default_date_range() -> Dict[str, str]:
    """Get default date range (last 30 days)"""
    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)
    return {
        "start_date": thirty_days_ago.strftime("%Y-%m-%d"),
        "end_date": today.strftime("%Y-%m-%d")
    }

async def make_api_request(endpoint: str, token: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Make API request to AppVector with authentication"""
    if not token:
        raise ValueError("Token is required")
    
    url = f"{API_URL}{endpoint}"
    headers = {
        "Authorization": f"Token {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise ValueError(f"API request failed ({response.status_code}): {response.text}")
        
        return response.json()

@mcp.tool()
async def appvector_apple_metadata(
    app: str,
    data: str = "title",
    country: str = "in", 
    language: str = "en",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """Get Apple App Store metadata history (title, description, media, genre, developer, ratings, price, version)
    
    Args:
        app: Apple app ID (e.g., 284882215)
        data: Type of metadata (title, description, media, genre, developer, ratings, price, version)
        country: Country code (default: in)
        language: Language code (default: en)  
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."
    
    date_range = get_default_date_range()
    params = {
        "app": app,
        "data": data,
        "country": country,
        "language": language,
        "start_date": start_date or date_range["start_date"],
        "end_date": end_date or date_range["end_date"]
    }
    
    try:
        result = await make_api_request("/metadata/apple/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch Apple metadata: {str(e)}"

@mcp.tool()
async def appvector_apple_rank(
    app: str,
    country: str = "in",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """Get Apple App Store category rank history
    
    Args:
        app: Apple app ID (e.g., 1386412985)
        country: Country code (default: in)
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."
    
    date_range = get_default_date_range()
    params = {
        "app": app,
        "country": country,
        "start_date": start_date or date_range["start_date"],
        "end_date": end_date or date_range["end_date"]
    }
    
    try:
        result = await make_api_request("/category/rank/apple/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch Apple category ranks: {str(e)}"

@mcp.tool()
async def appvector_android_metadata(
    app: str,
    data: str = "title",
    country: str = "in",
    language: str = "en", 
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """Get Google Play Store metadata history (title, description, media, install, ratings, genre, developer, price, events, version)
    
    Args:
        app: Android package name (e.g., com.spotify.music)
        data: Type of metadata (title, description, media, install, ratings, genre, developer, price, events, version)
        country: Country code (default: in)
        language: Language code (default: en)
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."
    
    date_range = get_default_date_range()
    params = {
        "app": app,
        "data": data,
        "country": country,
        "language": language,
        "start_date": start_date or date_range["start_date"],
        "end_date": end_date or date_range["end_date"]
    }
    
    try:
        result = await make_api_request("/metadata/android/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch Android metadata: {str(e)}"

@mcp.tool()
async def appvector_android_rank(
    app: str,
    country: str = "in",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """Get Google Play Store category rank
    
    Args:
        app: Android package name (e.g., com.spotify.music)
        country: Country code (default: in)
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."
    
    date_range = get_default_date_range()
    params = {
        "app": app,
        "country": country,
        "start_date": start_date or date_range["start_date"],
        "end_date": end_date or date_range["end_date"]
    }
    
    try:
        result = await make_api_request("/category/rank/android/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch Android category ranks: {str(e)}"


@mcp.tool()
async def appvector_keyword_research(
    keywords: List[str],
    country: str = "in",
    language: str = "en",
    platform: str = "android"
) -> str:
    """Generate keyword suggestions for a list of base keywords
    
    Args:
        keywords: List of base keywords
        country: Country code (default: in)
        language: Language code (default: en)
        platform: Platform (android or ios, default: android)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."
    
    params = {
        "keywords": keywords,
        "country": country,
        "language": language,
        "platform": platform
    }
    
    try:
        # Use the correct endpoint format and POST method
        url = f"{API_URL}/keyword-research/{platform}/"
        headers = {
            "Authorization": f"Token {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=params)
            
            if response.status_code != 200:
                raise ValueError(f"API request failed ({response.status_code}): {response.text}")
            
            result = response.json()
            return str(result)
    except Exception as e:
        return f"Error: Failed to fetch keyword research: {str(e)}"

@mcp.tool()
async def appvector_apple_reviews(
    app: str,
    country: str = "in",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """Get Apple app user reviews history
    
    Args:
        app: Apple app ID (e.g., 281796108)
        country: Country code (default: in)
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."
    
    date_range = get_default_date_range()
    params = {
        "app": app,
        "country": country,
        "start_date": start_date or date_range["start_date"],
        "end_date": end_date or date_range["end_date"]
    }
    
    try:
        result = await make_api_request("/reviews/apple/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch Apple reviews: {str(e)}"

@mcp.tool()
async def appvector_android_reviews(
    app: str,
    language: str = "en",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """Get Android app user reviews history
    
    Args:
        app: Android package name (e.g., com.facebook.katana)
        language: Language code (default: en)
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."
    
    date_range = get_default_date_range()
    params = {
        "app": app,
        "language": language,
        "start_date": start_date or date_range["start_date"],
        "end_date": end_date or date_range["end_date"]
    }
    
    try:
        result = await make_api_request("/reviews/android/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch Android reviews: {str(e)}"

@mcp.tool()
async def appvector_apple_keyword_rank(
    app: str,
    keywords: str,
    country: str = "in",
    language: str = "en",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    date: Optional[str] = None
) -> str:
    """Get Apple app keyword ranking history
    
    Args:
        app: Apple app ID (e.g., 284882215)
        keywords: Comma-separated keywords to track rankings for
        country: Country code (default: in)
        language: Language code (default: en)
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
        date: Specific date in YYYY-MM-DD format (alternative to start_date/end_date)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."
    
    # Validate required parameters
    if not keywords or keywords.strip() == "":
        return "Error: Keywords parameter is required and cannot be empty"
    
    # Use default date range (last 30 days) or provided dates
    date_range = get_default_date_range()
    
    params = {
        "app_id": app,
        "keywords": keywords.strip(),
        "country": country,
        "language": language
    }
    
    if date:
        params["date"] = date
    else:
        params["start_date"] = start_date or date_range["start_date"]
        params["end_date"] = end_date or date_range["end_date"]
    
    try:
        result = await make_api_request("/ranks/apple/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch Apple keyword ranks: {str(e)}"

@mcp.tool()
async def appvector_android_keyword_rank(
    app: str,
    keywords: str,
    country: str = "in",
    language: str = "en",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    date: Optional[str] = None
) -> str:
    """Get Android app keyword ranking history
    
    Args:
        app: Android package name (e.g., com.spotify.music)
        keywords: Comma-separated keywords to track rankings for
        country: Country code (default: in)
        language: Language code (default: en)
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
        date: Specific date in YYYY-MM-DD format (alternative to start_date/end_date)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."
    
    # Validate required parameters
    if not keywords or keywords.strip() == "":
        return "Error: Keywords parameter is required and cannot be empty"
    
    # Use default date range (last 30 days) or provided dates
    date_range = get_default_date_range()
    
    params = {
        "app_id": app,
        "keywords": keywords.strip(),
        "country": country,
        "language": language
    }
    
    if date:
        params["date"] = date
    else:
        params["start_date"] = start_date or date_range["start_date"]
        params["end_date"] = end_date or date_range["end_date"]
    
    try:
        result = await make_api_request("/ranks/android/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch Android keyword ranks: {str(e)}"
@mcp.tool()
async def appvector_user_jobs() -> str:
    """Retrieve all jobs created by the authenticated user, grouped into Android and iOS platforms with applied feature limits"""
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."

    try:
        result = await make_api_request("/userjobs/", token, {})
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch user jobs: {str(e)}"

@mcp.tool()
async def appvector_custom_store_listings(
    app: str,
    date_from: str,
    date_to: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None
) -> str:
    """Get custom store listings performance data for an Android app

    Args:
        app: Android package name (e.g., com.app.usage.datamanager)
        date_from: Start date in YYYY-MM-DD format (required)
        date_to: End date in YYYY-MM-DD format (required)
        page: Page number for pagination (optional)
        page_size: Number of results per page (optional)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."

    # Validate required parameters
    if not date_from or not date_to:
        return "Error: date_from and date_to are required parameters in YYYY-MM-DD format"

    params = {
        "date_from": date_from,
        "date_to": date_to
    }

    # Add optional pagination parameters
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size

    try:
        result = await make_api_request(f"/user/apps/{app}/custom-store-listings/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch custom store listings: {str(e)}"

@mcp.tool()
async def appvector_csl_base_reports(
    app: str,
    date_from: str,
    date_to: str,
    search_term: List[str]
) -> str:
    """Get custom store listing base reports with search term performance data

    Args:
        app: Android package name (e.g., com.appusage.monitor)
        date_from: Start date in YYYY-MM-DD format (required)
        date_to: End date in YYYY-MM-DD format (required)
        search_term: List of search terms to analyze (at least one required)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."

    # Validate required parameters
    if not date_from or not date_to:
        return "Error: date_from and date_to are required parameters in YYYY-MM-DD format"

    if not search_term or len(search_term) == 0:
        return "Error: At least one search_term is required"

    params = {
        "date_from": date_from,
        "date_to": date_to,
        "search_term": search_term
    }

    try:
        result = await make_api_request(f"/user/apps/{app}/csl-base-reports/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch CSL base reports: {str(e)}"

@mcp.tool()
async def appvector_csl_search_terms(
    app: str,
    date_from: str,
    date_to: str,
    csl_id: List[str]
) -> str:
    """Get CSL search terms performance data for an Android app

    Args:
        app: Android package name (e.g., com.appusage.monitor)
        date_from: Start date in YYYY-MM-DD format (required)
        date_to: End date in YYYY-MM-DD format (required)
        csl_id: List of CSL IDs (at least one required)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."

    # Validate required parameters
    if not date_from or not date_to:
        return "Error: date_from and date_to are required parameters in YYYY-MM-DD format"

    if not csl_id or len(csl_id) == 0:
        return "Error: At least one csl_id is required"

    params = {
        "date_from": date_from,
        "date_to": date_to,
        "csl_id": csl_id
    }

    try:
        result = await make_api_request(f"/user/apps/{app}/csl-search-terms/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch CSL search terms: {str(e)}"

@mcp.tool()
async def appvector_localization_performance_data(
    app: str,
    date_from: str,
    date_to: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None
) -> str:
    """Get localization performance data for an Android app

    Args:
        app: Android package name (e.g., com.app.usage.datamanager)
        date_from: Start date in YYYY-MM-DD format (required)
        date_to: End date in YYYY-MM-DD format (required)
        page: Page number for pagination (optional)
        page_size: Number of results per page (optional)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."

    # Validate required parameters
    if not date_from or not date_to:
        return "Error: date_from and date_to are required parameters in YYYY-MM-DD format"

    params = {
        "date_from": date_from,
        "date_to": date_to
    }

    # Add optional pagination parameters
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size

    try:
        result = await make_api_request(f"/user/apps/{app}/localization/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch localization performance data: {str(e)}"

@mcp.tool()
async def appvector_keyword_volume(
    country: str,
    language: str,
    keywords: List[str],
    app_id: Optional[str] = None,
    ranking_odds: Optional[bool] = None
) -> str:
    """Get keyword volume and optionally ranking odds for a list of keywords

    Args:
        country: Country code (e.g., us, in, de)
        language: Language code (e.g., en, hi, de)
        keywords: List of keywords to evaluate (e.g., ["fitness app", "workout tracker"])
        app_id: App ID to fetch associated title/description for ranking odds calculation (optional)
        ranking_odds: If True, ranking odds are calculated in addition to volume (optional)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."

    # Validate required parameters
    if not country or not language:
        return "Error: country and language are required parameters"

    if not keywords or len(keywords) == 0:
        return "Error: At least one keyword is required"

    body_params = {
        "country": country,
        "language": language,
        "keywords": keywords
    }

    if app_id:
        body_params["app_id"] = app_id

    try:
        url = f"{API_URL}/keywords/volume/"
        headers = {
            "Authorization": f"Token {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        query_params = {}
        if ranking_odds is not None:
            query_params["ranking_odds"] = "1" if ranking_odds else "0"

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=body_params, params=query_params)

            if response.status_code != 200:
                raise ValueError(f"API request failed ({response.status_code}): {response.text}")

            result = response.json()
            return str(result)
    except Exception as e:
        return f"Error: Failed to fetch keyword volume: {str(e)}"

@mcp.tool()
async def appvector_keyword_ranks(
    job_id: int,
    country: str,
    language: str,
    keywords: List[str],
    ranking_odds: Optional[bool] = None
) -> str:
    """Get keyword ranks for a specific job with optional ranking odds calculation

    Args:
        job_id: Job ID associated with the keywords (e.g., 12345)
        country: Country code (e.g., us, in, de)
        language: Language code (e.g., en, hi, de)
        keywords: List of keywords to evaluate (e.g., ["fitness", "workout"])
        ranking_odds: If True, ranking odds are calculated in addition to ranks (optional)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."

    # Validate required parameters
    if not job_id:
        return "Error: job_id is required"

    if not country or not language:
        return "Error: country and language are required parameters"

    if not keywords or len(keywords) == 0:
        return "Error: At least one keyword is required"

    body_params = {
        "job_id": job_id,
        "country": country,
        "language": language,
        "keywords": keywords
    }

    try:
        url = f"{API_URL}/keywords/ranks/"
        headers = {
            "Authorization": f"Token {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        query_params = {}
        if ranking_odds is not None:
            query_params["ranking_odds"] = "1" if ranking_odds else "0"

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=body_params, params=query_params)

            if response.status_code != 200:
                raise ValueError(f"API request failed ({response.status_code}): {response.text}")

            result = response.json()
            return str(result)
    except Exception as e:
        return f"Error: Failed to fetch keyword ranks: {str(e)}"

@mcp.tool()
async def appvector_image_difference(
    app_id: str,
    competitor_app_id: str,
    country: str,
    platform: str,
    comparison_type: str
) -> str:
    """Compare visual assets (screenshots or icons) between your app and competitor apps

    Args:
        app_id: Your app ID - Android package name (e.g., com.whatsapp) or iOS app ID (e.g., 310633997)
        competitor_app_id: Comma-separated list of competitor app IDs (e.g., "com.spotify.music,com.soundcloud.android")
        country: Two-letter country code (e.g., "us", "in", "uk")
        platform: Platform type - "android" or "ios"
        comparison_type: Type of comparison - "screenshots" or "icon"
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."

    # Validate required parameters
    if not app_id or not competitor_app_id or not country or not platform or not comparison_type:
        return "Error: app_id, competitor_app_id, country, platform, and comparison_type are all required parameters"

    if platform not in ["android", "ios"]:
        return "Error: platform must be either 'android' or 'ios'"

    if comparison_type not in ["screenshots", "icon"]:
        return "Error: comparison_type must be either 'screenshots' or 'icon'"

    params = {
        "app_id": app_id,
        "competitor_app_id": competitor_app_id,
        "country": country,
        "platform": platform,
        "comparison_type": comparison_type
    }

    try:
        result = await make_api_request("/image-difference/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch image difference: {str(e)}"

@mcp.tool()
async def appvector_keyword_opportunity(
    app: str,
    start_date: str,
    end_date: str,
    country: str = "in",
    language: str = "en",
    top: Optional[int] = None
) -> str:
    """Find keyword opportunities for your app by analyzing top-ranking keywords

    Args:
        app: Your app's package name (e.g., "com.whatsapp") or iOS app ID
        start_date: Start date for the data range in YYYY-MM-DD format (e.g., "2025-01-01")
        end_date: End date for the data range in YYYY-MM-DD format (e.g., "2025-01-31")
        country: Two-letter country code (default: "in")
        language: Two-letter language code (default: "en")
        top: Number of top keywords to return (default: 1000)
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."

    # Validate required parameters
    if not app or not start_date or not end_date:
        return "Error: app, start_date, and end_date are required parameters"

    params = {
        "app": app,
        "start_date": start_date,
        "end_date": end_date,
        "country": country,
        "language": language
    }

    if top is not None:
        params["top"] = top

    try:
        result = await make_api_request("/keyword-opportunity/", token, params)
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch keyword opportunity: {str(e)}"

@mcp.tool()
async def appvector_search_apps_android(
    keyword: str,
    country: str = "in",
    language: str = "en"
) -> str:
    """Search for Android apps by keyword, package ID, or Play Store URL

    Args:
        keyword: Search term, app package ID (e.g., "com.whatsapp"), or full Play Store URL
        country: ISO country code (default: "in")
        language: ISO language code (default: "en")
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."

    # Validate required parameters
    if not keyword:
        return "Error: keyword is required"

    body_params = {
        "keyword": keyword,
        "country": country,
        "language": language
    }

    try:
        url = f"{API_URL}/search-apps/android/"
        headers = {
            "Authorization": f"Token {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=body_params)

            if response.status_code != 200:
                raise ValueError(f"API request failed ({response.status_code}): {response.text}")

            result = response.json()
            return str(result)
    except Exception as e:
        return f"Error: Failed to search Android apps: {str(e)}"

@mcp.tool()
async def appvector_search_apps_apple(
    keyword: str,
    country: str = "in",
    language: str = "en"
) -> str:
    """Search for iOS apps by keyword, app ID, or App Store URL

    Args:
        keyword: Search term, app ID (e.g., "310633997"), or full App Store URL
        country: ISO country code (default: "in")
        language: ISO language code (default: "en")
    """
    token = extract_token_from_auth()
    if not token:
        return "Error: AppVector token not provided. Please add Authorization header with your token (e.g., 'Authorization: Token YOUR_TOKEN')."

    # Validate required parameters
    if not keyword:
        return "Error: keyword is required"

    body_params = {
        "keyword": keyword,
        "country": country,
        "language": language
    }

    try:
        url = f"{API_URL}/search-apps/apple/"
        headers = {
            "Authorization": f"Token {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=body_params)

            if response.status_code != 200:
                raise ValueError(f"API request failed ({response.status_code}): {response.text}")

            result = response.json()
            return str(result)
    except Exception as e:
        return f"Error: Failed to search Apple apps: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=3000)