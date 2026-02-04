#!/bin/bash
set -e

echo "Building Kong MCP Server..."
docker build -t kong-mcp-server .

echo ""
echo "✓ Build successful!"
echo ""
echo "Next steps:"
echo "1. Add to ~/.kiro/settings/mcp_config.json:"
echo ""
cat << 'EOF'
{
  "mcpServers": {
    "kong": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--network=host",
        "-e", "KONG_ADMIN_URL=http://localhost:8001",
        "kong-mcp-server"
      ]
    }
  }
}
EOF
echo ""
echo "2. Restart Kiro CLI"
echo "3. Test with: 'Liste os services do Kong'"
