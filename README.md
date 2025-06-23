# Production AI

This project is a production-ready AI service that processes both image and text inputs using the Gemini API. It is deployed on an AWS EC2 instance using Docker and includes performance monitoring.

## Features
- Accepts text + image input via HTTP POST
- Calls Gemini multimodal model to generate a response
- Measures and logs request latency and status
- Exposes endpoints for image-only or text-only processing

## Deployment Architecture
- FastAPI application hosted in a Docker container on an EC2 instance
- Image and text inputs handled using multipart form data
- Gemini API used for inference (no local model)
- Logs written to `performance_log.txt` on the server

## Endpoints

- `POST /process` — takes `prompt` (text) and `image` (file), returns model output and latency
- `POST /analyze-text` — takes `prompt` (text), returns text-only model result
- `POST /analyze-image` — takes `image`, returns metadata (format, mode, size)

## How to Run (on EC2)

1. **SSH into your EC2 instance**  
2. **Clone this repo and move into the folder**
3. **Run Docker container**
4. **Access your API**

## Performance Monitoring

Every request logs the following into `performance_log.txt`:
- Prompt text
- Latency in milliseconds
- Request status (success/error)

Logs pulled from ec2 instance for display
