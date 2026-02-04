# Contributing to Kong MCP Server

Thank you for your interest in contributing to Kong MCP Server! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Docker version, Kong version)

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- A clear description of the feature
- Use cases and benefits
- Any implementation ideas you have

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages (`git commit -m 'feat: add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Commit Message Convention

We follow conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Keep functions focused and small
- Add docstrings for public functions

### Testing

Before submitting a PR:
1. Build the Docker image: `docker build -t kong-mcp-server .`
2. Test all tools manually with Kiro CLI
3. Verify no regressions in existing functionality

### Adding New Tools

When adding new Kong Admin API tools:
1. Add the tool definition in `list_tools()`
2. Implement the handler in `call_tool()`
3. Update README.md with the new tool
4. Test the tool with a real Kong instance

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/kong-mcp-server.git
cd kong-mcp-server

# Build the image
docker build -t kong-mcp-server .

# Configure in Kiro CLI
# Edit ~/.kiro/settings/mcp_config.json
```

## Questions?

Feel free to open an issue for any questions or discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
