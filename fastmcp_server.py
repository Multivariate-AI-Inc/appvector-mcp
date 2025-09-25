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
        # This endpoint might use POST
        url = f"{API_URL}/keyword/research/"
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
    
    date_range = get_default_date_range()
    params = {
        "app": app,
        "keywords": keywords,
        "country": country,
        "language": language
    }
    
    if date:
        params["date"] = date
    else:
        params["start_date"] = start_date or date_range["start_date"]
        params["end_date"] = end_date or date_range["end_date"]
    
    try:
        result = await make_api_request("/keyword/rank/apple/", token, params)
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
    
    date_range = get_default_date_range()
    params = {
        "app": app,
        "keywords": keywords,
        "country": country,
        "language": language
    }
    
    if date:
        params["date"] = date
    else:
        params["start_date"] = start_date or date_range["start_date"]
        params["end_date"] = end_date or date_range["end_date"]
    
    try:
        result = await make_api_request("/keyword/rank/android/", token, params)
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
        result = await make_api_request("/user/jobs/", token, {})
        return str(result)
    except Exception as e:
        return f"Error: Failed to fetch user jobs: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=3000)