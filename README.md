# MCAT APP

A lightweight Python web app that serves a static MCAT study page and proxies chat requests to the NVIDIA Integrate API.

## Project Structure

- `server.py` - Python HTTP server that serves static files and forwards `/api/chat` POST requests to `https://integrate.api.nvidia.com/v1/chat/completions`.
- `mcat-study.html` - Front-end study interface for the MCAT app.
- `Dockerfile` - Container configuration for running the app in Docker.
- `render.yaml` - Render deployment configuration.
- `requirements.txt` - No external Python dependencies are required; the app uses the Python standard library.

## Features

- Serves static front-end assets from the project directory
- Provides CORS-enabled API proxy for chat requests
- Supports a configurable `PORT` environment variable
- Simple deploy support via Docker and Render

## Requirements

- Python 3.11+
- Docker (optional, for containerized deployment)

## Local Setup

1. Open a terminal in the project directory.
2. Run the app:

```bash
python server.py
```

3. Open your browser at:

```text
http://localhost:3000
```

## Environment Variables

- `PORT` - Port number for the server to listen on (default: `3000`).

Example:

```bash
export PORT=10000
python server.py
```

## Docker

Build the Docker image:

```bash
docker build -t mcat-app .
```

Run the container:

```bash
docker run -p 10000:10000 -e PORT=10000 mcat-app
```

The app will be available at `http://localhost:10000`.

## Render Deployment

This repository includes a `render.yaml` manifest configured for deployment on Render as a Python web service.

- `startCommand: python server.py`
- `runtime: python`

## API Proxy Behavior

The server accepts POST requests at `/api/chat` and forwards them to the NVIDIA Integrate Chat Completions endpoint.

- It preserves the `Authorization` header.
- It returns the remote response status and JSON body.
- It handles CORS preflight requests with `OPTIONS`.

## Notes

- `requirements.txt` is intentionally empty because the app uses only Python standard libraries.
- The app serves any static assets located in the project directory, including `mcat-study.html`.
