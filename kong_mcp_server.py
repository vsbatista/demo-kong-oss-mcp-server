import asyncio
import httpx
import os
from mcp.server import Server
from mcp.types import Tool, TextContent
from typing import Any

KONG_ADMIN_URL = os.getenv("KONG_ADMIN_URL", "http://localhost:8001")

app = Server("kong-mcp-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="kong_list_services",
            description="List all Kong services",
            inputSchema={"type": "object", "properties": {}}
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
            name="kong_delete_service",
            description="Delete a Kong service by name or ID",
            inputSchema={
                "type": "object",
                "required": ["service_id"],
                "properties": {"service_id": {"type": "string"}}
            }
        ),
        Tool(
            name="kong_list_routes",
            description="List all Kong routes",
            inputSchema={"type": "object", "properties": {}}
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
            name="kong_list_upstreams",
            description="List all Kong upstreams",
            inputSchema={"type": "object", "properties": {}}
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
            name="kong_list_plugins",
            description="List all enabled plugins",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="kong_enable_plugin",
            description="Enable a plugin on a service or route",
            inputSchema={
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string"},
                    "service_id": {"type": "string"},
                    "route_id": {"type": "string"},
                    "config": {"type": "object"}
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    async with httpx.AsyncClient() as client:
        try:
            if name == "kong_list_services":
                r = await client.get(f"{KONG_ADMIN_URL}/services")
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_create_service":
                r = await client.post(f"{KONG_ADMIN_URL}/services", json=arguments)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_delete_service":
                r = await client.delete(f"{KONG_ADMIN_URL}/services/{arguments['service_id']}")
                return [TextContent(type="text", text=f"Service deleted: {r.status_code}")]
            
            elif name == "kong_list_routes":
                r = await client.get(f"{KONG_ADMIN_URL}/routes")
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_create_route":
                service_id = arguments.pop("service_id")
                r = await client.post(f"{KONG_ADMIN_URL}/services/{service_id}/routes", json=arguments)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_list_upstreams":
                r = await client.get(f"{KONG_ADMIN_URL}/upstreams")
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_create_upstream":
                r = await client.post(f"{KONG_ADMIN_URL}/upstreams", json=arguments)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_add_target":
                upstream_id = arguments.pop("upstream_id")
                r = await client.post(f"{KONG_ADMIN_URL}/upstreams/{upstream_id}/targets", json=arguments)
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_list_plugins":
                r = await client.get(f"{KONG_ADMIN_URL}/plugins")
                return [TextContent(type="text", text=r.text)]
            
            elif name == "kong_enable_plugin":
                payload = {"name": arguments["name"]}
                if "config" in arguments:
                    payload["config"] = arguments["config"]
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
