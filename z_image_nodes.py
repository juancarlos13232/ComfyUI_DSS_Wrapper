import os
import sys
import torch
import numpy as np
from PIL import Image
from PIL import Image
import folder_paths


# Import DiffSynth modules after path setup
from diffsynth.pipelines.z_image import (
    ZImagePipeline, ModelConfig,
    ZImageUnit_Image2LoRAEncode, ZImageUnit_Image2LoRADecode
)

# Capture the original environment variable at startup/import time
# This prevents pollution if we overwrite os.environ later
ORIGINAL_ENV_PATH = os.environ.get("DIFFSYNTH_MODEL_BASE_PATH")
print(f"[Z-Image] Init - DIFFSYNTH_MODEL_BASE_PATH: {ORIGINAL_ENV_PATH}")

class ZImageLoader:
    @classmethod
    def INPUT_TYPES(cls):
        path_from_env = ORIGINAL_ENV_PATH
        # print(f"[Z-Image] Checking ENV 'DIFFSYNTH_MODEL_BASE_PATH': {path_from_env}")
        
        if path_from_env:
            default_path = path_from_env
        else:
            default_path = os.path.join(folder_paths.models_dir, "diffsynth")
        return {
            "required": {
                "model_path": ("STRING", {"default": default_path, "multiline": False}),
                "device": (["cuda", "cpu"], {"default": "cuda"}),
                "precision": (["bf16", "fp32"], {"default": "bf16"}),
            }
        }

    RETURN_TYPES = ("Z_IMAGE_PIPE",)
    RETURN_NAMES = ("pipe",)
    FUNCTION = "load_model"
    CATEGORY = "DiffSynth/Z-Image"

    def load_model(self, model_path, device, precision):
        print(f"[Z-Image] Load Model called with path: {model_path}")

        target_path = model_path
        
        # Priority: ENV > Widget
        # If the environment variable is set, it overrides the widget input completely.
        if ORIGINAL_ENV_PATH:
             print(f"[Z-Image] NOTICE: ENV 'DIFFSYNTH_MODEL_BASE_PATH' is set to '{ORIGINAL_ENV_PATH}'.")
             print(f"[Z-Image] Force using ENV path, ignoring widget path '{model_path}'.")
             target_path = ORIGINAL_ENV_PATH
        
        # Set the environment variable for DiffSynth to use
        os.environ["DIFFSYNTH_MODEL_BASE_PATH"] = target_path
        os.environ["DIFFSYNTH_DOWNLOAD_SOURCE"] = "huggingface"

        torch_dtype = {
            "bf16": torch.bfloat16,
            "fp32": torch.float32
        }[precision]

        # VRAM config for hot-loading to save memory
        vram_config = {
            "offload_dtype": torch_dtype,
            "offload_device": "cpu",
            "onload_dtype": torch_dtype,
            "onload_device": device,
            "preparing_dtype": torch_dtype,
            "preparing_device": device,
            "computation_dtype": torch_dtype,
            "computation_device": device,
        }

        pipe = ZImagePipeline.from_pretrained(
            torch_dtype=torch_dtype,
            device=device,
            model_configs=[
                ModelConfig(model_id="Tongyi-MAI/Z-Image", origin_file_pattern="transformer/*.safetensors", **vram_config),
                ModelConfig(model_id="Tongyi-MAI/Z-Image-Turbo", origin_file_pattern="text_encoder/*.safetensors", **vram_config),
                ModelConfig(model_id="Tongyi-MAI/Z-Image-Turbo", origin_file_pattern="vae/diffusion_pytorch_model.safetensors", **vram_config),
                ModelConfig(model_id="DiffSynth-Studio/General-Image-Encoders", origin_file_pattern="SigLIP2-G384/model.safetensors", **vram_config),
                ModelConfig(model_id="DiffSynth-Studio/General-Image-Encoders", origin_file_pattern="DINOv3-7B/model.safetensors", **vram_config),
                ModelConfig(model_id="DiffSynth-Studio/Z-Image-i2L", origin_file_pattern="model.safetensors", **vram_config),
            ],
            tokenizer_config=ModelConfig(model_id="Tongyi-MAI/Z-Image-Turbo", origin_file_pattern="tokenizer/"),
        )
        
        return (pipe,)

class ZImageI2L:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipe": ("Z_IMAGE_PIPE",),
            },
            "optional": {
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                "image_5": ("IMAGE",),
                "image_6": ("IMAGE",),
                "image_7": ("IMAGE",),
                "image_8": ("IMAGE",),
                "image_9": ("IMAGE",),
                "image_10": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("Z_IMAGE_LORA",)
    RETURN_NAMES = ("lora",)
    FUNCTION = "process"
    CATEGORY = "DiffSynth/Z-Image"

    def process(self, pipe, image_1=None, image_2=None, image_3=None, image_4=None,
                image_5=None, image_6=None, image_7=None, image_8=None, image_9=None, image_10=None):
        images_tensor = []
        if image_1 is not None: images_tensor.append(image_1)
        if image_2 is not None: images_tensor.append(image_2)
        if image_3 is not None: images_tensor.append(image_3)
        if image_4 is not None: images_tensor.append(image_4)
        if image_5 is not None: images_tensor.append(image_5)
        if image_6 is not None: images_tensor.append(image_6)
        if image_7 is not None: images_tensor.append(image_7)
        if image_8 is not None: images_tensor.append(image_8)
        if image_9 is not None: images_tensor.append(image_9)
        if image_10 is not None: images_tensor.append(image_10)

        if not images_tensor:
            raise ValueError("At least one image is required for Z-Image I2L processing.")

        # Convert ComfyUI tensors (Batch, H, W, C) to PIL Images
        pil_images = []
        for img_batch in images_tensor:
            for img_tensor in img_batch:
                # tensor is 0-1 float, convert to 0-255 uint8
                i = 255. * img_tensor.cpu().numpy()
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                pil_images.append(img.convert("RGB"))

        with torch.no_grad():
            # Using the DiffSynth units
            embs = ZImageUnit_Image2LoRAEncode().process(pipe, image2lora_images=pil_images)
            lora = ZImageUnit_Image2LoRADecode().process(pipe, **embs)["lora"]

        return (lora,)

class ZImageSampler:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipe": ("Z_IMAGE_PIPE",),
                "prompt": ("STRING", {"multiline": True, "default": "a cat"}),
                "negative_prompt": ("STRING", {"multiline": True, "default": "泛黄，发绿，模糊，低分辨率，低质量图像，扭曲的肢体，诡异的外观，丑陋，AI感，噪点，网格感，JPEG压缩条纹，异常的肢体，水印，乱码，意义不明的字符"}),
                "width": ("INT", {"default": 1024, "min": 256, "max": 4096, "step": 64}),
                "height": ("INT", {"default": 1024, "min": 256, "max": 4096, "step": 64}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 50, "min": 1, "max": 1000}),
                "cfg_scale": ("FLOAT", {"default": 4.0, "min": 0.0, "max": 100.0, "step": 0.1}),
                "sigma_shift": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0}),
            },
            "optional": {
                "lora": ("Z_IMAGE_LORA",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "sample"
    CATEGORY = "DiffSynth/Z-Image"

    def sample(self, pipe, prompt, negative_prompt, width, height, seed, steps, cfg_scale, sigma_shift, lora=None):
        
        # Ensure seed reproducibility
        torch.manual_seed(seed)
        
        kwargs = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "height": height,
            "width": width,
            "seed": seed,
            "cfg_scale": cfg_scale,
            "num_inference_steps": steps,
            "sigma_shift": sigma_shift,
        }
        
        if lora is not None:
            kwargs["positive_only_lora"] = lora

        # Run pipeline
        # pipe() returns a PIL Image
        image_pil = pipe(**kwargs)
        
        # Convert PIL back to ComfyUI tensor (Batch, H, W, C)
        image_np = np.array(image_pil).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)[None,] # Add batch dimension
        
        return (image_tensor,)

from safetensors.torch import save_file


class ZImageLoRASaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "lora": ("Z_IMAGE_LORA",),
                "filename_prefix": ("STRING", {"default": "z_image_lora"}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_lora"
    CATEGORY = "DiffSynth/Z-Image"
    OUTPUT_NODE = True

    def save_lora(self, lora, filename_prefix):
        output_dir = folder_paths.get_output_directory()
        filename = f"{filename_prefix}.safetensors"
        full_path = os.path.join(output_dir, filename)
        print("Saved in: " + output_dir)
        
        # Avoid overwriting existing files by appending counter if needed
        # Simple counter logic
        counter = 1
        base_name, ext = os.path.splitext(filename)
        while os.path.exists(full_path):
            full_path = os.path.join(output_dir, f"{base_name}_{counter}{ext}")
            counter += 1

        save_file(lora, full_path)
        print(f"Z-Image LoRA saved to: {full_path}")
        
        return ()
