#!/usr/bin/env python3
"""
Uvicorn configuration for AppVector FastMCP Server
Production-ready deployment configuration
"""

import os
from uvicorn.workers import UvicornWorker

# Server configuration
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = int(os.environ.get('WORKERS', '1'))
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5

# Logging
loglevel = os.environ.get('LOG_LEVEL', 'info')
accesslog = "-"
errorlog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "appvector-mcp-server"

# Preload app
preload_app = True

# SSL (if needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"