# processing.py
from typing import List, Dict, Any
from statistics import mean


def enrich_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Exemple de traitement :
    - calcul d'un score normalisé
    - ajout d'un champ 'quality'
    """
    if not records:
        return records

    values = [r["value"] for r in records]
    avg = mean(values)

    for r in records:
        r["score"] = r["value"] / avg if avg != 0 else 0
        r["quality"] = "HIGH" if r["score"] >= 1 else "LOW"

    return records
