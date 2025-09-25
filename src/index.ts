#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema
} from '@modelcontextprotocol/sdk/types.js';
import dotenv from 'dotenv';
import express from 'express';
import cors from 'cors';
import { AppleMetadataHandler } from './handlers/appleMetadata.js';
import { AppleRankHandler } from './handlers/appleRank.js';
import { AndroidMetadataHandler } from './handlers/androidMetadata.js';
import { AndroidRankHandler } from './handlers/androidRank.js';
import { KeywordResearchHandler } from './handlers/keywordResearch.js';
import { AppleReviewsHandler } from './handlers/appleReviews.js';
import { AndroidReviewsHandler } from './handlers/androidReviews.js';
import { AppleKeywordRankHandler } from './handlers/appleKeywordRank.js';
import { AndroidKeywordRankHandler } from './handlers/androidKeywordRank.js';
import { UserJobsHandler } from './handlers/userJobs.js';

// Load environment variables
// Use ENV_PATH if set, otherwise fall back to `.env` in the project root
const envPath = process.env.ENV_PATH || ".env";
dotenv.config({ path: envPath });

// API configuration
const API_URL = "https://appvector.io/external-apis/api";
const API_TOKEN = process.env.APPVECTOR_TOKEN || "";

if (!API_TOKEN) {
  console.warn("⚠️  APPVECTOR_TOKEN is missing. Please set it in your .env file.");
}

// Initialize handlers
const appleMetadataHandler = new AppleMetadataHandler(API_URL, API_TOKEN);
const appleRankHandler = new AppleRankHandler(API_URL, API_TOKEN);
const androidMetadataHandler = new AndroidMetadataHandler(API_URL, API_TOKEN);
const androidRankHandler = new AndroidRankHandler(API_URL, API_TOKEN);
const keywordResearchHandler = new KeywordResearchHandler(API_URL, API_TOKEN);
const appleReviewsHandler = new AppleReviewsHandler(API_URL, API_TOKEN);
const androidReviewsHandler = new AndroidReviewsHandler(API_URL, API_TOKEN);
const appleKeywordRankHandler = new AppleKeywordRankHandler(API_URL, API_TOKEN);
const androidKeywordRankHandler = new AndroidKeywordRankHandler(API_URL, API_TOKEN);
const userJobsHandler = new UserJobsHandler(API_URL, API_TOKEN);

// Create server instance
const server = new Server(
  {
    name: 'appvector-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define tools
const tools = [
  {
    name: 'appvector_apple_metadata',
    description: 'Get Apple App Store metadata history (title, description, media, genre, developer, ratings, price, version)',
    inputSchema: {
      type: 'object',
      properties: {
        app: {
          type: 'string',
          description: 'Apple app ID (e.g., 284882215)'
        },
        data: {
          type: 'string',
          description: 'Type of metadata: title, description, media, genre, developer, ratings, price, version',
          enum: ['title', 'description', 'media', 'genre', 'developer', 'ratings', 'price', 'version']
        },
        country: {
          type: 'string',
          description: 'Country code (default: in)',
          default: 'in'
        },
        language: {
          type: 'string',
          description: 'Language code (default: en)',
          default: 'en'
        },
        start_date: {
          type: 'string',
          description: 'Start date in YYYY-MM-DD format (default: 30 days ago)'
        },
        end_date: {
          type: 'string',
          description: 'End date in YYYY-MM-DD format (default: today)'
        }
      },
      required: ['app']
    }
  },
  {
    name: 'appvector_apple_rank',
    description: 'Get Apple App Store category rank history',
    inputSchema: {
      type: 'object',
      properties: {
        app: {
          type: 'string',
          description: 'Apple app ID (e.g., 1386412985)'
        },
        country: {
          type: 'string',
          description: 'Country code (default: in)',
          default: 'in'
        },
        start_date: {
          type: 'string',
          description: 'Start date in YYYY-MM-DD format (default: 30 days ago)'
        },
        end_date: {
          type: 'string',
          description: 'End date in YYYY-MM-DD format (default: today)'
        }
      },
      required: ['app']
    }
  },
  {
    name: 'appvector_android_metadata',
    description: 'Get Google Play Store metadata history (title, description, media, install, ratings, genre, developer, price, events, version)',
    inputSchema: {
      type: 'object',
      properties: {
        app: {
          type: 'string',
          description: 'Android package name (e.g., com.spotify.music)'
        },
        data: {
          type: 'string',
          description: 'Type of metadata: title, description, media, install, ratings, genre, developer, price, events, version',
          enum: ['title', 'description', 'media', 'install', 'ratings', 'genre', 'developer', 'price', 'events', 'version']
        },
        country: {
          type: 'string',
          description: 'Country code (default: in)',
          default: 'in'
        },
        language: {
          type: 'string',
          description: 'Language code (default: en)',
          default: 'en'
        },
        start_date: {
          type: 'string',
          description: 'Start date in YYYY-MM-DD format (default: 30 days ago)'
        },
        end_date: {
          type: 'string',
          description: 'End date in YYYY-MM-DD format (default: today)'
        }
      },
      required: ['app']
    }
  },
  {
    name: 'appvector_android_rank',
    description: 'Get Google Play Store category rank',
    inputSchema: {
      type: 'object',
      properties: {
        app: {
          type: 'string',
          description: 'Android package name (e.g., com.spotify.music)'
        },
        country: {
          type: 'string',
          description: 'Country code (default: in)',
          default: 'in'
        },
        start_date: {
          type: 'string',
          description: 'Start date in YYYY-MM-DD format (default: 30 days ago)'
        },
        end_date: {
          type: 'string',
          description: 'End date in YYYY-MM-DD format (default: today)'
        }
      },
      required: ['app']
    }
  },
  {
    name: 'appvector_keyword_research',
    description: 'Generate keyword suggestions for a list of base keywords',
    inputSchema: {
      type: 'object',
      properties: {
        keywords: {
          type: 'array',
          items: { type: 'string' },
          description: 'List of base keywords'
        },
        country: {
          type: 'string',
          default: 'in',
          description: 'Country code'
        },
        language: {
          type: 'string',
          default: 'en',
          description: 'Language code'
        },
        platform: {
          type: 'string',
          enum: ['android', 'ios'],
          default: 'android',
          description: 'Platform'
        }
      },
      required: ['keywords']
    }
  },
  {
    name: 'appvector_apple_reviews',
    description: 'Get Apple app user reviews history',
    inputSchema: {
      type: 'object',
      properties: {
        app: {
          type: 'string',
          description: 'Apple app ID (e.g., 281796108)'
        },
        country: {
          type: 'string',
          default: 'in',
          description: 'Country code (default: in)'
        },
        start_date: {
          type: 'string',
          description: 'Start date in YYYY-MM-DD format (default: 30 days ago)'
        },
        end_date: {
          type: 'string',
          description: 'End date in YYYY-MM-DD format (default: today)'
        }
      },
      required: ['app']
    }
  },
  {
    name: 'appvector_android_reviews',
    description: 'Get Android app user reviews history',
    inputSchema: {
      type: 'object',
      properties: {
        app: {
          type: 'string',
          description: 'Android package name (e.g., com.facebook.katana)'
        },
        language: {
          type: 'string',
          default: 'en',
          description: 'Language code (default: en)'
        },
        start_date: {
          type: 'string',
          description: 'Start date in YYYY-MM-DD format (default: 30 days ago)'
        },
        end_date: {
          type: 'string',
          description: 'End date in YYYY-MM-DD format (default: today)'
        }
      },
      required: ['app']
    }
  },
  {
    name: 'appvector_apple_keyword_rank',
    description: 'Get Apple app keyword ranking history',
    inputSchema: {
      type: 'object',
      properties: {
        app: {
          type: 'string',
          description: 'Apple app ID (e.g., 284882215)'
        },
        keywords: {
          type: 'string',
          description: 'Comma-separated keywords to track rankings for'
        },
        country: {
          type: 'string',
          description: 'Country code (default: in)',
          default: 'in'
        },
        language: {
          type: 'string',
          description: 'Language code (default: en)',
          default: 'en'
        },
        start_date: {
          type: 'string',
          description: 'Start date in YYYY-MM-DD format (default: 30 days ago)'
        },
        end_date: {
          type: 'string',
          description: 'End date in YYYY-MM-DD format (default: today)'
        },
        date: {
          type: 'string',
          description: 'Specific date in YYYY-MM-DD format (alternative to start_date/end_date)'
        }
      },
      required: ['app', 'keywords']
    }
  },
  {
    name: 'appvector_android_keyword_rank',
    description: 'Get Android app keyword ranking history',
    inputSchema: {
      type: 'object',
      properties: {
        app: {
          type: 'string',
          description: 'Android package name (e.g., com.spotify.music)'
        },
        keywords: {
          type: 'string',
          description: 'Comma-separated keywords to track rankings for'
        },
        country: {
          type: 'string',
          description: 'Country code (default: in)',
          default: 'in'
        },
        language: {
          type: 'string',
          description: 'Language code (default: en)',
          default: 'en'
        },
        start_date: {
          type: 'string',
          description: 'Start date in YYYY-MM-DD format (default: 30 days ago)'
        },
        end_date: {
          type: 'string',
          description: 'End date in YYYY-MM-DD format (default: today)'
        },
        date: {
          type: 'string',
          description: 'Specific date in YYYY-MM-DD format (alternative to start_date/end_date)'
        }
      },
      required: ['app', 'keywords']
    }
  },
  {
    name: 'appvector_user_jobs',
    description: 'Retrieve all jobs created by the authenticated user, grouped into Android and iOS platforms with applied feature limits',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    }
  }
];

// Handle list tools request
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'appvector_apple_metadata':
        return await appleMetadataHandler.handle(args);
      
      case 'appvector_apple_rank':
        return await appleRankHandler.handle(args);
      
      case 'appvector_android_metadata':
        return await androidMetadataHandler.handle(args);
      
      case 'appvector_android_rank':
        return await androidRankHandler.handle(args);

      case 'appvector_keyword_research':
        return await keywordResearchHandler.handle(args);

      case 'appvector_apple_reviews':
        return await appleReviewsHandler.handle(args);

      case 'appvector_android_reviews':
        return await androidReviewsHandler.handle(args);

      case 'appvector_apple_keyword_rank':
        return await appleKeywordRankHandler.handle(args);

      case 'appvector_android_keyword_rank':
        return await androidKeywordRankHandler.handle(args);

      case 'appvector_user_jobs':
        return await userJobsHandler.handle(args);

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error instanceof Error ? error.message : String(error)}`
        }
      ]
    };
  }
});

// Start the server
async function main() {
  const app = express();
  const port = process.env.PORT || 3000;

  // Enable CORS for all routes
  app.use(cors());
  
  // Parse JSON bodies
  app.use(express.json());
  
  // Health check endpoint
  app.get('/health', (req, res) => {
    res.json({ status: 'healthy', name: 'appvector-mcp', version: '1.0.0' });
  });

  // Create Streamable HTTP transport
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: () => `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
  });
  await server.connect(transport);
  
  // Handle MCP requests on /mcp endpoint
  app.all('/mcp', (req, res) => {
    transport.handleRequest(req, res, req.body);
  });
  
  // Start the HTTP server
  app.listen(port, () => {
    console.log(`AppVector MCP server running on port ${port}`);
    console.log(`Health check: http://localhost:${port}/health`);
    console.log(`MCP endpoint: http://localhost:${port}/mcp`);
  });
}

main().catch((error) => {
  console.error('Failed to start server:', error);
  process.exit(1);
});