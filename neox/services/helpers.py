from pathlib import Path
import re
import zipfile


def process_attachment(path: Path) -> str:
    """Read and format attached files."""
    if not path.exists() or path.stat().st_size > 10 * 1024 * 1024:
        return "[File too large (>10MB) or missing]"

    suffix = path.suffix.lower()
    text_exts = {
        ".txt", ".py", ".json", ".md", ".log",
        ".csv", ".yaml", ".yml", ".toml",
        ".html", ".css", ".js", ".bat", ".sh"
    }

    if suffix in text_exts:
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return "[Could not read text file]"

    if suffix == ".zip":
        try:
            with zipfile.ZipFile(path) as z:
                files = []

                for name in z.namelist()[:15]:
                    if not name.endswith("/"):
                        data = z.read(name)

                        try:
                            text = data.decode("utf-8")
                        except Exception:
                            text = f"[binary, {len(data)} bytes]"

                        files.append(f"--- {name} ---\n{text}")

                return (
                    "\n\n".join(files)
                    + f"\n[Zip had {len(z.namelist())} files total]"
                )

        except Exception:
            return "[Corrupted zip]"

    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".pdf"}:
        return f"[Attached Media: {path.name}] (Vision processing not yet enabled)"

    return f"[Attached binary file: {path.name}]"


def short_id(s: str, n: int = 20) -> str:
    """Truncate a model ID for display."""
    if len(s) <= n:
        return s

    return s[:n // 2 - 1] + "…" + s[-(n // 2):]


def get_initials(text: str) -> str:
    """Generate 2-character initials from a name."""
    parts = text.replace(":", " ").replace("-", " ").replace("_", " ").split()

    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()

    if len(parts) == 1 and len(parts[0]) >= 2:
        return parts[0][:2].upper()

    return text[:2].upper()


def repair_json(json_str: str) -> str:
    """Aggressively repair malformed JSON from small models."""
    s = json_str.strip()

    # Remove markdown fences
    s = re.sub(r"```(?:json)?", "", s)

    # Find JSON object/array
    brace_start = s.find("{")
    brace_end = s.rfind("}")

    if brace_start != -1 and brace_end > brace_start:
        s = s[brace_start:brace_end + 1]

    # Fix single quotes around keys only
    s = re.sub(r"['](\w+)[']\s*:", r'"\1":', s)

    # Fix missing commas
    s = re.sub(r'(?<=\d)\s+(?=")', ", ", s)
    s = re.sub(r'(?<=")\s+(?=")', ", ", s)

    return s