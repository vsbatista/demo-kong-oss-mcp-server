import asyncio
import httpx
import os
from mcp.server import Server
from mcp.types import Tool, TextContent
from typing import Any

# Configuração via environment variables
KONG_ADMIN_URL = os.getenv("KONG_ADMIN_URL", "http://localhost:8001")
KONG_ENV = os.getenv("KONG_ENV", "local")  # local, dev, staging, prod

app = Server("kong-mcp-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # Services
        Tool(
            name="kong_list_services",
            description="List all Kong services",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="kong_get_service",
            description="Get details of a specific service",
            inputSchema={
                "type": "object",
                "required": ["service_id"],
                "properties": {"service_id": {"type": "string"}}
            }
        ),
        Tool(
            name="kong_create_service",
            description="Create a new Kong service",
            inputSchema={
                "type": "object",
                "required": ["name", "url"],
                "properties": {
                    "name": {"type": "string"},
                    "url": {"type": "string", "description": "Backend URL (e.g., http://api.example.com)"}
                }
            }
        ),
        Tool(
            name="kong_update_service",
            description="Update an existing service",
            inputSchema={
                "type": "object",
                "required": ["service_id"],
                "properties": {
                    "service_id": {"type": "string"},
                    "name": {"type": "string"},
                    "url": {"type": "string"}
                }
            }
        ),
        Tool(
            name="kong_delete_service",
            description="Delete a Kong service by name or ID",
            inputSchema={
                "type": "object",
                "required": ["service_id"],
                "properties": {"service_id": {"type": "string"}}
            }
        ),
        
        # Routes
        Tool(
            name="kong_list_routes",
            description="List all Kong routes",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="kong_get_route",
            description="Get details of a specific route",
            inputSchema={
                "type": "object",
                "required": ["route_id"],
                "properties": {"route_id": {"type": "string"}}
            }
        ),
        Tool(
            name="kong_create_route",
            description="Create a route for a service",
            inputSchema={
                "type": "object",
                "required": ["service_id", "paths"],
                "properties": {
                    "service_id": {"type": "string"},
                    "paths": {"type": "array", "items": {"type": "string"}},
                    "methods": {"type": "array", "items": {"type": "string"}}
                }
            }
        ),
        Tool(
            name="kong_update_route",
            description="Update an existing route",
            inputSchema={
                "type": "object",
                "required": ["route_id"],
                "properties": {
                    "route_id": {"type": "string"},
                    "paths": {"type": "array", "items": {"type": "string"}},
                    "methods": {"type": "array", "items": {"type": "string"}}
                }
            }
        ),
        Tool(
            name="kong_delete_route",
            description="Delete a route",
            inputSchema={
                "type": "object",
                "required": ["route_id"],
                "properties": {"route_id": {"type": "string"}}
            }
        ),
        
        # Upstreams
        Tool(
            name="kong_list_upstreams",
            description="List all Kong upstreams",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="kong_get_upstream",
            description="Get details of a specific upstream",
            inputSchema={
                "type": "object",
                "required": ["upstream_id"],
                "properties": {"upstream_id": {"type": "string"}}
            }
        ),
        Tool(
            name="kong_create_upstream",
            description="Create an upstream with load balancing",
            inputSchema={
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string"},
                    "algorithm": {"type": "string", "enum": ["round-robin", "consistent-hashing", "least-connections"]}
                }
            }
        ),
        Tool(
            name="kong_delete_upstream",
            description="Delete an upstream",
            inputSchema={
                "type": "object",
                "required": ["upstream_id"],
                "properties": {"upstream_id": {"type": "string"}}
            }
        ),
        
        # Targets
        Tool(
            name="kong_list_targets",
            description="List all targets of an upstream",
            inputSchema={
                "type": "object",
                "required": ["upstream_id"],
                "properties": {"upstream_id": {"type": "string"}}
            }
        ),
        Tool(
            name="kong_add_target",
            description="Add a target to an upstream",
            inputSchema={
                "type": "object",
                "required": ["upstream_id", "target"],
                "properties": {
                    "upstream_id": {"type": "string"},
                    "target": {"type": "string", "description": "host:port"}
                }
            }
        ),
        Tool(
            name="kong_delete_target",
            description="Delete a target from an upstream",
            inputSchema={
                "type": "object",
                "required": ["upstream_id", "target_id"],
                "properties": {
                    "upstream_id": {"type": "string"},
                    "target_id": {"type": "string"}
                }
            }
        ),
        
        # Plugins - Generic
        Tool(
            name="kong_list_plugins",
            description="List all enabled plugins",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="kong_delete_plugin",
            description="Delete a plugin",
            inputSchema={
                "type": "object",
                "required": ["plugin_id"],
                "properties": {"plugin_id": {"type": "string"}}
            }
        ),
        
        # Plugins - Specific
        Tool(
            name="kong_enable_rate_limiting",
            description="Enable rate limiting plugin on a service or route",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_id": {"type": "string"},
                    "route_id": {"type": "string"},
                    "second": {"type": "integer"},
                    "minute": {"type": "integer"},
                    "hour": {"type": "integer"},
                    "day": {"type": "integer"}
                }
            }
        ),
        Tool(
            name="kong_enable_cors",
            description="Enable CORS plugin on a service or route",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_id": {"type": "string"},
                    "route_id": {"type": "string"},
                    "origins": {"type": "array", "items": {"type": "string"}},
                    "methods": {"type": "array", "items": {"type": "string"}},
                    "headers": {"type": "array", "items": {"type": "string"}},
                    "credentials": {"type": "boolean"}
                }
            }
        ),
        Tool(
            name="kong_enable_key_auth",
            description="Enable key authentication plugin on a service or route",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_id": {"type": "string"},
                    "route_id": {"type": "string"},
                    "key_names": {"type": "array", "items": {"type": "string"}, "description": "Header names for API key (default: apikey)"}
                }
            }
        ),
        Tool(
            name="kong_enable_jwt",
            description="Enable JWT authentication plugin on a service or route",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_id": {"type": "string"},
                    "route_id": {"type": "string"},
                    "uri_param_names": {"type": "array", "items": {"type": "string"}},
                    "claims_to_verify": {"type": "array", "items": {"type": "string"}}
                }
            }
        ),
        Tool(
            name="kong_enable_ip_restriction",
            description="Enable IP restriction plugin on a service or route",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_id": {"type": "string"},
                    "route_id": {"type": "string"},
                    "allow": {"type": "array", "items": {"type": "string"}, "description": "Allowed IPs/CIDRs"},
                    "deny": {"type": "array", "items": {"type": "string"}, "description": "Denied IPs/CIDRs"}
                }
            }
        ),
        Tool(
            name="kong_enable_request_transformer",
            description="Enable request transformer plugin on a service or route",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_id": {"type": "string"},
                    "route_id": {"type": "string"},
                    "add_headers": {"type": "array", "items": {"type": "string"}},
                    "remove_headers": {"type": "array", "items": {"type": "string"}},
                    "add_querystring": {"type": "array", "items": {"type": "string"}},
                    "remove_querystring": {"type": "array", "items": {"type": "string"}}
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    async with httpx.AsyncClient() as client:
        try:
            # Services
            if name == "kong_list_services":
                r = await client.get(f"{KONG_ADMIN_URL}/services")
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_get_service":
                r = await client.get(f"{KONG_ADMIN_URL}/services/{arguments['service_id']}")
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_create_service":
                r = await client.post(f"{KONG_ADMIN_URL}/services", json=arguments)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_update_service":
                service_id = arguments.pop("service_id")
                r = await client.patch(f"{KONG_ADMIN_URL}/services/{service_id}", json=arguments)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_delete_service":
                r = await client.delete(f"{KONG_ADMIN_URL}/services/{arguments['service_id']}")
                return [TextContent(type="text", text=f"Service deleted: {r.status_code}")]
            
            # Routes
            elif name == "kong_list_routes":
                r = await client.get(f"{KONG_ADMIN_URL}/routes")
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_get_route":
                r = await client.get(f"{KONG_ADMIN_URL}/routes/{arguments['route_id']}")
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_create_route":
                service_id = arguments.pop("service_id")
                r = await client.post(f"{KONG_ADMIN_URL}/services/{service_id}/routes", json=arguments)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_update_route":
                route_id = arguments.pop("route_id")
                r = await client.patch(f"{KONG_ADMIN_URL}/routes/{route_id}", json=arguments)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_delete_route":
                r = await client.delete(f"{KONG_ADMIN_URL}/routes/{arguments['route_id']}")
                return [TextContent(type="text", text=f"Route deleted: {r.status_code}")]
            
            # Upstreams
            elif name == "kong_list_upstreams":
                r = await client.get(f"{KONG_ADMIN_URL}/upstreams")
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_get_upstream":
                r = await client.get(f"{KONG_ADMIN_URL}/upstreams/{arguments['upstream_id']}")
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_create_upstream":
                r = await client.post(f"{KONG_ADMIN_URL}/upstreams", json=arguments)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_delete_upstream":
                r = await client.delete(f"{KONG_ADMIN_URL}/upstreams/{arguments['upstream_id']}")
                return [TextContent(type="text", text=f"Upstream deleted: {r.status_code}")]
            
            # Targets
            elif name == "kong_list_targets":
                r = await client.get(f"{KONG_ADMIN_URL}/upstreams/{arguments['upstream_id']}/targets")
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_add_target":
                upstream_id = arguments.pop("upstream_id")
                r = await client.post(f"{KONG_ADMIN_URL}/upstreams/{upstream_id}/targets", json=arguments)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_delete_target":
                upstream_id = arguments["upstream_id"]
                target_id = arguments["target_id"]
                r = await client.delete(f"{KONG_ADMIN_URL}/upstreams/{upstream_id}/targets/{target_id}")
                return [TextContent(type="text", text=f"Target deleted: {r.status_code}")]
            
            # Plugins - Generic
            elif name == "kong_list_plugins":
                r = await client.get(f"{KONG_ADMIN_URL}/plugins")
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_delete_plugin":
                r = await client.delete(f"{KONG_ADMIN_URL}/plugins/{arguments['plugin_id']}")
                return [TextContent(type="text", text=f"Plugin deleted: {r.status_code}")]
            
            # Plugins - Specific
            elif name == "kong_enable_rate_limiting":
                payload = {
                    "name": "rate-limiting",
                    "config": {}
                }
                for key in ["second", "minute", "hour", "day"]:
                    if key in arguments:
                        payload["config"][key] = arguments[key]
                if "service_id" in arguments:
                    payload["service"] = {"id": arguments["service_id"]}
                if "route_id" in arguments:
                    payload["route"] = {"id": arguments["route_id"]}
                r = await client.post(f"{KONG_ADMIN_URL}/plugins", json=payload)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_enable_cors":
                config = {}
                if "origins" in arguments:
                    config["origins"] = arguments["origins"]
                if "methods" in arguments:
                    config["methods"] = arguments["methods"]
                if "headers" in arguments:
                    config["headers"] = arguments["headers"]
                if "credentials" in arguments:
                    config["credentials"] = arguments["credentials"]
                
                payload = {"name": "cors", "config": config}
                if "service_id" in arguments:
                    payload["service"] = {"id": arguments["service_id"]}
                if "route_id" in arguments:
                    payload["route"] = {"id": arguments["route_id"]}
                r = await client.post(f"{KONG_ADMIN_URL}/plugins", json=payload)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_enable_key_auth":
                config = {}
                if "key_names" in arguments:
                    config["key_names"] = arguments["key_names"]
                
                payload = {"name": "key-auth", "config": config}
                if "service_id" in arguments:
                    payload["service"] = {"id": arguments["service_id"]}
                if "route_id" in arguments:
                    payload["route"] = {"id": arguments["route_id"]}
                r = await client.post(f"{KONG_ADMIN_URL}/plugins", json=payload)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_enable_jwt":
                config = {}
                if "uri_param_names" in arguments:
                    config["uri_param_names"] = arguments["uri_param_names"]
                if "claims_to_verify" in arguments:
                    config["claims_to_verify"] = arguments["claims_to_verify"]
                
                payload = {"name": "jwt", "config": config}
                if "service_id" in arguments:
                    payload["service"] = {"id": arguments["service_id"]}
                if "route_id" in arguments:
                    payload["route"] = {"id": arguments["route_id"]}
                r = await client.post(f"{KONG_ADMIN_URL}/plugins", json=payload)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_enable_ip_restriction":
                config = {}
                if "allow" in arguments:
                    config["allow"] = arguments["allow"]
                if "deny" in arguments:
                    config["deny"] = arguments["deny"]
                
                payload = {"name": "ip-restriction", "config": config}
                if "service_id" in arguments:
                    payload["service"] = {"id": arguments["service_id"]}
                if "route_id" in arguments:
                    payload["route"] = {"id": arguments["route_id"]}
                r = await client.post(f"{KONG_ADMIN_URL}/plugins", json=payload)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_enable_request_transformer":
                config = {}
                if "add_headers" in arguments:
                    config["add"] = {"headers": arguments["add_headers"]}
                if "remove_headers" in arguments:
                    config["remove"] = {"headers": arguments["remove_headers"]}
                if "add_querystring" in arguments:
                    if "add" not in config:
                        config["add"] = {}
                    config["add"]["querystring"] = arguments["add_querystring"]
                if "remove_querystring" in arguments:
                    if "remove" not in config:
                        config["remove"] = {}
                    config["remove"]["querystring"] = arguments["remove_querystring"]
                
                payload = {"name": "request-transformer", "config": config}
                if "service_id" in arguments:
                    payload["service"] = {"id": arguments["service_id"]}
                if "route_id" in arguments:
                    payload["route"] = {"id": arguments["route_id"]}
                r = await client.post(f"{KONG_ADMIN_URL}/plugins", json=payload)
                return [TextContent(type="text", text=r.text)]
            
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
        
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
