# ComfyUI-Nano-Banana

Custom node pack for **Nano Banana** (Gemini image generation and editing) in ComfyUI.

## Nodes

| Node | Description |
|------|-------------|
| **Google API Key** | Provides API key via env var, config file, or manual input |
| **Nano Banana Generate** | Text-to-image and image-to-image via Gemini models (`:generateContent` endpoint) |
| **Nano Banana Chat Edit** | Multi-turn conversational image editing and transformation |

## Installation

1. Clone into `ComfyUI/custom_nodes/`:
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/fwlemos/NBP-Comfyui.git
   ```
2. Install dependencies:
   ```bash
   pip install -r NBP-Comfyui/requirements.txt
   ```
3. Restart ComfyUI.

## API Key Setup

Provide your Google API key via one of these methods (checked in order):

1. **Environment variable**: Set `GOOGLE_API_KEY` or `GEMINI_API_KEY`
2. **Config file**: Create `google_api_key.txt` in the extension directory with your key
3. **Node input**: Wire a `Google API Key` node and type the key directly

## Nano Banana Generate

Generates images using Google's Gemini vision-language models via the `:generateContent` endpoint.

### Models

- `gemini-3-pro-image-preview` (Nano Banana Pro) — Highest quality, best text rendering.
- `gemini-3.1-flash-image-preview` (Nano Banana 2 / Flash) — Faster, cheaper, supports reasoning/thinking & 512px.

### Parameters

- **prompt**: Text prompt for generation or editing.
- **model**: Gemini model selection (Pro or Flash).
- **aspect_ratio**: Control the output shape (Up to 14 ratios on Flash).
- **image_size**: Resolution control (512px, 1K, 2K, 4K - dependent on model).
- **reference_images** (Optional): Support for up to 14 reference images for image-to-image/editing tasks.
- **batch_count**: Number of images to generate (supports concurrency).
- **thinking_level**: Reasoning depth for Flash model.

## Nano Banana Chat Edit

A conversational interface for iterative image editing.

### Parameters

- **prompt**: Instruction for the edit (e.g., "Change the sky to sunset").
- **input_image**: The base image to be edited.
- **chat_history**: Connect to previous chat nodes for multi-turn editing.

## License

MIT
