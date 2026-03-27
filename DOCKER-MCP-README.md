# Docker-Based MCP Servers for Windsurf Cascade

Run MCP (Model Context Protocol) servers as Docker containers for Windsurf Cascade.

## Quick Start

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env and add your GitHub and Slack tokens
vim .env

# 3. Start essential MCP servers
docker compose up -d mcp-github mcp-slack

# 4. Verify servers are running
docker compose ps

# 5. Configure Windsurf (see docs/mcp-docker-setup.md)
```

## What's Included

### Essential Servers (Start These First)
- **mcp-github** (port 8102) - GitHub PR and CI access
- **mcp-slack** (port 8103) - Slack notifications

### Recommended Servers
- **mcp-sonarqube** (port 8104) - Code quality and security analysis (Official SonarSource)

### Optional Servers
- **mcp-jira** (port 8100) - JIRA issue tracking
- **mcp-clickup** (port 8101) - ClickUp task management

### Placeholder Servers (Verify Implementation)
- **mcp-codecov** (port 8105) - Coverage reporting

## Files

- `docker-compose.yml` - Main MCP server configuration
- `docker-compose.override.yml` - Local development overrides
- `.env.example` - Environment variable template
- `docs/mcp-docker-setup.md` - Complete setup guide

## Required Credentials

### GitHub (Essential)
```bash
GITHUB_TOKEN=ghp_your_token_here
```
Generate at: https://github.com/settings/tokens  
Scopes: `repo`, `read:org`, `workflow`

### Slack (Recommended)
```bash
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_TEAM_ID=T1234567890
```
Generate at: https://api.slack.com/apps  
Scopes: `chat:write`, `channels:read`, `im:write`

### SonarQube (Recommended)
```bash
# For SonarQube Cloud:
SONARQUBE_TOKEN=your_token_here
SONARQUBE_ORG=your-org-key

# For SonarQube Server (self-hosted):
SONARQUBE_TOKEN=your_token_here
SONARQUBE_URL=https://sonarqube.your-company.com
```
Generate at: https://sonarcloud.io (Cloud) or your SonarQube Server  
Official implementation: https://github.com/SonarSource/sonarqube-mcp-server

### JIRA (Optional)
```bash
JIRA_URL=https://your-org.atlassian.net
JIRA_EMAIL=you@example.com
JIRA_API_TOKEN=your_token_here
```
Generate at: https://id.atlassian.com/manage-profile/security/api-tokens

### ClickUp (Optional)
```bash
CLICKUP_API_TOKEN=your_token_here
CLICKUP_TEAM_ID=your_team_id
```
Generate at: https://app.clickup.com/settings/apps

## Common Commands

```bash
# Start essential servers
docker compose up -d mcp-github mcp-slack

# Start recommended servers (including SonarQube)
docker compose up -d mcp-github mcp-slack mcp-sonarqube

# Start all servers (including optional JIRA/ClickUp)
docker compose --profile optional up -d

# View logs
docker compose logs -f

# Stop servers
docker compose down

# Update images
docker compose pull && docker compose up -d --force-recreate
```

## Windsurf Configuration

Create `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "github": {
      "url": "http://localhost:8102",
      "transport": "http"
    },
    "slack": {
      "url": "http://localhost:8103",
      "transport": "sse"
    },
    "sonarqube": {
      "url": "http://localhost:8104",
      "transport": "http",
      "headers": {
        "Authorization": "Bearer YOUR_SONARQUBE_TOKEN"
      }
    }
  }
}
```

## Documentation

- **Complete setup guide**: `docs/mcp-docker-setup.md`
- **MCP integration overview**: `docs/mcp-integration.md`
- **npx-based setup**: `docs/mcp-setup-guide.md`

## Troubleshooting

### Servers won't start
```bash
# Check logs
docker compose logs mcp-github

# Verify .env has tokens
cat .env | grep GITHUB_TOKEN
```

### Health check failing
```bash
# Check status
docker compose ps

# Restart server
docker compose restart mcp-github
```

### Windsurf can't connect
```bash
# Test connectivity
curl http://localhost:8102

# Verify Windsurf config
cat ~/.codeium/windsurf/mcp_config.json
```

## Security

- Never commit `.env` to git
- Use minimal token scopes
- Rotate tokens every 90 days
- Ports bound to localhost only (127.0.0.1)

## Support

For detailed setup instructions, troubleshooting, and configuration options, see:
- `docs/mcp-docker-setup.md` - Complete Docker setup guide
- `docs/mcp-integration.md` - MCP architecture and design
- `AGENTS.md` - Project-specific MCP configuration

---

**Ready to start?** Run `docker compose up -d mcp-github mcp-slack` and configure Windsurf!
