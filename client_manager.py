"""
Singleton manager for the Google GenAI SDK client.

Lazily initialises one `google.genai.Client` per resolved API key and Base URL,
and reuses it for every subsequent call.

Supports custom Base URL via:
1. GOOGLE_GENAI_BASE_URL environment variable
2. google_base_url.txt config file
3. Node input override
"""

import os

# Lazy import — the SDK may not be installed when ComfyUI first scans nodes.
# Cache key is now a tuple: (api_key, base_url)
_client_cache: dict = {}


def _resolve_api_key(override: str = "") -> str:
    """Resolve Google API key using three-tier priority.

    Priority: environment variable → config file → node input override.

    Args:
        override: API key string from the node input. Empty string means not set.

    Returns:
        Resolved API key string.

    Raises:
        RuntimeError: If no API key is found via any method.
    """
    # 1. Environment variable
    env_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    # 2. Config file in the extension directory
    config_path = os.path.join(os.path.dirname(__file__), "google_api_key.txt")
    if os.path.isfile(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            file_key = f.read().strip()
        if file_key:
            return file_key

    # 3. Node input override
    if override and override.strip():
        return override.strip()

    raise RuntimeError(
        "No Google API key found. Provide one via:\n"
        "  1. GOOGLE_API_KEY or GEMINI_API_KEY environment variable\n"
        "  2. google_api_key.txt file in the extension directory\n"
        "  3. The Google API Key node connected to the api_key input"
    )


def _resolve_base_url(override: str = "") -> str:
    """Resolve Custom Base URL using three-tier priority.

    Priority: environment variable → config file → node input override.
    Returns None if no custom URL is provided (uses SDK default).

    Args:
        override: Base URL string from the node input.

    Returns:
        Resolved Base URL string or None.
    """
    # 1. Environment variable
    env_url = os.environ.get("GOOGLE_GENAI_BASE_URL")
    if env_url and env_url.strip():
        return env_url.strip()

    # 2. Config file in the extension directory
    config_path = os.path.join(os.path.dirname(__file__), "google_base_url.txt")
    if os.path.isfile(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            file_url = f.read().strip()
        if file_url:
            return file_url

    # 3. Node input override
    if override and override.strip():
        return override.strip()

    return None


def get_client(api_key_override: str = "", base_url_override: str = ""):
    """Return a cached `google.genai.Client`, creating one if necessary.

    The client is cached per (API Key, Base URL) pair. This allows switching
    keys or endpoints at runtime while avoiding redundant initialisations.

    Args:
        api_key_override: Optional API key string from a node input.
        base_url_override: Optional Base URL string from a node input
                           (e.g., for proxies or custom gateways).

    Returns:
        A `google.genai.Client` instance ready for use.
    """
    # Deferred import so import errors surface at call-time only if SDK is missing
    from google import genai
    from google.genai.types import HttpOptions

    resolved_key = _resolve_api_key(api_key_override)
    resolved_url = _resolve_base_url(base_url_override)

    # Use a tuple as the cache key to distinguish clients with different URLs
    cache_key = (resolved_key, resolved_url)

    if cache_key not in _client_cache:
        # Prepare HttpOptions
        # If a custom URL is provided, we inject it here.
        # The SDK's internal logic will respect this if vertexai=False (default).
        if resolved_url:
            http_opts = HttpOptions(
                timeout=300000,
                base_url=resolved_url
            )
        else:
            http_opts = HttpOptions(timeout=300000)

        # Initialize Client
        # IMPORTANT: Do NOT set vertexai=True here, as it forces the SDK to
        # override the base_url with Vertex AI endpoints.
        _client_cache[cache_key] = genai.Client(
            api_key=resolved_key,
            http_options=http_opts
        )

    return _client_cache[cache_key]


def resolve_api_key(override: str = "") -> str:
    """Public wrapper kept for backward-compatibility with the API key node."""
    return _resolve_api_key(override)


def resolve_base_url(override: str = "") -> str:
    """Public wrapper to resolve base URL, useful for debugging or other nodes."""
    return _resolve_base_url(override)
