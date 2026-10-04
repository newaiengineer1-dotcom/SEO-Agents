import json
from core.schemas import AuditResult
from utils.web_audit import normalize_url

def test_normalize_url():
    assert normalize_url("example.com") == "https://example.com"

def test_schema_json():
    a = AuditResult("https://example.com",200,"T","D","",1,2,100,1,0,3,1,True,True,[],True,True,[],[],[],"")
    data=json.loads(a.compact_json())
    assert data["status_code"] == 200
