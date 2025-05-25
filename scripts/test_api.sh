#!/bin/bash
set -e

# Monocle API curl tests
# Update HOST if running elsewhere
HOST="localhost:8000"

# 1. Test /embed with text
curl -s -w "\n[Status: %{http_code}]\n" -X POST http://$HOST/embed \
  -H "Content-Type: application/json" \
  -d '{"texts": ["hello world", "test embedding"]}'

echo "---"

# 2. Test /embed/image with image_path
curl -s -w "\n[Status: %{http_code}]\n" -X POST http://$HOST/embed/image \
  -H "Content-Type: application/json" \
  -d '{"image_path": "test.jpg"}'

echo "---"

# 3. Test /embed/image with image_base64
IMG_B64=$(base64 ../test.jpg | tr -d '\n')
curl -s -w "\n[Status: %{http_code}]\n" -X POST http://$HOST/embed/image \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "'$IMG_B64'"}'

echo "---"

# 4. Test /embed with image_path (multi-modal)
curl -s -w "\n[Status: %{http_code}]\n" -X POST http://$HOST/embed \
  -H "Content-Type: application/json" \
  -d '{"image_path": "test.jpg"}'

echo "---"

# 5. Test /embed with image_base64 (multi-modal)
curl -s -w "\n[Status: %{http_code}]\n" -X POST http://$HOST/embed \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "'$IMG_B64'"}'

echo "---"

# 6. Test /embed with text and image (multi-modal)
curl -s -w "\n[Status: %{http_code}]\n" -X POST http://$HOST/embed \
  -H "Content-Type: application/json" \
  -d '{"texts": ["hello world"], "image_path": "test.jpg"}'

echo "---"

# 7. Test error: missing input
curl -s -w "\n[Status: %{http_code}]\n" -X POST http://$HOST/embed \
  -H "Content-Type: application/json" \
  -d '{}'

echo "---"

# 8. Test error: invalid image path
curl -s -w "\n[Status: %{http_code}]\n" -X POST http://$HOST/embed/image \
  -H "Content-Type: application/json" \
  -d '{"image_path": "nonexistent.jpg"}'

echo "All tests completed."
