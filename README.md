# ComfyUI DiffSynth Studio Wrapper

A custom node wrapper for [DiffSynth-Studio](https://github.com/modelscope/DiffSynth-Studio)'s Z-Image I2L (Image to Lora) functionality in ComfyUI.

## Description

This project enables the use of Z-Image (Zero-shot Image-to-Image) features directly within ComfyUI. It allows you to load Z-Image models, create LoRAs from input images on-the-fly, and sample new images using those LoRAs.

I created these nodes to experiment with DiffSynth. While the functionality is valuable, please note that this project is provided "as-is" and I do not plan to provide active maintenance.

## Installation

1.  Clone this repository into your `ComfyUI/custom_nodes/` directory:
    ```bash
    cd ComfyUI/custom_nodes/
    git clone https://github.com/your-repo/ComfyUI_DSS_Wrapper.git
    ```

2.  Install the required dependencies:
    ```bash
    cd ComfyUI_DSS_Wrapper
    pip install -r requirements.txt
    ```

## Configuration

### Model Path

By default, the nodes will download the required models in `ComfyUI/models/diffsynth`.

You can override this path globally by setting the **Environment Variable**: `DIFFSYNTH_MODEL_BASE_PATH`.
If this variable is set, it will **always** take precedence over the path provided in the widget.

## Usage

The suite consists of three main nodes:

### 1. Z-Image Loader
*   **Model Path**: Directory where models are stored. If `DIFFSYNTH_MODEL_BASE_PATH` is set, this input is ignored (see console output for confirmation).
*   **Precision**:
    *   `bf16` (Recommended): Uses BFloat16 precision. Best balance of speed and memory.
    *   `fp32`: Full precision. Uses significantly more memory.
    *   *Note: `fp16` is not supported due to compatibility issues with the underlying library.*

### 2. Z-Image I2L (Image to LoRA)
*   Accepts up to 10 input images.
*   Converts these images into a temporary LoRA representation used by the sampler.

### 3. Z-Image Sampler
*   **Prompt/Negative Prompt**: Standard text inputs.
*   **Sigma Shift**: Controls the noise schedule shift.
*   **LoRA**: Input connection from the `Z-Image I2L` node.

### 4. Z-Image LoRA Saver
*   **LoRA**: Input connection from the `Z-Image I2L` node.
*   **Filename Prefix**: Prefix for the saved `.safetensors` file.
*   Saves the converted LoRA to your ComfyUI output directory. Use this if you want to reuse the style/character transfer without re-computing the `I2L` step.
---

## 📘 Documentation

Additional documentation is available in the `docs/` folder:

- **Overview**  
  `docs/overview.md`  
  Explains what this project does, why it exists, and what has been improved.

- **Installation Paths**  
  `docs/install_paths.md`  
  Shows exactly where to place this repository, models, and related files on your system.

- **User Configuration**  
  `docs/user_config.json`  
  Example configuration file showing safe, user-editable settings.

New users are strongly encouraged to read these files before using the nodes.
