#!/bin/bash

# Setup Python FastMCP Server
echo "Setting up AppVector FastMCP Server..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make the server executable
chmod +x src/fastmcp_server.py

echo "✅ Setup complete!"
echo ""
echo "To run the server:"
echo "  source venv/bin/activate"
echo "  python src/fastmcp_server.py"
echo ""
echo "Or with FastMCP:"
echo "  fastmcp run src/fastmcp_server.py"