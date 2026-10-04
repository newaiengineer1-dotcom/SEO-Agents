from dataclasses import dataclass, asdict
from typing import Any
import json

@dataclass
class AuditResult:
    url: str
    status_code: int
    title: str
    meta_description: str
    canonical: str
    h1_count: int
    h2_count: int
    word_count: int
    image_count: int
    images_missing_alt: int
    internal_links: int
    external_links: int
    robots_ok: bool
    sitemap_found: bool
    schema_types: list[str]
    viewport: bool
    https: bool
    issues: list[str]
    warnings: list[str]
    strengths: list[str]
    raw_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def compact_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
