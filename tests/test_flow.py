# tests/test_flow.py
from datetime import datetime
from csp_ingestor.validation import validate_record, ValidationError
from csp_ingestor.processing import enrich_records


def test_validate_record_ok():
    rec = {
        "id": "abc",
        "timestamp": datetime.now().isoformat(),
        "value": "10.5",
    }
    validated = validate_record(rec)
    assert isinstance(validated["value"], float)


def test_validate_record_missing_field():
    rec = {"id": "abc", "value": 10}
    try:
        validate_record(rec)
        assert False, "Should have raised ValidationError"
    except ValidationError:
        assert True


def test_enrich_records():
    data = [
        {"id": "1", "timestamp": datetime.now(), "value": 10.0},
        {"id": "2", "timestamp": datetime.now(), "value": 20.0},
    ]
    enriched = enrich_records(data)
    assert "score" in enriched[0]
    assert "quality" in enriched[0]
