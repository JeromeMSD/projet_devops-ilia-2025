# validation.py
from datetime import datetime
from typing import Dict, Any, List


REQUIRED_FIELDS = ["id", "timestamp", "value"]


class ValidationError(Exception):
    pass


def validate_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Valide un enregistrement et normalise les champs."""
    # Vérifier les champs obligatoires
    missing = [f for f in REQUIRED_FIELDS if f not in record]
    if missing:
        raise ValidationError(f"Missing required fields: {missing}")

    # Normalisation : timestamp → datetime
    ts = record.get("timestamp")
    if isinstance(ts, str):
        try:
            record["timestamp"] = datetime.fromisoformat(ts)
        except ValueError:
            raise ValidationError(f"Invalid timestamp format: {ts}")

    # Exemple : value → float
    try:
        record["value"] = float(record["value"])
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid value: {record.get('value')}")

    return record


def validate_batch(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Valide une liste d’enregistrements."""
    valid_records = []
    for rec in records:
        try:
            valid_records.append(validate_record(rec))
        except ValidationError as e:
            # Pour l’instant on log simplement l’erreur (print), à remplacer par du vrai logging
            print(f"[VALIDATION ERROR] {e}")
    return valid_records
