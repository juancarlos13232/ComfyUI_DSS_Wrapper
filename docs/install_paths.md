# Installation Paths and Folder Structure

This document explains where files should be placed on your local machine
when using the ComfyUI DiffSynth Studio Wrapper.

It is written for beginners and assumes no prior knowledge of ComfyUI internals.


## 1. Where this repository goes

This repository must be placed inside ComfyUI's `custom_nodes` directory.

Example (Windows):

C:\ComfyUI\custom_nodes\ComfyUI_DSS_Wrapper

Example (Linux / macOS):

~/ComfyUI/custom_nodes/ComfyUI_DSS_Wrapper

Do not rename the folder after cloning.


## 2. Important folders inside this project

Inside `ComfyUI_DSS_Wrapper`, you will find:

- `z_image_nodes.py`
  This contains the Python code for the custom nodes.
  Users should NOT edit this file unless they know what they are doing.

- `workflows/`
  Contains example ComfyUI workflow JSON files.
  These can be loaded directly inside ComfyUI.

- `docs/`
  Contains documentation files like this one.
  Editing files here is always safe.


## 3. Where Z-Image models go

Z-Image model files (for DiffSynth) should be placed in a directory
that you control on your system.

Example:

C:\Models\DiffSynth\Z-Image\

The exact path can be referenced later in user configuration files
or inside ComfyUI nodes.


## 4. Where generated LoRAs are saved

Generated LoRA files are written to a user-defined output folder.

Example:

C:\ComfyUI\models\loras\generated\

This allows the LoRA to appear automatically in ComfyUI
without restarting.


## 5. Files users are expected to edit

Users are encouraged to edit:

- `docs/user_config.json`
  This file is designed to be safe for user customization.

Users should avoid editing Python files unless instructed.


## 6. What NOT to move or rename

Do NOT:
- Rename `z_image_nodes.py`
- Rename the repository folder
- Move files out of `custom_nodes`

Doing so may cause ComfyUI to stop detecting the nodes.


## Summary

If this repository is placed correctly inside `custom_nodes`,
and paths are set correctly, the nodes will appear automatically
when ComfyUI is started.
