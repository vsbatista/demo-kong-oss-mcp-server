# Kong MCP Server

MCP server para administração do Kong Gateway via API Admin.

## Instalação via Docker (Recomendado)

### Build da imagem:
```bash
./setup.sh
# ou manualmente:
docker build -t kong-mcp-server .
```

**IMPORTANTE:** Não tente rodar o container diretamente. Ele só funciona quando chamado pelo Kiro CLI via stdio.

### Configuração no Kiro CLI

Adicione ao `~/.kiro/mcp_config.json`:

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

## Distribuição para a Equipe

### Opção 1: Docker Hub
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

### Opção 2: Registry Privado
```bash
docker tag kong-mcp-server registry.empresa.com/kong-mcp-server:latest
docker push registry.empresa.com/kong-mcp-server:latest
```

### Opção 3: Arquivo tar
```bash
docker save kong-mcp-server > kong-mcp-server.tar
# Distribuir o arquivo

# Equipe carrega:
docker load < kong-mcp-server.tar
```

## Variáveis de Ambiente

- `KONG_ADMIN_URL` - URL da API Admin do Kong (padrão: `http://localhost:8001`)
- `KONG_ENV` - Ambiente (local/dev/staging/prod) para identificação (padrão: `local`)

Copie `.env.example` para `.env` e ajuste conforme necessário.

## Tools Disponíveis

### Services (CRUD Completo)
- `kong_list_services` - Lista todos os services
- `kong_get_service` - Detalhes de um service específico
- `kong_create_service` - Cria um novo service
- `kong_update_service` - Atualiza um service existente
- `kong_delete_service` - Remove um service

### Routes (CRUD Completo)
- `kong_list_routes` - Lista todas as routes
- `kong_get_route` - Detalhes de uma route específica
- `kong_create_route` - Cria uma route para um service
- `kong_update_route` - Atualiza uma route existente
- `kong_delete_route` - Remove uma route

### Upstreams & Targets
- `kong_list_upstreams` - Lista upstreams
- `kong_get_upstream` - Detalhes de um upstream específico
- `kong_create_upstream` - Cria upstream com load balancing
- `kong_delete_upstream` - Remove um upstream
- `kong_list_targets` - Lista targets de um upstream
- `kong_add_target` - Adiciona target a um upstream
- `kong_delete_target` - Remove target de um upstream

### Plugins Genéricos
- `kong_list_plugins` - Lista plugins habilitados
- `kong_delete_plugin` - Remove um plugin

### Plugins Específicos (Configuração Simplificada)
- `kong_enable_rate_limiting` - Rate limiting (por segundo/minuto/hora/dia)
- `kong_enable_cors` - CORS (origins, methods, headers, credentials)
- `kong_enable_key_auth` - Autenticação por API key
- `kong_enable_jwt` - Autenticação JWT
- `kong_enable_ip_restriction` - Restrição por IP (allow/deny)
- `kong_enable_request_transformer` - Transformação de requests (headers, querystring)

## Exemplo de Uso

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
