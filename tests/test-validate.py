import pandas as pd
from core.validate import validate_data
from core.contracts import Contract

def test_validate_schema():
    df = pd.DataFrame({"id": [1], "amount": [50.0], "churn": ["yes"]})
    contract = Contract(
        dataset="test",
        data_schema={"id": "int", "amount": "float", "churn": "str"},
        sla={"completeness": 0.99},
        rules=["amount > 0"],
        ai_checks={"field_baselines": {"amount_mean": 50}, "labels": "consistent"},
        lineage={"source": "raw.csv", "version": "v1"}
    )
    results = validate_data(contract, "dummy.csv")
    assert results["schema"] is True