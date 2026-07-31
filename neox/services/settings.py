import json
from pathlib import Path


# NeoX project root directory
APP_DIR = Path(__file__).resolve().parents[2]

# Runtime settings file
SETTINGS_PATH = APP_DIR / "kouncil_settings.json"


def load_settings() -> dict:
    """Load settings from JSON or return defaults."""
    default = {
        "lm_studio_url": "http://localhost:1234",
        "ollama_url": "http://localhost:11434",
        "lm_studio_enabled": True,
        "ollama_enabled": True,
        "theme": "dark",
        "max_concurrency": 3,
        "persona_assignments": {},
        "debate_enabled": False,
        "debate_rounds": 2,
        "web_search_enabled": False,
        "google_api_key": "",
        "google_search_engine_id": "",
        "max_search_results": 5,
        "response_mode": "voting",
    }

    if SETTINGS_PATH.exists():
        try:
            data = json.loads(
                SETTINGS_PATH.read_text(encoding="utf-8")
            )
            default.update(data)
        except Exception as e:
            print(f"Error loading settings: {e}")

    return default


def save_settings(s: dict):
    """Save settings to JSON."""
    current = load_settings()
    current.update(s)

    try:
        SETTINGS_PATH.write_text(
            json.dumps(current, indent=2),
            encoding="utf-8"
        )
    except Exception as e:
        print(f"Error saving settings: {e}")


settings = load_settings()