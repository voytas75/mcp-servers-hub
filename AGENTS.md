# Repository Guidelines

## Project Structure & Module Organization
- Root-level config drives the runtime: `Dockerfile`, `docker-compose.yml`, and `supervisord.conf`.
- `mcp-servers/` is the place for local MCP server code or wrappers (currently placeholder directories).
- `logs/` is a host-mounted volume for process logs written by `supervisord`.
- Dependency manifests live in `package.json` (Node) and `requirements.txt` (Python).

## Build, Test, and Development Commands
- `docker compose up -d --build` builds the image and starts the hub.
- `docker compose restart` restarts all supervised services.
- `docker exec mcp-servers-hub supervisorctl status` shows per-server status.
- `docker exec mcp-servers-hub supervisorctl tail -f mcp-filesystem` tails a server log.
- `docker compose logs -f` follows container logs.

## Coding Style & Naming Conventions
- Match existing formatting: 2-space indentation in YAML, INI-style blocks in `supervisord.conf`.
- Name supervisor programs as `mcp-<server>` and logs as `mcp-<server>.log`.
- Keep shell scripts in bash and minimal; use clear, direct commands.

## Testing Guidelines
- No automated tests are defined in this repository.
- If you add tests, document the framework and the primary command here.

## Commit & Pull Request Guidelines
- Commit messages follow a short, imperative style (e.g., “Add …”, “Remove …”).
- PRs should describe configuration changes, list required env vars, and include a quick validation step (e.g., `supervisorctl status`).

## Security & Configuration Tips
- Store tokens in `.env` and never hardcode them in config files.
- `.env` is ignored by git; avoid committing real secrets.
- When adding servers, update `supervisord.conf`, and keep README notes in sync.
