# AppVector MCP Server For ASO Tools

MCP server for accessing AppVector APIs, providing app metadata, ranking data, and ASO keyword research capabilities for Apple App Store and Google Play Store optimization.

[![Node.js](https://img.shields.io/badge/Node.js-18+-green)](https://nodejs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue)](https://www.typescriptlang.org)
[![MCP](https://img.shields.io/badge/MCP-Compatible-orange)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/License-Proprietary-red)](./LICENSE)
[![Free to Use](https://img.shields.io/badge/Access-AppVector%20Account-green)](https://appvector.io)

## Features

This app store optimization platform provides ASO tools and keyword research functionality through a standardized MCP interface:

- **Apple App Store optimization**: Metadata history and category ranking analysis
- **Google Play ASO tools**: Android app metadata and ranking tracking
- **ASO keyword research**: Historical keyword performance and ranking data
- **App store ranking tracker**: Multi-country ranking monitoring
- **App store localization**: Multi-language and regional optimization data
- **Historical ASO data**: Custom date range queries for app store optimization metrics
- **App store intelligence**: Analytics and competitive analysis tools

## Use Cases

- ASO keyword research and optimization workflows
- App store ranking analysis and monitoring
- Competitive intelligence for mobile app optimization
- Historical trend analysis for app store performance
- Multi-market app store optimization strategies
- Automated ASO reporting and analytics

## Installation

### Prerequisites
- **Node.js 18 or higher** (Required by MCP SDK)
- npm or yarn
- Git

⚠️ **Important**: This MCP server requires Node.js version 18 or higher. Check your version with `node --version`.

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Multivariate-AI-Inc/appvector-mcp.git
cd appvector-mcp
```

2. Install dependencies:
```bash
npm install
```

3. Build the TypeScript code:
```bash
npm run build
```

4. Configure environment variables:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your API token (obtain your AppVector token from [here](https://appvector.io/users/get_token/)):
     ```env
     APPVECTOR_TOKEN=your_api_token_here
     ```

5. Install pre-commit hooks for security:
```bash
npm install
npm run prepare
```

### Add to Claude

From the main MCP directory:
```bash
# Replace <path-to-your-project> with the full path where your repo is located
# Example: claude mcp add appvector node /Users/developer/appvector-mcp/dist/index.js
claude mcp add appvector node <path-to-your-project>/appvector-mcp/dist/index.js
```

## Available Tools

### 1. `appvector_apple_metadata`
Get Apple App Store metadata history for ASO keyword research and app store optimization.

**Parameters:**
- `app` (required): Apple app ID (e.g., "284882215")
- `data`: Metadata type - title, description, media, genre, developer, ratings, price, version (default: "title")
- `country`: Country code (default: "in")
- `language`: Language code (default: "en")
- `start_date`: YYYY-MM-DD format (default: 30 days ago)
- `end_date`: YYYY-MM-DD format (default: today)

### 2. `appvector_apple_rank`
Get Apple App Store category rank history for app store ranking tracker functionality.

**Parameters:**
- `app` (required): Apple app ID (e.g., "1386412985")
- `country`: Country code (default: "in")
- `start_date`: YYYY-MM-DD format (default: 30 days ago)
- `end_date`: YYYY-MM-DD format (default: today)

### 3. `appvector_android_metadata`
Get Google Play Store metadata history for Android ASO tools and app store optimization.

**Parameters:**
- `app` (required): Android package name (e.g., "com.spotify.music")
- `data`: Metadata type - title, description, media, install, ratings, genre, developer, price, events, version (default: "title")
- `country`: Country code (default: "in")
- `language`: Language code (default: "en")
- `start_date`: YYYY-MM-DD format (default: 30 days ago)
- `end_date`: YYYY-MM-DD format (default: today)

### 4. `appvector_android_rank`
Get Google Play Store category rank for Google Play ASO tool and ranking analysis.

**Parameters:**
- `app` (required): Android package name (e.g., "com.spotify.music")
- `country`: Country code (default: "in")
- `start_date`: YYYY-MM-DD format (default: 30 days ago)
- `end_date`: YYYY-MM-DD format (default: today)

## Usage Examples

### Get Apple App Store metadata:
```javascript
Use tool: appvector_apple_metadata
Arguments: {
  "app": "284882215",
  "data": "title",
  "country": "us"
}
```

### Track Android app rankings:
```javascript
Use tool: appvector_android_rank
Arguments: {
  "app": "com.spotify.music",
  "country": "in",
  "start_date": "2025-08-01",
  "end_date": "2025-08-31"
}
```

### Historical metadata analysis:
```javascript
Use tool: appvector_apple_metadata
Arguments: {
  "app": "your_app_id",
  "data": "description",
  "country": "us",
  "language": "en",
  "start_date": "2025-01-01",
  "end_date": "2025-09-26"
}
```

## Development

### Run in development mode:
```bash
npm run dev
```

### Build for production:
```bash
npm run build
```

### Start production server:
```bash
npm start
```

### Security check:
```bash
npm run security-check
```

## Troubleshooting

1. **Authentication errors**: Verify APPVECTOR_TOKEN is set correctly in .env
2. **Network errors**: Check API URL and network connectivity
3. **Invalid parameters**: Ensure app IDs and country codes are valid
4. **Date errors**: Dates must be in YYYY-MM-DD format, no future dates allowed
5. **Pre-commit failures**: Run `npm run security-check` to identify issues
6. **Environment not loading**: Check ENV_PATH or use default location

## ASO Best Practices

When using this app store optimization platform, consider these guidelines:

- **ASO keyword research**: Focus on high-volume, low-competition keywords for better app store visibility
- **App store screenshots**: Follow Apple and Google Play screenshot guidelines for optimal performance
- **App store localization**: Implement multi-language optimization for global reach
- **App store conversion optimization**: Monitor conversion rates to improve listing performance
- **Competitive analysis**: Use ranking data to monitor competitor performance
- **Algorithm awareness**: Stay updated with app store ranking algorithm changes

## API Integration

This MCP server provides standardized access to AppVector's ASO tools and app store optimization data through:

- RESTful API endpoints for app store metadata
- Historical ranking data for trend analysis
- Multi-platform support (iOS and Android)
- Configurable date ranges and localization options
- Structured JSON responses for easy integration

## Usage & Access

This MCP server is **free to use** with a valid AppVector account. API limits and features depend on your active AppVector plan.

**Copyright © 2025 Multivariate AI Private Limited. All rights reserved.**

### Getting Started

1. **Sign up for AppVector**: [appvector.io](https://appvector.io)
2. **Get your API token**: [appvector.io/users/get_token/](https://appvector.io/users/get_token/)
3. **Configure the MCP server** with your token
4. **Start using ASO tools** based on your plan limits

### AppVector Plans

- **Free Plan**: Basic ASO keyword research and limited API calls
- **Pro Plan**: Advanced features and higher API limits
- **Enterprise Plan**: Full access and unlimited API usage

**Note**: API usage limits and available features are determined by your active AppVector subscription plan.

---

For more information about AppVector's app store optimization platform, visit [appvector.io](https://appvector.io).
