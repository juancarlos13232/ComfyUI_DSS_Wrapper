# ComfyUI DiffSynth Studio Wrapper – Overview

This document explains what this project does, why it exists,
and what has been improved compared to the original implementation.
## What this project is

ComfyUI DiffSynth Studio Wrapper integrates DiffSynth Studio's Z-Image
(Image-to-LoRA and Image-to-Image) functionality directly into ComfyUI
as custom nodes.

It allows users to:
- Load Z-Image models inside ComfyUI
- Generate LoRAs from images without leaving the node graph
- Control layer-wise strength and refinement visually
- Use generated LoRAs immediately in the same workflow


## Why this fork exists

The original project provided valuable experimental functionality but
was not intended for long-term maintenance.

This fork focuses on:
- Improving stability with recent ComfyUI versions
- Making workflows easier to load and reuse
- Clarifying where users should edit settings
- Documenting the structure so others can understand it quickly


## What has been improved

Key improvements include:
- Clear separation between Python logic, workflows, and documentation
- Ready-to-use ComfyUI workflow JSON files
- User-safe configuration examples
- Better compatibility with modern ComfyUI setups
- Reduced confusion around installation and usage


## Who this is for

This project is intended for:
- ComfyUI users experimenting with LoRA generation
- Artists exploring image-driven LoRA workflows
- Developers interested in DiffSynth integration

It is not a production-ready training system, but a powerful creative tool.
