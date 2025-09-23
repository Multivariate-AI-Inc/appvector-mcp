# AppVector MCP Server

MCP server for accessing AppVector external APIs, providing app metadata and ranking data for Apple App Store and Google Play Store.

## Features

- **Apple App Store**: Metadata history and category rankings
- **Google Play Store**: Metadata history and category rankings
- **Configurable**: URL and authentication via environment variables
- **Date Range Support**: Query historical data with custom date ranges

## Installation

### Prerequisites

- **Node.js 18 or higher** (Required by MCP SDK)
- npm or yarn
- Git (for version control)

⚠️ **Important**: This MCP server requires Node.js version 18 or higher. Check your version with `node --version`.

### Setup for AppVector mcp server

1. Clone the repository (you must have access):

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
   - Edit `.env` and add your API token (obtain your Appvector token from [here](https://appvector.io/users/get_token/)):
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
# e.g claude mcp add appvector node /Users/<your-user>/Desktop/appvector-mcp/dist/index.js
claude mcp add appvector node <path-to-your-project>/appvector-mcp/dist/index.js

```

### Add to Claude Desktop

From the main MCP directory

```
"appvector-mcp": {
      "command": "node",
      "args": [
        "<PROJECT_PATH>/dist/index.js"
      ]
    }
```

Replace `<PROJECT_PATH>` with AppVector MCP directory full path.

## Available Tools

### 1. `appvector_apple_metadata`

Get Apple App Store metadata history.

**Parameters:**

- `app` (required): Apple app ID (e.g., "284882215")
- `data`: Metadata type - title, description, media, genre, developer, ratings, price, version (default: "title")
- `country`: Country code (default: "in")
- `language`: Language code (default: "en")
- `start_date`: YYYY-MM-DD format (default: 30 days ago)
- `end_date`: YYYY-MM-DD format (default: today)

### 2. `appvector_apple_rank`

Get Apple App Store category rank history.

**Parameters:**

- `app` (required): Apple app ID (e.g., "1386412985")
- `country`: Country code (default: "in")
- `start_date`: YYYY-MM-DD format (default: 30 days ago)
- `end_date`: YYYY-MM-DD format (default: today)

### 3. `appvector_android_metadata`

Get Google Play Store metadata history.

**Parameters:**

- `app` (required): Android package name (e.g., "com.spotify.music")
- `data`: Metadata type - title, description, media, install, ratings, genre, developer, price, events, version (default: "title")
- `country`: Country code (default: "in")
- `language`: Language code (default: "en")
- `start_date`: YYYY-MM-DD format (default: 30 days ago)
- `end_date`: YYYY-MM-DD format (default: today)

### 4. `appvector_android_rank`

Get Google Play Store category rank.

**Parameters:**

- `app` (required): Android package name (e.g., "com.spotify.music")
- `country`: Country code (default: "in")
- `start_date`: YYYY-MM-DD format (default: 30 days ago)
- `end_date`: YYYY-MM-DD format (default: today)

## Usage Examples

### Get Apple app title history:

```
Use tool: appvector_apple_metadata
Arguments: {
  "app": "284882215",
  "data": "title",
  "country": "us"
}
```

### Get Android app rankings:

```
Use tool: appvector_android_rank
Arguments: {
  "app": "com.spotify.music",
  "country": "in",
  "start_date": "2025-08-01",
  "end_date": "2025-08-31"
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
