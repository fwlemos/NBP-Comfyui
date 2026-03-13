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

The extension resolves your Google API key using the following priority order:

1. **Environment Variables**: `GOOGLE_API_KEY` or `GEMINI_API_KEY`.
2. **Config File**: A `google_api_key.txt` file inside the extension directory.
3. **Node Input**: The `api_key` input on generation/chat nodes (or the dedicated **Google API Key** node).

> [!NOTE]
> This priority ensures you can have a global key set but still override it for specific workflows.

## Nano Banana Generate

Generates images using Google's Gemini vision-language models via the `:generateContent` endpoint.

### Models

- `gemini-3-pro-image-preview` (Nano Banana Pro) — Highest quality, best text rendering.
- `gemini-3.1-flash-image-preview` (Nano Banana 2 / Flash) — Faster, cheaper, supports reasoning/thinking & 512px.

### Parameters

#### Generation & Sampling
- **prompt**: Text description of the image. Supports multiple languages.
- **model**: Gemini model selection (Pro or Flash).
- **aspect_ratio**: Output proportions (Up to 14 ratios supported on Flash).
- **image_size**: Resolution (512px, 1K, 2K, 4K). Note: 512px is Flash-only.
- **temperature**: Controls randomness (0.0–2.0). 1.0 is recommended for Gemini 3.
- **top_p** / **top_k**: Nucleus and Top-K sampling parameters for variety control.
- **seed**: Sampling seed (0 = random). Influences consistency but doesn't guarantee identical results.

#### Logic & Batching
- **reference_images** (Optional): Connect up to 14 images for image-to-image or identity locking.
- **batch_count**: Number of concurrent API calls (1–8).
- **candidate_count**: Variations per API call (1–4). Total images = `batch_count` × `candidate_count`.
- **max_output_tokens**: Total token budget (text + thinking + image). Recommended: 2048+.
- **thinking_level**: Reasoning depth (Flash only). Options: `minimal`, `low`, `medium`, `high`.
- **response_modality**: `IMAGE` (extracts only imagery) or `TEXT_AND_IMAGE` (includes model descriptions).
- **enable_search_grounding**: Uses Google Search to inform generation with real-world knowledge.

#### Safety & Filters
- **safety_...**: Configurable filters for Hate Speech, Harassment, Sexually Explicit, and Dangerous Content. 
- **stop_sequences**: (Optional) Strings that trigger immediate generation termination.

## Nano Banana Chat Edit

A conversational interface for iterative image editing.

### Parameters

- **instruction**: The edit command (e.g., "Change the sky to sunset").
- **input_image**: The base image to be transformed.
- **chat_history**: Chain multiple chat nodes to maintain context across turns.
- **system_instruction**: High-level persona or style guidance for the model.
- Includes all sampling and safety parameters from the Generate node.

## License

MIT
