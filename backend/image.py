from diffusers import StableDiffusionPipeline
import torch
import os

IMAGE_PATH = "./data/images"
os.makedirs(IMAGE_PATH, exist_ok=True)

print("Loading image model...")
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32
)
pipe = pipe.to("cpu")

def generate_image(prompt: str, filename: str) -> str:
    full_prompt = f"{prompt}, fantasy art"
    try:
        image = pipe(
            full_prompt,
            num_inference_steps=15,
            width=384,
            height=384
        ).images[0]
        path = f"{IMAGE_PATH}/{filename}.png"
        image.save(path)
        print(f"Image saved: {path}")
        return filename
    except Exception as e:
        print(f"Image generation failed: {e}")
        return None