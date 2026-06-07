from __future__ import annotations

import json
import logging
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# SAS construct detection patterns
_MACRO_DEF = re.compile(r"^\s*%macro\s+(\w+)", re.IGNORECASE | re.MULTILINE)
_PROC_BLOCK = re.compile(r"^\s*proc\s+(\w+)", re.IGNORECASE | re.MULTILINE)
_DATA_STEP = re.compile(r"^\s*data\s+(\w+)", re.IGNORECASE | re.MULTILINE)
_MACRO_VAR = re.compile(r"%let\s+(\w+)\s*=", re.IGNORECASE)
_MACRO_FUNC = re.compile(r"%([a-z_][a-z0-9_]*)\b", re.IGNORECASE)
_SAS_FUNC = re.compile(r"\b([a-z_][a-z0-9_]*)\s*\(", re.IGNORECASE)
_LIBREF = re.compile(r"\b(\w+)\.", re.IGNORECASE)


@dataclass
class SasCodeAnalysis:
    file_path: str
    macro_definitions: list[str]
    proc_calls: list[str]
    data_steps: list[str]
    macro_variables: list[str]
    macro_functions: list[str]
    sas_functions: list[str]
    librefs: list[str]
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def analyze_sas_code(code: str, file_path: str = "") -> SasCodeAnalysis:
    """Extract SAS constructs from source code."""
    macro_defs = sorted(set(_MACRO_DEF.findall(code)))
    procs = sorted(set(_PROC_BLOCK.findall(code)))
    data_steps = sorted(set(_DATA_STEP.findall(code)))
    macro_vars = sorted(set(_MACRO_VAR.findall(code)))
    macro_funcs = sorted(set(_MACRO_FUNC.findall(code)))
    # Filter out common false positives and single-letter macros
    macro_funcs = [f for f in macro_funcs if len(f) > 1 and f.upper() not in {"DO", "IF", "THEN", "ELSE", "END", "TO"}]
    sas_funcs = sorted(set(_SAS_FUNC.findall(code)))
    # Filter out SQL keywords that look like function calls
    sql_keywords = {"SELECT", "FROM", "WHERE", "AND", "OR", "NOT", "IN", "IS", "AS", "UNIQUE", "COUNT"}
    sas_funcs = [f for f in sas_funcs if f.upper() not in sql_keywords]
    librefs = sorted(set(_LIBREF.findall(code)))
    # Filter numeric-looking refs and common false positives
    librefs = [ref for ref in librefs if ref.isalpha() and len(ref) <= 8]

    lines = code.strip().split("\n")
    summary = _generate_summary(
        len(lines),
        macro_defs,
        procs,
        data_steps,
        macro_vars,
    )

    return SasCodeAnalysis(
        file_path=file_path,
        macro_definitions=macro_defs,
        proc_calls=procs,
        data_steps=data_steps,
        macro_variables=macro_vars,
        macro_functions=macro_funcs,
        sas_functions=sas_funcs,
        librefs=librefs,
        summary=summary,
    )


def _generate_summary(
    line_count: int,
    macro_defs: list[str],
    procs: list[str],
    data_steps: list[str],
    macro_vars: list[str],
) -> str:
    parts = [f"SAS program with {line_count} lines."]
    if macro_defs:
        parts.append(f"Defines {len(macro_defs)} macros: {', '.join(macro_defs)}.")
    if procs:
        parts.append(f"Uses PROC {', '.join(procs)}.")
    if data_steps:
        parts.append(f"Contains {len(data_steps)} DATA step definition(s).")
    if macro_vars:
        parts.append(f"Declares {len(macro_vars)} macro variable(s).")
    return " ".join(parts)


def build_explanation_queries(analysis: SasCodeAnalysis) -> list[dict[str, str]]:
    """Build RAG retrieval queries from analyzed SAS constructs."""
    queries: list[dict[str, str]] = []

    for proc in analysis.proc_calls:
        queries.append({
            "topic": f"PROC {proc.upper()}",
            "query": f"PROC {proc.upper()} syntax and usage",
            "source_family": "procedures" if proc.lower() not in {"sql"} else "proc-sql",
        })

    for macro in analysis.macro_definitions:
        queries.append({
            "topic": f"%{macro} macro",
            "query": f"SAS macro definition %MACRO {macro} %MEND syntax",
            "source_family": "macro",
        })

    for macro_func in analysis.macro_functions:
        queries.append({
            "topic": f"%{macro_func}()",
            "query": f"SAS macro function %{macro_func} syntax",
            "source_family": "macro",
        })

    for sas_func in analysis.sas_functions:
        queries.append({
            "topic": f"{sas_func}()",
            "query": f"SAS function {sas_func} syntax and examples",
            "source_family": "language-reference",
        })

    for macro_var in analysis.macro_variables[:5]:  # Limit to avoid overload
        queries.append({
            "topic": f"&{macro_var} macro variable",
            "query": "SAS macro variable %LET scope resolution",
            "source_family": "macro",
        })

    return queries


def explain_sas_code(
    code: str,
    file_path: str,
    search_fn: Any,
) -> dict[str, Any]:
    """Analyze SAS code and retrieve explanations from the RAG index.

    Args:
        code: The SAS source code.
        file_path: Path to the source file (for reporting).
        search_fn: Callable that accepts (query, k, filters) and returns results.

    Returns:
        Dict with analysis, queries, and retrieved evidence.
    """
    analysis = analyze_sas_code(code, file_path)
    queries = build_explanation_queries(analysis)

    explanations: list[dict[str, Any]] = []
    for item in queries:
        try:
            results = search_fn(
                query=item["query"],
                k=2,
                filters={"source_family": item["source_family"]} if item.get("source_family") else None,
            )
            explanations.append({
                "topic": item["topic"],
                "query": item["query"],
                "source_family": item.get("source_family"),
                "evidence": results,
            })
        except Exception as exc:
            logger.warning(f"Failed to retrieve evidence for {item['topic']}: {exc}")
            explanations.append({
                "topic": item["topic"],
                "query": item["query"],
                "source_family": item.get("source_family"),
                "error": str(exc),
            })

    return {
        "analysis": analysis.to_dict(),
        "queries": queries,
        "explanations": explanations,
    }


def explain_sas_file(file_path: Path, search_fn: Any) -> dict[str, Any]:
    code = file_path.read_text(encoding="utf-8")
    return explain_sas_code(code, str(file_path), search_fn)
