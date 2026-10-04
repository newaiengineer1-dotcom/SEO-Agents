from unittest.mock import patch, Mock
from utils.web_audit import audit_url

HTML = '''<html><head><title>Example Premium Service</title>
<meta name="description" content="A useful premium service description for customers and search engines with enough context to be meaningful.">
<link rel="canonical" href="https://example.com/">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script type="application/ld+json">{"@type":"Organization"}</script></head>
<body><h1>Main heading</h1><h2>Section</h2><img src="x.jpg" alt="Example"><a href="/about">About</a><a href="https://other.example">Other</a>
<p>Useful content for the website audit.</p></body></html>'''

def test_audit_with_mocked_http():
    page = Mock(status_code=200, url="https://example.com/", text=HTML)
    page.raise_for_status.return_value = None
    robots = Mock(ok=True)
    sitemap = Mock(ok=True)
    with patch("utils.web_audit.requests.get", side_effect=[page, robots, sitemap]):
        result = audit_url("example.com")
    assert result.status_code == 200
    assert result.h1_count == 1
    assert result.images_missing_alt == 0
    assert result.sitemap_found is True
    assert "Organization" in result.schema_types
