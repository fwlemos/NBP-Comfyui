"""
ComfyUI-Nano-Banana: Custom node pack for Nano Banana image generation.
"""

from .nodes import (
    GoogleAPIKeyNode, 
    NanoBananaGenerate, 
    NanoBananaChat
)

NODE_CLASS_MAPPINGS = {
    "GoogleAPIKey": GoogleAPIKeyNode,
    "NanoBananaGenerate": NanoBananaGenerate,
    "NanoBananaChat": NanoBananaChat,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GoogleAPIKey": "Google API Key",
    "NanoBananaGenerate": "🍌 Nano Banana Generate",
    "NanoBananaChat": "🍌 Nano Banana Chat Edit",
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
