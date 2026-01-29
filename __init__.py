from .z_image_nodes import ZImageLoader, ZImageI2L, ZImageSampler, ZImageLoRASaver

NODE_CLASS_MAPPINGS = {
    "ZImageLoader": ZImageLoader,
    "ZImageI2L": ZImageI2L,
    "ZImageSampler": ZImageSampler,
    "ZImageLoRASaver": ZImageLoRASaver
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZImageLoader": "Z-Image Loader (DiffSynth)",
    "ZImageI2L": "Z-Image Image-to-LoRA (DiffSynth)",
    "ZImageSampler": "Z-Image Sampler (DiffSynth)",
    "ZImageLoRASaver": "Z-Image LoRA Saver (DiffSynth)"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
