
## Current Configuration

### Active MCP Servers
- **filesystem** - File system operations (enabled)
- **github** - GitHub integration (requires `GITHUB_PERSONAL_ACCESS_TOKEN` in `.env`)

### IDE Integration
- **Roo Cline (VS Code)**: Configured via `~/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`
- **Wrapper Scripts**: Located in `~/.local/bin/mcp-*`

### Management Commands
```bash
# View MCP server status
docker exec mcp-servers-hub supervisorctl status

# View logs
docker exec mcp-servers-hub supervisorctl tail -f mcp-filesystem

# Restart specific server
docker exec mcp-servers-hub supervisorctl restart mcp-filesystem

# Container management
docker compose restart        # Restart all
docker compose logs -f        # View all logs
docker compose down           # Stop all
docker compose up -d --build  # Rebuild and start
```

### Adding New MCP Servers

1. Edit `supervisord.conf` and add new `[program:mcp-yourserver]` section
2. Create wrapper script in `~/.local/bin/mcp-yourserver`
3. Add to Roo Cline config: `~/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`
4. Restart: `docker compose restart`
