# Monocle API Manual

**Version:** 1.0
**Last Updated:** 2025-05-25

---

## Overview
Monocle is a multi-modal embedding service providing endpoints for text and image embeddings. It supports both combined and image-only embedding workflows via a simple HTTP API. The service is powered by FastAPI, Sentence Transformers, and CLIP/OpenCLIP models.

---

## Base URL
```
http://<host>:8000/
```

---

## Endpoints

### 1. `POST /embed`
#### Description
Multi-modal endpoint: Accepts texts, image_path, or image_base64 and auto-detects the input type. Returns a list of embeddings for provided inputs.

#### Request Body (JSON)
```
{
  "texts": ["string", ...],           // Optional: List of texts to embed
  "image_path": "string",             // Optional: Path to image file on server
  "image_base64": "string"            // Optional: Base64-encoded image data
}
```
At least one of `texts`, `image_path`, or `image_base64` must be provided.

#### Response (200 OK)
```
{
  "embeddings": [[float, ...], ...]     // List of embeddings (each input returns one embedding)
}
```

#### Error Responses
- `400 Bad Request`: No valid input provided or image could not be loaded/decoded.
- `500 Internal Server Error`: Model or embedding error.

---

### 2. `POST /embed/image`
#### Description
Image-only endpoint: Accepts `image_path` or `image_base64` and returns a single image embedding and a generated description.

#### Request Body (JSON)
```
{
  "image_path": "string",              // Optional: Path to image file on server
  "image_base64": "string"             // Optional: Base64-encoded image data
}
```
One of `image_path` or `image_base64` must be provided.

#### Response (200 OK)
```
{
  "embedding": [float, ...],            // Embedding vector for the image
  "description": "string"              // Generated or default description
}
```

#### Error Responses
- `400 Bad Request`: No valid image input or image could not be loaded/decoded.
- `500 Internal Server Error`: Model or embedding error.

---

## Models Used
- **Text Embedding:** all-MiniLM-L6-v2 (Sentence Transformers)
- **Image Embedding:**
  - OpenCLIP (`ViT-B-32`, pretrained on `laion2b_s34b_b79k`) if available
  - Fallback: CLIP from HuggingFace transformers (`openai/clip-vit-base-patch32`)

---

## Example Usage
### Text Embedding
```
curl -X POST http://localhost:8000/embed -H "Content-Type: application/json" -d '{"texts": ["hello world"]}'
```

### Image Embedding (by path)
```
curl -X POST http://localhost:8000/embed/image -H "Content-Type: application/json" -d '{"image_path": "test.jpg"}'
```

### Image Embedding (by base64)
```
curl -X POST http://localhost:8000/embed/image -H "Content-Type: application/json" -d '{"image_base64": "<base64>"}'
```

---

## Error Handling
All errors are returned as JSON with a `detail` field describing the problem.

---

## Health and Debug
- The service exposes `/docs` (Swagger UI) and `/redoc` for interactive API documentation.
- Healthcheck is performed via `GET /docs` by default in Docker Compose.

---

## Directory Structure (Relevant to API)
- `app.py` – Main FastAPI application
- `requirements.txt` – Python dependencies
- `Dockerfile` – Docker build instructions
- `test.jpg` – Example image for testing
- `docs/API_MANUAL.md` – This API documentation

---

## Contact & Support
For issues, feature requests, or contributions, please contact the Monocle maintainers or open an issue in your project repository.
