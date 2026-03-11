from typing import Any


def compile_prompt(elements: dict[str, Any]) -> str:
    parts = []

    if "subject" in elements:
        parts.append(elements["subject"])
    if "scene" in elements:
        parts.append(f"in {elements['scene']}")
    if "camera" in elements:
        parts.append(f"camera: {elements['camera']}")
    if "style" in elements:
        parts.append(f"style: {elements['style']}")
    if "lighting" in elements:
        parts.append(f"lighting: {elements['lighting']}")
    if "mood" in elements:
        parts.append(f"mood: {elements['mood']}")

    if not parts:
        return elements.get("raw", "")

    return ", ".join(parts)
