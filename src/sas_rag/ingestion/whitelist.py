from __future__ import annotations

import json
import logging
from pathlib import Path

from sas_rag.ingestion.models.records import SourceRecord

logger = logging.getLogger(__name__)


REQUIRED_SOURCE_FIELDS = {
    "source_id",
    "title",
    "source_uri",
    "local_path",
    "source_family",
    "sas_version",
    "priority",
    "source_type",
    "ingestion_status",
}


def load_whitelist(path: Path) -> list[SourceRecord]:
    logger.info(f"Loading whitelist from: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Source whitelist must be a JSON list")

    records: list[SourceRecord] = []
    source_ids: set[str] = set()
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Whitelist item {index} must be an object")
        missing = REQUIRED_SOURCE_FIELDS - set(item)
        if missing:
            logger.warning(f"Whitelist item {index} missing fields: {sorted(missing)}")
            raise ValueError(f"Whitelist item {index} missing fields: {sorted(missing)}")
        record = SourceRecord.from_dict(item)
        if record.source_id in source_ids:
            raise ValueError(f"Duplicate source_id: {record.source_id}")
        source_ids.add(record.source_id)
        records.append(record)

    logger.info(f"Whitelist loaded: {len(records)} records")
    return records
