from pydantic import BaseModel
import yaml
from typing import Dict, List
import click

class SLA(BaseModel):
    completeness: float

class AIChecks(BaseModel):
    # Dynamic field baselines, e.g., "amount_mean": 100
    field_baselines: Dict[str, float]  # e.g., {"amount_mean": 100, "price_mean": 50}
    labels: str  # Still "consistent" for now, can expand later

class Lineage(BaseModel):
    source: str
    version: str

class Contract(BaseModel):
    dataset: str
    data_schema: Dict[str, str]  # e.g., {"id": "int", "amount": "float", "churn": "str"}
    sla: SLA
    rules: List[str]  # e.g., ["amount > 0"]
    ai_checks: AIChecks
    lineage: Lineage

def load_contract(file_path: str) -> Contract:
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return Contract(**data)
    except FileNotFoundError:
        raise click.FileError(file_path, "Contract file not found")