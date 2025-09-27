# Multi-MCP Server Deployment Guide

This setup runs both AppVector MCP and Gamma MCP servers using Docker Compose with Caddy as reverse proxy.

## Services

- **appvector-mcp**: Original MCP server (port 3000)
  - Domain: `appvector-mcp.example.com`
  - Endpoint: `/mcp`

- **gamma-mcp**: Gamma AI presentation generator MCP (port 8000)
  - Domain: `gamma-mcp.example.com`
  - Endpoint: `/mcp`

- **caddy**: Reverse proxy with automatic HTTPS
  - Ports: 80 (HTTP), 443 (HTTPS)

## Prerequisites

1. **Domain Setup**: Point both domains to your server IP:
   ```
   appvector-mcp.example.com -> YOUR_SERVER_IP
   gamma-mcp.example.com -> YOUR_SERVER_IP
   ```

2. **Firewall**: Open ports 80 and 443 on your server

## Deployment Steps

### 1. Deploy Both Services

```bash
cd /path/to/appvector-mcp
docker-compose up -d
```

### 2. Check Service Status

```bash
# Check all services
docker-compose ps

# Check logs
docker-compose logs -f appvector-mcp
docker-compose logs -f gamma-mcp
docker-compose logs -f caddy
```

### 3. Health Checks

```bash
# AppVector MCP health
curl -f http://localhost:3000/mcp || echo "AppVector MCP not ready"

# Gamma MCP health  
curl -f http://localhost:8000/mcp || echo "Gamma MCP not ready"

# External access (replace with your domains)
curl https://appvector-mcp.example.com/mcp
curl https://gamma-mcp.example.com/mcp
```

## Usage

### AppVector MCP
```json
{
  "mcpServers": {
    "appvector": {
      "url": "https://appvector-mcp.example.com/mcp"
    }
  }
}
```

### Gamma MCP
```json
{
  "mcpServers": {
    "gamma": {
      "url": "https://gamma-mcp.example.com/mcp",
      "headers": {
        "API_KEY": "sk-gamma-your-key-here"
      }
    }
  }
}
```

## Troubleshooting

### Service Won't Start
```bash
# Rebuild specific service
docker-compose build appvector-mcp
docker-compose build gamma-mcp

# Force recreate
docker-compose up -d --force-recreate
```

### Check Internal Network
```bash
# Test internal connectivity
docker-compose exec caddy wget -q -O- http://appvector-mcp:3000/mcp
docker-compose exec caddy wget -q -O- http://gamma-mcp:8000/mcp
```

### SSL Issues
```bash
# Check Caddy SSL status
docker-compose exec caddy caddy trust
docker-compose logs caddy | grep -i cert
```

### View Real-time Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f gamma-mcp
```

## File Structure
```
appvector-mcp/
├── docker-compose.yml       # Multi-service orchestration
├── Caddyfile               # Reverse proxy config
├── Dockerfile              # AppVector MCP image
├── fastmcp_server.py       # AppVector MCP source
├── requirements.txt        # AppVector dependencies
└── DEPLOYMENT.md           # This file

gamma-mcp/
├── Dockerfile              # Gamma MCP image
├── mcp_gamma/              # Gamma MCP source
├── pyproject.toml          # Gamma dependencies
└── ...
```

## Updating Services

### Update AppVector MCP
```bash
docker-compose build appvector-mcp
docker-compose up -d appvector-mcp
```

### Update Gamma MCP
```bash
docker-compose build gamma-mcp
docker-compose up -d gamma-mcp
```

### Update Both
```bash
docker-compose build
docker-compose up -d
```

## Monitoring

### Resource Usage
```bash
docker stats
```

### Service Health
```bash
# AppVector MCP functions
curl -X POST https://appvector-mcp.example.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'

# Gamma MCP functions  
curl -X POST https://gamma-mcp.example.com/mcp \
  -H "Content-Type: application/json" \
  -H "API_KEY: sk-gamma-your-key" \
  -d '{"method": "tools/list"}'
```

## Production Considerations

1. **Environment Variables**: Use `.env` files for sensitive configs
2. **Backup**: Regular backup of Caddy data volume
3. **Monitoring**: Set up health check alerts
4. **Scaling**: Consider load balancing for high traffic
5. **Security**: Regular security updates for base images