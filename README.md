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

## Tools Disponíveis

- `kong_list_services` - Lista todos os services
- `kong_create_service` - Cria um novo service
- `kong_delete_service` - Remove um service
- `kong_list_routes` - Lista todas as routes
- `kong_create_route` - Cria uma route para um service
- `kong_list_upstreams` - Lista upstreams
- `kong_create_upstream` - Cria upstream com load balancing
- `kong_add_target` - Adiciona target a um upstream
- `kong_list_plugins` - Lista plugins habilitados
- `kong_enable_plugin` - Habilita plugin em service/route

## Exemplo de Uso

No Kiro CLI:

```
Crie um service chamado "api-backend" apontando para http://api.example.com
```

```
Liste todos os services do Kong
```

```
Crie um upstream "backend-pool" com algoritmo round-robin e adicione os targets 10.0.1.10:8080 e 10.0.1.11:8080
```
