from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ChecksumRegistry:
    """Tracks source checksums across ingestion runs to detect changes."""

    def __init__(self, registry_path: Path) -> None:
        self.registry_path = registry_path
        self._checksums: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        if self.registry_path.exists():
            try:
                data = json.loads(self.registry_path.read_text(encoding="utf-8"))
                self._checksums = data.get("checksums", {})
                logger.debug(f"Loaded checksum registry: {len(self._checksums)} sources")
            except (json.JSONDecodeError, KeyError) as exc:
                logger.warning(f"Failed to load checksum registry: {exc}")
                self._checksums = {}
        else:
            logger.debug("No existing checksum registry found")

    def save(self) -> None:
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.registry_path.write_text(
            json.dumps({"checksums": self._checksums}, indent=2),
            encoding="utf-8",
        )
        logger.debug(f"Saved checksum registry: {len(self._checksums)} sources")

    def get(self, source_id: str) -> str | None:
        return self._checksums.get(source_id)

    def set(self, source_id: str, checksum: str) -> None:
        self._checksums[source_id] = checksum

    def classify_source(self, source_id: str, current_checksum: str) -> str:
        """Classify source as 'new', 'unchanged', or 'changed'."""
        previous = self.get(source_id)
        if previous is None:
            return "new"
        if previous == current_checksum:
            return "unchanged"
        return "changed"

    def summary(self) -> dict[str, Any]:
        return {
            "total_tracked": len(self._checksums),
            "registry_path": str(self.registry_path),
        }
