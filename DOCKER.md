# Docker Deployment Guide

This guide explains how to deploy DataViz Pro Analytics Platform using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed (optional, for easier deployment)
- Google Gemini API key

## Quick Start with Docker Compose

1. **Set up environment variables**
   ```bash
   # Create or edit .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

2. **Build and run**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Open browser to: http://localhost:8501

4. **Stop the application**
   ```bash
   docker-compose down
   ```

## Manual Docker Deployment

### Build the Docker Image

```bash
docker build -t dataviz-pro:latest .
```

### Run the Container

```bash
docker run -d \
  --name dataviz-pro \
  -p 8501:8501 \
  -e GEMINI_API_KEY=your_api_key_here \
  -v $(pwd)/data:/app/data \
  dataviz-pro:latest
```

### Container Management

**View logs:**
```bash
docker logs dataviz-pro
```

**Stop container:**
```bash
docker stop dataviz-pro
```

**Start container:**
```bash
docker start dataviz-pro
```

**Remove container:**
```bash
docker rm -f dataviz-pro
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| GEMINI_API_KEY | Google Gemini API key for AI features | Yes |
| STREAMLIT_SERVER_PORT | Port number (default: 8501) | No |
| STREAMLIT_SERVER_ADDRESS | Server address (default: 0.0.0.0) | No |

## Volume Mapping

Map local directories to container for data persistence:

```bash
docker run -d \
  -p 8501:8501 \
  -e GEMINI_API_KEY=your_key \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/exports:/app/exports \
  dataviz-pro:latest
```

## Health Check

The container includes a health check endpoint:

```bash
curl http://localhost:8501/_stcore/health
```

## Troubleshooting

**Container won't start:**
- Check logs: `docker logs dataviz-pro`
- Verify API key is set correctly
- Ensure port 8501 is not already in use

**Cannot access application:**
- Verify container is running: `docker ps`
- Check port mapping: `docker port dataviz-pro`
- Ensure firewall allows connections to port 8501

**Performance issues:**
- Increase container resources in Docker settings
- Check system resources: `docker stats dataviz-pro`

## Production Deployment

For production use, consider:

1. **Use a reverse proxy (Nginx/Traefik)**
2. **Enable HTTPS**
3. **Set up monitoring and logging**
4. **Configure resource limits:**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 4G
       reservations:
         cpus: '1'
         memory: 2G
   ```

## Security Notes

- Never commit .env file with real API keys
- Use Docker secrets for sensitive data in production
- Keep Docker images updated
- Use non-root user in production containers

## Support

For issues or questions, check the main README.md or create an issue in the repository.
