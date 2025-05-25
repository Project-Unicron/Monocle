print('LOADED MONOCLE APP.PY')
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import base64
from PIL import Image
import io
from sentence_transformers import SentenceTransformer

# For image embedding, use open_clip if available, fallback to CLIP from transformers
try:
    import open_clip
    clip_model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
    import torch
    use_open_clip = True
except ImportError:
    from transformers import CLIPProcessor, CLIPModel
    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    use_open_clip = False

app = FastAPI()
text_model = SentenceTransformer('all-MiniLM-L6-v2')

class EmbedRequest(BaseModel):
    texts: Optional[List[str]] = None
    image_path: Optional[str] = None
    image_base64: Optional[str] = None

class ImageEmbedResponse(BaseModel):
    embedding: list
    description: str

class EmbedResponse(BaseModel):
    embeddings: List[List[float]]

@app.post("/embed", response_model=EmbedResponse)
def embed(req: EmbedRequest):
    """
    Multi-modal endpoint: Accepts texts, image_path, or image_base64 and auto-detects the input type.
    """
    embeddings = []
    # Auto-detect and process text
    if req.texts:
        try:
            vectors = text_model.encode(req.texts, convert_to_numpy=True).tolist()
            embeddings.extend(vectors)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Text embedding error: {str(e)}")
    # Auto-detect and process image
    img = None
    if req.image_path:
        try:
            img = Image.open(req.image_path).convert("RGB")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not open image at path: {str(e)}")
    elif req.image_base64:
        try:
            img_data = base64.b64decode(req.image_base64)
            img = Image.open(io.BytesIO(img_data)).convert("RGB")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not decode base64 image: {str(e)}")
    if img is not None:
        try:
            if use_open_clip:
                img_tensor = preprocess(img).unsqueeze(0)
                with torch.no_grad():
                    image_emb = clip_model.encode_image(img_tensor)
                image_emb = image_emb.cpu().numpy().tolist()
            else:
                inputs = processor(images=img, return_tensors="pt")
                with torch.no_grad():
                    image_emb = clip_model.get_image_features(**inputs)
                image_emb = image_emb.cpu().numpy().tolist()
            embeddings.extend(image_emb)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image embedding error: {str(e)}")
    if not embeddings:
        raise HTTPException(status_code=400, detail="No valid input provided. Provide at least one of: texts, image_path, or image_base64.")
    return {"embeddings": embeddings}

@app.post("/embed/image", response_model=ImageEmbedResponse)
def embed_image(req: EmbedRequest):
    """
    Image-only endpoint: Accepts image_path or image_base64 and returns image embedding and CLIP description.
    """
    img = None
    if req.image_path:
        try:
            img = Image.open(req.image_path).convert("RGB")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not open image at path: {str(e)}")
    elif req.image_base64:
        try:
            img_data = base64.b64decode(req.image_base64)
            img = Image.open(io.BytesIO(img_data)).convert("RGB")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not decode base64 image: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="No image input provided. Provide image_path or image_base64.")
    try:
        # Get image embedding
        if use_open_clip:
            img_tensor = preprocess(img).unsqueeze(0)
            with torch.no_grad():
                image_emb = clip_model.encode_image(img_tensor)
            image_emb = image_emb.cpu().numpy().tolist()[0]
            # Generate description using open_clip captioning if available
            try:
                if hasattr(open_clip, 'Tokenizer') and hasattr(clip_model, 'generate_caption'):
                    description = clip_model.generate_caption(img_tensor)
                else:
                    description = "Image embedding generated."
            except Exception:
                description = "Image embedding generated."
        else:
            inputs = processor(images=img, return_tensors="pt")
            with torch.no_grad():
                image_emb = clip_model.get_image_features(**inputs)
            image_emb = image_emb.cpu().numpy().tolist()[0]
            # No captioning available in transformers CLIP
            description = "Image embedding generated."
        return {"embedding": image_emb, "description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image embedding error: {str(e)}")

# DEBUG: Print all registered routes
print("Registered routes:", [route.path for route in app.routes])