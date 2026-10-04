from __future__ import annotations
from datetime import datetime, timezone
import json
from pathlib import Path

def build_report(audit, outputs: dict[str, str], business_context: str, target_keywords: str) -> str:
    sections = [
        "# Premium SEO & Website Upgrade Report",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"URL: {audit.url}",
        "\n## Executive Summary",
        f"HTTP status: {audit.status_code}; H1: {audit.h1_count}; words: {audit.word_count}; internal links: {audit.internal_links}; schema types: {', '.join(audit.schema_types) or 'None detected'}.",
        "\n## Audit Evidence\n```json\n" + json.dumps(audit.to_dict(), ensure_ascii=False, indent=2) + "\n```",
        f"\n## Business Context\n{business_context or 'Not supplied.'}",
        f"\n## Target Keywords\n{target_keywords or 'Not supplied.'}",
    ]
    labels = {"technical":"Technical SEO","keywords":"Keyword & Content Strategy","copy":"On-Page Copy","ux":"Premium UX/UI","growth":"Authority & Growth","qa":"QA & Release"}
    for k,v in outputs.items(): sections.append(f"\n## {labels.get(k,k.title())}\n{v}")
    sections.append("\n## Implementation Principle\nApply changes in a staging environment, validate crawl/indexing and conversion behavior, then release. SEO outcomes are not guaranteed because rankings depend on search-engine systems and competition.")
    return "\n".join(sections)

def write_report(text: str, path: str | Path) -> Path:
    p = Path(path); p.write_text(text, encoding="utf-8"); return p
