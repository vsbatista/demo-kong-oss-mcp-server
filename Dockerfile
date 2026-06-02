FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml kong_mcp_server.py ./

RUN pip install --no-cache-dir -e .

CMD ["python", "kong_mcp_server.py"]
