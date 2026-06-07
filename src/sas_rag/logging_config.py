import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if hasattr(record, "extra"):
            log_obj.update(record.extra)
        return json.dumps(log_obj, default=str)


def configure_logging(
    log_dir: Path = Path("logs"),
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
) -> None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        console = logging.StreamHandler(sys.stderr)
        console.setLevel(console_level)
        console.setFormatter(JSONFormatter())
        root.addHandler(console)

    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "sas-rag.log")
        file_handler.setLevel(file_level)
        file_handler.setFormatter(JSONFormatter())
        root.addHandler(file_handler)
