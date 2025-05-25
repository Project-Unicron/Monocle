# Monocle

**Monocle** is a multi-modal embedding service designed for easy integration into modern applications. It provides HTTP API endpoints for generating text and image embeddings using state-of-the-art models. Monocle is ideal for semantic search, recommendation, and AI-powered content understanding.

---

## Features
- **Text Embedding:** Generate vector embeddings for text using Sentence Transformers.
- **Image Embedding:** Generate vector embeddings for images using OpenCLIP or CLIP.
- **Multi-Modal:** Supports text, image path, or base64-encoded image inputs.
- **REST API:** Simple and fast HTTP endpoints powered by FastAPI.
- **Dockerized:** Ready-to-deploy with Docker and Docker Compose.
- **Automated Tests:** Includes bash scripts for API testing.

---

## Quickstart

### 1. Build and Run with Docker Compose
```sh
docker-compose build monocle
docker-compose up -d monocle
```

### 2. Test the API
Use the provided bash script:
```sh
cd apps/monocle/scripts
bash test_api.sh
```

Or try a simple curl command:
```sh
curl -X POST http://localhost:8000/embed -H "Content-Type: application/json" -d '{"texts": ["hello world"]}'
```

---

## API Documentation
See [`docs/API_MANUAL.md`](./docs/API_MANUAL.md) for full details on all endpoints, request/response formats, and example usage.

---

## Directory Structure
```
apps/monocle/
├── app.py               # Main FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker build instructions
├── test.jpg             # Example image for testing
├── docs/
│   └── API_MANUAL.md    # Full API documentation
├── scripts/
│   └── test_api.sh      # Bash API test script
└── ...
```

---

## Models
- **Text:** all-MiniLM-L6-v2 (Sentence Transformers)
- **Image:** OpenCLIP (ViT-B-32, laion2b_s34b_b79k) or fallback to CLIP (openai/clip-vit-base-patch32)

---

## Development
- Python 3.10+
- See `requirements.txt` for dependencies.
- Service runs on port `8000` by default.

---

## Troubleshooting
- If you see errors about `numpy` version incompatibility, ensure `requirements.txt` pins `numpy<2.0`.
- For Docker issues, check volumes and network settings in `docker-compose.yml`.

---

## License
This prject is licensed under GPL3
---

## Contact & Support
For issues or feature requests, please contact the maintainers or open an issue in your repository.
