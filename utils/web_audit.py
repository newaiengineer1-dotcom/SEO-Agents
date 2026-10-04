from __future__ import annotations
from urllib.parse import urljoin, urlparse
import re
import requests
from bs4 import BeautifulSoup
from core.schemas import AuditResult

UA = "PremiumSEOAgent/1.0 (+SEO audit)"

def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url

def audit_url(url: str, timeout: int = 15) -> AuditResult:
    url = normalize_url(url)
    r = requests.get(url, timeout=timeout, headers={"User-Agent": UA}, allow_redirects=True)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    md = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    canonical_tag = soup.find("link", attrs={"rel": lambda x: x and "canonical" in x})
    images = soup.find_all("img")
    links = soup.find_all("a", href=True)
    host = urlparse(r.url).netloc
    internal = external = 0
    for a in links:
        href = urljoin(r.url, a.get("href", ""))
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        if urlparse(href).netloc == host:
            internal += 1
        elif urlparse(href).netloc:
            external += 1
    schema_types = []
    for s in soup.find_all("script", attrs={"type": "application/ld+json"}):
        text = s.get_text(" ", strip=True)
        schema_types += re.findall(r'"@type"\s*:\s*"([^"]+)"', text)
    robots_url = urljoin(r.url, "/robots.txt")
    sitemap_url = urljoin(r.url, "/sitemap.xml")
    try:
        robots_ok = requests.get(robots_url, timeout=8, headers={"User-Agent": UA}).ok
    except requests.RequestException:
        robots_ok = False
    try:
        sitemap_found = requests.get(sitemap_url, timeout=8, headers={"User-Agent": UA}).ok
    except requests.RequestException:
        sitemap_found = False
    text = soup.get_text(" ", strip=True)
    word_count = len(re.findall(r"\b\w+\b", text))
    issues, warnings, strengths = [], [], []
    if not title: issues.append("Missing title tag")
    elif len(title) < 30 or len(title) > 60: warnings.append("Title length is outside the common 30–60 character target")
    if not md: issues.append("Missing meta description")
    elif len(md.get("content", "")) < 70 or len(md.get("content", "")) > 165: warnings.append("Meta description length should be reviewed")
    if len(soup.find_all("h1")) != 1: issues.append("Page should normally have exactly one primary H1")
    if not canonical_tag: warnings.append("Canonical URL is missing")
    if not images: warnings.append("No images detected")
    if images and sum(1 for i in images if not i.get("alt", "").strip()) > 0: issues.append("Some images are missing alt text")
    if not robots_ok: warnings.append("robots.txt could not be verified")
    if not sitemap_found: warnings.append("sitemap.xml could not be verified")
    if not soup.find("meta", attrs={"name": re.compile("^viewport$", re.I)}): issues.append("Missing mobile viewport meta tag")
    if r.url.startswith("https://"): strengths.append("HTTPS is enabled")
    if schema_types: strengths.append("Structured data detected")
    if internal >= 3: strengths.append("Useful internal-link footprint detected")
    return AuditResult(
        url=r.url, status_code=r.status_code, title=title,
        meta_description=md.get("content", "") if md else "",
        canonical=canonical_tag.get("href", "") if canonical_tag else "",
        h1_count=len(soup.find_all("h1")), h2_count=len(soup.find_all("h2")),
        word_count=word_count, image_count=len(images),
        images_missing_alt=sum(1 for i in images if not i.get("alt", "").strip()),
        internal_links=internal, external_links=external, robots_ok=robots_ok,
        sitemap_found=sitemap_found, schema_types=sorted(set(schema_types)),
        viewport=bool(soup.find("meta", attrs={"name": re.compile("^viewport$", re.I)})),
        https=r.url.startswith("https://"), issues=issues, warnings=warnings,
        strengths=strengths, raw_text=text[:12000],
    )
