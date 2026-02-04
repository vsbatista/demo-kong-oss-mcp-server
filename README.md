# Kong MCP Server

[English](#english) | [Português](#português)

---

## English

MCP server for Kong Gateway administration via Admin API.

### Features

- Complete CRUD operations for services, routes, upstreams, and targets
- Simplified configuration for common plugins (rate-limiting, CORS, authentication, etc.)
- Multi-environment support (local/dev/staging/prod)
- Docker-based for easy distribution
- No Python/venv setup required

### Installation via Docker (Recommended)

#### Build the image:
```bash
./setup.sh
# or manually:
docker build -t kong-mcp-server .
```

**IMPORTANT:** Do not try to run the container directly. It only works when called by Kiro CLI via stdio.

### Configuration in Kiro CLI

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

### Distribution to Team

#### Option 1: Docker Hub
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

#### Option 2: Private Registry
```bash
docker tag kong-mcp-server registry.company.com/kong-mcp-server:latest
docker push registry.company.com/kong-mcp-server:latest
```

#### Option 3: Tar file
```bash
docker save kong-mcp-server > kong-mcp-server.tar
# Distribute the file

# Team loads:
docker load < kong-mcp-server.tar
```

### Environment Variables

- `KONG_ADMIN_URL` - Kong Admin API URL (default: `http://localhost:8001`)
- `KONG_ENV` - Environment identifier (local/dev/staging/prod) (default: `local`)

Copy `.env.example` to `.env` and adjust as needed.

### Available Tools

#### Services (Complete CRUD)
- `kong_list_services` - List all services
- `kong_get_service` - Get details of a specific service
- `kong_create_service` - Create a new service
- `kong_update_service` - Update an existing service
- `kong_delete_service` - Delete a service

#### Routes (Complete CRUD)
- `kong_list_routes` - List all routes
- `kong_get_route` - Get details of a specific route
- `kong_create_route` - Create a route for a service
- `kong_update_route` - Update an existing route
- `kong_delete_route` - Delete a route

#### Upstreams & Targets
- `kong_list_upstreams` - List upstreams
- `kong_get_upstream` - Get details of a specific upstream
- `kong_create_upstream` - Create upstream with load balancing
- `kong_delete_upstream` - Delete an upstream
- `kong_list_targets` - List targets of an upstream
- `kong_add_target` - Add target to an upstream
- `kong_delete_target` - Delete target from an upstream

#### Generic Plugins
- `kong_list_plugins` - List enabled plugins
- `kong_delete_plugin` - Delete a plugin

#### Specific Plugins (Simplified Configuration)
- `kong_enable_rate_limiting` - Rate limiting (per second/minute/hour/day)
- `kong_enable_cors` - CORS (origins, methods, headers, credentials)
- `kong_enable_key_auth` - API key authentication
- `kong_enable_jwt` - JWT authentication
- `kong_enable_ip_restriction` - IP restriction (allow/deny)
- `kong_enable_request_transformer` - Request transformation (headers, querystring)

### Usage Examples

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

---

## Português

Servidor MCP para administração do Kong Gateway via API Admin.

### Funcionalidades

- Operações CRUD completas para services, routes, upstreams e targets
- Configuração simplificada para plugins comuns (rate-limiting, CORS, autenticação, etc.)
- Suporte multi-ambiente (local/dev/staging/prod)
- Baseado em Docker para fácil distribuição
- Não requer setup de Python/venv

### Instalação via Docker (Recomendado)

#### Build da imagem:
```bash
./setup.sh
# ou manualmente:
docker build -t kong-mcp-server .
```

**IMPORTANTE:** Não tente rodar o container diretamente. Ele só funciona quando chamado pelo Kiro CLI via stdio.

### Configuração no Kiro CLI

Adicione ao `~/.kiro/settings/mcp_config.json`:

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

### Ou usando Docker Compose:

```bash
docker compose up -d
```

E configure no Kiro:
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

### Distribuição para a Equipe

#### Opção 1: Docker Hub
```bash
docker tag kong-mcp-server seu-usuario/kong-mcp-server:latest
docker push seu-usuario/kong-mcp-server:latest
```

Equipe usa:
```json
{
  "mcpServers": {
    "kong": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--network=host", "seu-usuario/kong-mcp-server"]
    }
  }
}
```

#### Opção 2: Registry Privado
```bash
docker tag kong-mcp-server registry.empresa.com/kong-mcp-server:latest
docker push registry.empresa.com/kong-mcp-server:latest
```

#### Opção 3: Arquivo tar
```bash
docker save kong-mcp-server > kong-mcp-server.tar
# Distribuir o arquivo

# Equipe carrega:
docker load < kong-mcp-server.tar
```

### Variáveis de Ambiente

- `KONG_ADMIN_URL` - URL da API Admin do Kong (padrão: `http://localhost:8001`)
- `KONG_ENV` - Identificador de ambiente (local/dev/staging/prod) (padrão: `local`)

Copie `.env.example` para `.env` e ajuste conforme necessário.

### Tools Disponíveis

#### Services (CRUD Completo)
- `kong_list_services` - Lista todos os services
- `kong_get_service` - Detalhes de um service específico
- `kong_create_service` - Cria um novo service
- `kong_update_service` - Atualiza um service existente
- `kong_delete_service` - Remove um service

#### Routes (CRUD Completo)
- `kong_list_routes` - Lista todas as routes
- `kong_get_route` - Detalhes de uma route específica
- `kong_create_route` - Cria uma route para um service
- `kong_update_route` - Atualiza uma route existente
- `kong_delete_route` - Remove uma route

#### Upstreams & Targets
- `kong_list_upstreams` - Lista upstreams
- `kong_get_upstream` - Detalhes de um upstream específico
- `kong_create_upstream` - Cria upstream com load balancing
- `kong_delete_upstream` - Remove um upstream
- `kong_list_targets` - Lista targets de um upstream
- `kong_add_target` - Adiciona target a um upstream
- `kong_delete_target` - Remove target de um upstream

#### Plugins Genéricos
- `kong_list_plugins` - Lista plugins habilitados
- `kong_delete_plugin` - Remove um plugin

#### Plugins Específicos (Configuração Simplificada)
- `kong_enable_rate_limiting` - Rate limiting (por segundo/minuto/hora/dia)
- `kong_enable_cors` - CORS (origins, methods, headers, credentials)
- `kong_enable_key_auth` - Autenticação por API key
- `kong_enable_jwt` - Autenticação JWT
- `kong_enable_ip_restriction` - Restrição por IP (allow/deny)
- `kong_enable_request_transformer` - Transformação de requests (headers, querystring)

### Exemplos de Uso

No Kiro CLI:

**Services & Routes:**
```
Crie um service chamado "api-backend" apontando para http://api.example.com
```

```
Crie uma route /v1/users com métodos GET e POST para o service api-backend
```

```
Atualize o service api-backend para apontar para http://new-api.example.com
```

**Upstreams & Load Balancing:**
```
Crie um upstream "backend-pool" com algoritmo round-robin e adicione os targets 10.0.1.10:8080 e 10.0.1.11:8080
```

```
Liste todos os targets do upstream backend-pool
```

**Plugins:**
```
Habilite rate limiting de 100 requisições por minuto no service api-backend
```

```
Habilite CORS permitindo origins https://app.example.com e https://admin.example.com
```

```
Habilite autenticação por API key na route /v1/users
```

```
Habilite IP restriction permitindo apenas 10.0.0.0/8 e 192.168.1.0/24
```

---

## License

MIT