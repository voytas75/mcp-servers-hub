
## Current Configuration

### Why use this hub instead of separate MCPs?
- **One place to run them all**: start, stop, and restart multiple servers with a single `docker compose` and `supervisorctl` flow.
- **Consistent logs**: every server writes to `./logs` so debugging doesn’t require hunting in multiple places.
- **Shared env config**: tokens live in one `.env`, avoiding duplicated setup across separate runs.
- **Fewer moving parts**: Docker image includes Node + Python deps once; no per‑server installs on the host.
- **Easy IDE wiring**: wrapper scripts point to the hub, so adding a server doesn’t mean reworking IDE configs.

### Active MCP Servers
- **mcp-filesystem** - File system operations (enabled)
- **mcp-github** - GitHub integration (requires `GITHUB_PERSONAL_ACCESS_TOKEN` in `.env`)
- **mcp-context7** - Context7 documentation lookup (HTTP on `:8080`)
- **mcp-microsoft-docs** - Microsoft Docs MCP (remote via `mcp-remote`)
- **mcp-system-info** - Local system configuration (enabled)
- **mcp-tavily-expert** - Tavily search/extract/map/crawl (requires `TAVILY_API_KEY` in `.env`)
- **mcp-firecrawl** - Firecrawl search/scrape/extract (requires `FIRECRAWL_API_KEY` in `.env`)
- **mcp-exa** - Exa search (remote via `mcp-remote`)

### Where this hub fits (vs other options)
This project is the lightweight, local option: a simple Docker + supervisord runner for a small set of MCP servers.

- **If you want a single MCP endpoint + API/UI**: look at `mcp-hub` (central coordinator with HTTP/SSE, config management, and monitoring).
- **If you want a web UI and per-server HTTP proxy ports**: `mcpzoo` provides that in a single container.
- **If you need enterprise runtime, registry, gateway, and policy controls**: `ToolHive` is a full platform with Docker/K8s support.
- **If you just need server implementations**: `modelcontextprotocol/servers` is the reference server repo this hub can run via `npx`.

### Environment Configuration
Copy `.env.example` to `.env` in the repo root and fill in the values:
```bash
cp .env.example .env
```

Keys expected (placeholders shown):
```bash
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token_here
TAVILY_API_KEY=your_tavily_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
# If you re-enable Slack, also set:
# SLACK_BOT_TOKEN=your_slack_bot_token_here
# SLACK_TEAM_ID=your_slack_team_id_here
```

### Required Host Setup
If your MCP client runs on the host (Roo/Codex), install the wrapper scripts and keep the container name `mcp-servers-hub` (or update the wrappers).
```bash
mkdir -p ~/.local/bin
ln -sf "$PWD"/mcp-servers/wrappers/mcp-* ~/.local/bin/
```

### IDE Integration
- **Roo Cline (VS Code)**: Configured via `~/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json` and `~/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/settings/mcp_settings.json`
- **Wrapper Scripts**: Stored in `mcp-servers/wrappers/mcp-*` and symlinked into `~/.local/bin/mcp-*` (e.g., `mcp-context7` proxies to the local Context7 HTTP endpoint)
- **Codex CLI**: Point your Codex MCP settings to the same wrapper scripts (`~/.local/bin/mcp-*`) to launch servers over stdio.

### Codex CLI
Codex reads MCP config from `~/.codex/config.toml` (shared with the IDE extension). After the hub is running and wrapper scripts are installed, add servers using either the CLI or by editing the file directly.

Add servers with the CLI:
```bash
codex mcp add mcp-filesystem -- ~/.local/bin/mcp-filesystem
codex mcp add mcp-context7 -- ~/.local/bin/mcp-context7
```

Or edit `config.toml` (use absolute paths for the wrapper scripts):
```toml
[mcp_servers.mcp-filesystem]
command = "/home/you/.local/bin/mcp-filesystem"

[mcp_servers.mcp-context7]
command = "/home/you/.local/bin/mcp-context7"
```

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
2. Create wrapper script in `mcp-servers/wrappers/mcp-yourserver` and symlink to `~/.local/bin`
3. Add to Roo Cline config: `~/.vscode-server/data/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`
4. Restart: `docker compose restart`
