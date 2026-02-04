# Kong MCP Server

MCP server for Kong Gateway administration via Admin API.

## Features

- Complete CRUD operations for services, routes, upstreams, and targets
- Simplified configuration for common plugins (rate-limiting, CORS, authentication, etc.)
- Multi-environment support (local/dev/staging/prod)
- Docker-based for easy distribution
- No Python/venv setup required

## Installation via Docker (Recommended)

### Build the image:
```bash
./setup.sh
# or manually:
docker build -t kong-mcp-server .
```

**IMPORTANT:** Do not try to run the container directly. It only works when called by Kiro CLI via stdio.

## Configuration in Kiro CLI

Add to `~/.kiro/settings/mcp_config.json`:

```json
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
```

### Or using Docker Compose:

```bash
docker compose up -d
```

And configure in Kiro:
```json
{
  "mcpServers": {
    "kong": {
      "command": "docker",
      "args": ["exec", "-i", "kong-mcp-server", "python", "kong_mcp_server.py"]
    }
  }
}
```

## Distribution to Team

### Option 1: Docker Hub
```bash
docker tag kong-mcp-server your-username/kong-mcp-server:latest
docker push your-username/kong-mcp-server:latest
```

Team uses:
```json
{
  "mcpServers": {
    "kong": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--network=host", "your-username/kong-mcp-server"]
    }
  }
}
```

### Option 2: Private Registry
```bash
docker tag kong-mcp-server registry.company.com/kong-mcp-server:latest
docker push registry.company.com/kong-mcp-server:latest
```

### Option 3: Tar file
```bash
docker save kong-mcp-server > kong-mcp-server.tar
# Distribute the file

# Team loads:
docker load < kong-mcp-server.tar
```

## Environment Variables

- `KONG_ADMIN_URL` - Kong Admin API URL (default: `http://localhost:8001`)
- `KONG_ENV` - Environment identifier (local/dev/staging/prod) (default: `local`)

Copy `.env.example` to `.env` and adjust as needed.

## Available Tools

### Services (Complete CRUD)
- `kong_list_services` - List all services
- `kong_get_service` - Get details of a specific service
- `kong_create_service` - Create a new service
- `kong_update_service` - Update an existing service
- `kong_delete_service` - Delete a service

### Routes (Complete CRUD)
- `kong_list_routes` - List all routes
- `kong_get_route` - Get details of a specific route
- `kong_create_route` - Create a route for a service
- `kong_update_route` - Update an existing route
- `kong_delete_route` - Delete a route

### Upstreams & Targets
- `kong_list_upstreams` - List upstreams
- `kong_get_upstream` - Get details of a specific upstream
- `kong_create_upstream` - Create upstream with load balancing
- `kong_delete_upstream` - Delete an upstream
- `kong_list_targets` - List targets of an upstream
- `kong_add_target` - Add target to an upstream
- `kong_delete_target` - Delete target from an upstream

### Generic Plugins
- `kong_list_plugins` - List enabled plugins
- `kong_delete_plugin` - Delete a plugin

### Specific Plugins (Simplified Configuration)
- `kong_enable_rate_limiting` - Rate limiting (per second/minute/hour/day)
- `kong_enable_cors` - CORS (origins, methods, headers, credentials)
- `kong_enable_key_auth` - API key authentication
- `kong_enable_jwt` - JWT authentication
- `kong_enable_ip_restriction` - IP restriction (allow/deny)
- `kong_enable_request_transformer` - Request transformation (headers, querystring)

## Usage Examples

In Kiro CLI:

**Services & Routes:**
```
Create a service called "api-backend" pointing to http://api.example.com
```

```
Create a route /v1/users with GET and POST methods for the api-backend service
```

```
Update the api-backend service to point to http://new-api.example.com
```

**Upstreams & Load Balancing:**
```
Create an upstream "backend-pool" with round-robin algorithm and add targets 10.0.1.10:8080 and 10.0.1.11:8080
```

```
List all targets of the backend-pool upstream
```

**Plugins:**
```
Enable rate limiting of 100 requests per minute on the api-backend service
```

```
Enable CORS allowing origins https://app.example.com and https://admin.example.com
```

```
Enable API key authentication on the /v1/users route
```

```
Enable IP restriction allowing only 10.0.0.0/8 and 192.168.1.0/24
```

## Disclaimer

This project is provided "as is" without warranty of any kind, express or implied. The authors and contributors are not responsible for any damages or issues arising from the use of this software. Use at your own risk.

This is an unofficial community project and is not affiliated with or endorsed by Kong Inc.

## License

MIT
