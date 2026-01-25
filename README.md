
## Current Configuration

### Why use this hub instead of separate MCPs?
- **One place to run them all**: start, stop, and restart multiple servers with a single `docker compose` and `supervisorctl` flow.
- **Consistent logs**: every server writes to `./logs` so debugging doesn’t require hunting in multiple places.
- **Shared env config**: tokens live in one `.env`, avoiding duplicated setup across separate runs.
- **Fewer moving parts**: Docker image includes Node + Python deps once; no per‑server installs on the host.
- **Easy IDE wiring**: wrapper scripts point to the hub, so adding a server doesn’t mean reworking IDE configs.

### Active MCP Servers
- **filesystem** - File system operations (enabled)
- **github** - GitHub integration (requires `GITHUB_PERSONAL_ACCESS_TOKEN` in `.env`)
- **context7** - Context7 documentation lookup (HTTP on `:8080`)
- **microsoft-docs** - Microsoft Docs MCP (remote via `mcp-remote`)
- **system-info** - Local system configuration (enabled)
- **tavily-expert** - Tavily search/extract/map/crawl (requires `TAVILY_API_KEY` in `.env`)

### Where this hub fits (vs other options)
This project is the lightweight, local option: a simple Docker + supervisord runner for a small set of MCP servers.

- **If you want a single MCP endpoint + API/UI**: look at `mcp-hub` (central coordinator with HTTP/SSE, config management, and monitoring).
- **If you want a web UI and per-server HTTP proxy ports**: `mcpzoo` provides that in a single container.
- **If you need enterprise runtime, registry, gateway, and policy controls**: `ToolHive` is a full platform with Docker/K8s support.
- **If you just need server implementations**: `modelcontextprotocol/servers` is the reference server repo this hub can run via `npx`.

### Environment Configuration
Create a `.env` file in the repo root with the keys below (placeholders shown):
```bash
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token_here
TAVILY_API_KEY=your_tavily_api_key_here
# If you re-enable Slack, also set:
# SLACK_BOT_TOKEN=your_slack_bot_token_here
# SLACK_TEAM_ID=your_slack_team_id_here
```

### IDE Integration
- **Roo Cline (VS Code)**: Configured via `~/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json` and `~/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/settings/mcp_settings.json`
- **Wrapper Scripts**: Located in `~/.local/bin/mcp-*` (e.g., `mcp-context7` proxies to the local Context7 HTTP endpoint)
- **Codex CLI**: Point your Codex MCP settings to the same wrapper scripts (`~/.local/bin/mcp-*`) to launch servers over stdio.

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
