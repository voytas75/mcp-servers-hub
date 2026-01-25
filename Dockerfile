FROM node:20-alpine

# Install Python, Git, and supervisor
RUN apk add --no-cache python3 py3-pip supervisor bash git

WORKDIR /app

# Create directory structure
RUN mkdir -p /app/mcp-servers /app/logs

# Copy dependency files
COPY package.json package-lock.json* ./
COPY requirements.txt* ./

# Install dependencies
RUN npm install && \
    if [ -f requirements.txt ]; then pip3 install --break-system-packages -r requirements.txt; fi

# Copy MCP server configurations
COPY mcp-servers/ /app/mcp-servers/

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisord.conf

# Health check script
COPY healthcheck.sh /app/
RUN chmod +x /app/healthcheck.sh

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD /app/healthcheck.sh

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
